from typing import List

from exceptions.discount_code import DiscountCodeAlreadyExistant
from models.discount_codes import DiscountCode
from models.price_rules import PriceRule
from models.shop_credentials import ShopCredentials
from configuration.logger import logger
from models.end_points import PriceRuleEndpoints
from utils.date import get_last_hour_date_string
import re
import requests
from ratelimit import limits, sleep_and_retry


class ShopifyStore:
    """
    A class that represents a store in shopify

    Attribute
    ---------
    discount_codes:
        A list of discount code objects
    price_rule_ids:
        A list of the price rules ids that are part of the store.
    base_url: str
        The shop's api base url.
    """

    discount_codes: List[DiscountCode]
    price_rules: List[PriceRule] = []
    price_rules_to_add: List[PriceRule] = []
    price_rules_titles: List[str] = []

    def __init__(self,shop_credentials):
        self.price_rules_to_add = []
        self.price_rules_titles = []
        self.price_rules = []
        self.shop_credentials = shop_credentials

    def __contains__(self, item):

        return item.title in self.price_rules_titles

    @sleep_and_retry
    @limits(calls=4, period=1)
    def fetch_last_hour_price_rules(self):
        """
        Fetches all the price rules ids that are present in the store and that were created
        one hour before the current time at which the function is being executed
        :return:
        """
        logger.info(f"Fetching all price rules ids for site {self.shop_credentials.site_name}")

        last_hour_date_string = get_last_hour_date_string()
        next_end_point_regex_pattern = r"<https://(.*)\.myshopify\.com(.*)>"
        has_next_endpoint_regex_pattern = f"(.*)(rel=\"next\")"

        query_params = {"limit":250, "created_at_min":last_hour_date_string}
        r = requests.get(self.shop_credentials.base_url + PriceRuleEndpoints.GET_ALL.value, params=query_params)
        price_rules_dicts = r.json().get("price_rules")
        for price_rules_dict in price_rules_dicts:
            price_rule_id = price_rules_dict.get("id")
            price_rule = PriceRule(self.shop_credentials, price_rule_id)
            self.price_rules.append(price_rule)
            self.price_rules_titles.append(price_rule.title)

        headers = r.headers.get("Link", None)

        if headers is not None:
            has_next_end_points_match_groups = re.match(has_next_endpoint_regex_pattern, headers)
        else:
            has_next_end_points_match_groups = None

        if has_next_end_points_match_groups == None:
            return

        count = 1

        while "Link" in r.headers.keys():
            logger.info(f"Getting price rules from page {count}")
            end_points_match_groups = re.match(next_end_point_regex_pattern,r.headers.get("Link"))
            url = end_points_match_groups.group(1)
            r = requests.get(self.shop_credentials.base_url+url)
            price_rules_dicts = r.json().get("price_rules")
            for price_rules_dict in price_rules_dicts:
                price_rule_id = price_rules_dict.get("id")
                price_rule = PriceRule(self.shop_credentials, price_rule_id)
                self.price_rules.append(price_rule)
                self.price_rules_titles.append(price_rule.title)

            has_next_end_points_match_groups = re.match(has_next_endpoint_regex_pattern,r.headers.get("Link"))
            if has_next_end_points_match_groups == None:
                break

            count+=1

        logger.info(f"All price rules for site {self.shop_credentials.site_name} have been fetched")


    def add_missing_price_rules(self, price_rules_available_in_all_stores: List[PriceRule]):
        """
        Adds all the missing price rules in the store.
        This will get a list of all the available price rules in all stores and compare them to the ones available in it.
        Then it'll make HTTP requests to build them.

        :param price_rules_available_in_all_stores: A list of all the price rules available in all stores.
        :return:
        """
        logger.info(f"Filtering all price rules for store {self.shop_credentials.site_name}")
        self.price_rules_to_add = list(set(price_rules_available_in_all_stores) - set(self.price_rules))

        if len(self.price_rules_to_add)==0:
            logger.info(f"Nothing to do for store {self.shop_credentials.site_name}")
            return

        for price_rule in self.price_rules_to_add:
            if price_rule.discount_code.code is not None and price_rule.is_percentage():
                try:
                    new_price_rule_id = price_rule.create(shop_credentials=self.shop_credentials)
                    price_rule.discount_code.create(price_rule_id=new_price_rule_id,
                                                    shop_credentials=self.shop_credentials)

                except AttributeError:
                    logger.exception(f"The following price rule {price_rule.title} in shop {self.shop_credentials.site_name} has no discount code")
                except DiscountCodeAlreadyExistant:
                    self.delete_price_rule(self.shop_credentials,new_price_rule_id)
                except Exception as e:
                    logger.exception("The following exception happened while creating a new price rule")
                    logger.exception(e)

    @sleep_and_retry
    @limits(calls=4, period=1)
    def delete_price_rule(self, shop_credentials: ShopCredentials, price_rule_id):
        """
        Deletes a specific price rule
        :param shop_credentials: The shop's credentials from which the price rule will be deleted
        :param price_rule_id: The id of the price rule that will be deleted
        :return:
        """
        requests.delete(shop_credentials.base_url + PriceRuleEndpoints.DELETE_ONE.value.format(
            price_rule_id=price_rule_id))