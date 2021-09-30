from models.discount_codes import DiscountCode
from models.end_points import PriceRuleEndpoints
from models.shop_credentials import  ShopCredentials
from configuration.logger import logger
import requests
from ratelimit import limits, sleep_and_retry

class PriceRule:

    """
    A class that represents a price rule in shopify.

    Attributes
    ----------
    store_dict:
        A dictionnary holding the info of the store that the price rule belongs to
    id:
        The id of the price rule
    title:
        The price rule's title, which eventually represents the code.
    value:
        The discount's value.
    once_per_customer:
        A boolean indicating whether the price rule is usable once per customer
    discount_code:
        The discount code that belongs to this price rule.

    """
    store_dict: dict
    discount_code: DiscountCode
    id: int
    title: str
    value: str
    value_type: str
    once_per_customer: bool
    target_type: str

    @sleep_and_retry
    @limits(calls=4, period=1)
    def __init__(self, shop_credentials: ShopCredentials, id: int):
        """
        Initializes the price rule class
        :param shop_credentials:
        :param id: The id of the price rule that will be fetched
        """
        logger.info(f"Fetching details of price rule with id: {id}")

        response = requests.get(shop_credentials.base_url + PriceRuleEndpoints.GET_ONE.value.format(price_rule_id=id))
        price_rule_json = response.json().get("price_rule")
        price_rule_json.pop("id")
        price_rule_json.pop("admin_graphql_api_id")
        price_rule_json.pop("created_at")
        price_rule_json.pop("updated_at")
        for k,v in price_rule_json.items():
            self.__dict__[k]=v
        self.__dict__["target_selection"] = "all"
        self.__dict__["customer_selection"] = "all"
        self.__dict__["prerequisite_product_ids"] = []
        self.__dict__["prerequisite_variant_ids"] = []
        self.__dict__["prerequisite_collection_ids"] = []
        self.__dict__["prerequisite_saved_search_ids"] = []
        self.__dict__["prerequisite_customer_ids"] = []
        self.__dict__["entitled_product_ids"] = []
        self.__dict__["entitled_variant_ids"] = []
        self.__dict__["entitled_collection_ids"] = []
        self.__dict__["entitled_country_ids"] = []

        self.shop_credentials = shop_credentials
        self.discount_code = DiscountCode(self.shop_credentials, id)

    def __eq__(self, other):
        return self.title == other.title

    def __hash__(self):
        return hash(("title", self.title))

    def is_percentage(self):
        """
        A predicate that indicates whether the price rule is a percentage or not.
        :return:
        """
        return self.value_type == "percentage"

    def to_dict(self):
        """
        Returns the JSON representation of the price rule.
        This will later be used in the HTTP data to create a price rule.
        :return:
        dict The JSON object representation of the price rule
        """
        return {"price_rule":{key: value for key, value in self.__dict__.items() if key not in ["id","shop_credentials","discount_code"]}}

    @sleep_and_retry
    @limits(calls=4, period=1)
    def create(self, shop_credentials: ShopCredentials):
        """
        Creates a new price rule with the current instance's attributes.
        :return:
        int The newly created price rule's id
        """
        logger.info(f"Creating price rule {self.title} for store {shop_credentials.site_name}")
        response = requests.post(url=shop_credentials.base_url+PriceRuleEndpoints.CREATE_ONE.value, json=self.to_dict())
        if response.status_code == 201:
            self.id = response.json().get("price_rule").get("id")
            logger.info(f"Price rule created. Title: {self.title}, ID : {self.id}")
            return self.id
        else:
            logger.info(f"Price rule couldn't be created. Title: {self.title}")
            logger.info(f"Status code: {response.status_code}")
            logger.info(f"Response text: {response.text}")
            return -1
