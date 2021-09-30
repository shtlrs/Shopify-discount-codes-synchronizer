import requests

from exceptions.discount_code import DiscountCodeAlreadyExistant
from models.end_points import DiscountCodeEndpoints
from models.shop_credentials import ShopCredentials
from configuration.logger import logger
from ratelimit import limits, sleep_and_retry

class DiscountCode:

    """
    A class that represents a discount code in shopify

    Attributes
    ----------
    code:
        The actual discount code
    usage_count:
        The number of times the code has been used
    price_rule_id:
        The id of the price rule that wraps the discount code.
    """
    shop_credentials: ShopCredentials
    code: str
    usage_count: int

    @sleep_and_retry
    @limits(calls=4,period=1)
    def __init__(self, shop_credentials: ShopCredentials, price_rule_id):
        logger.info(f"Fetching discount codes that belong under price rule {price_rule_id}")
        self.shop_credentials = shop_credentials
        response = requests.get(url=shop_credentials.base_url+DiscountCodeEndpoints.GET_ONE.value.format(price_rule_id=price_rule_id))
        logger.info(f"{response.status_code}")
        discount_code_json_list = response.json().get("discount_codes")
        if len(discount_code_json_list)>0:
            first_discount_code_json = response.json().get("discount_codes")[0]
            self.code = first_discount_code_json.get("code",None)
            self.usage_count = first_discount_code_json.get("usage_count",0)
            self.created_at = first_discount_code_json.get("created_at")
        else:
            self.code = None
            logger.info(f"Price rule {price_rule_id} has no discount codes")

    def to_dict(self):
        """
        Returns the JSON representation of the discount code.
        This will later be used in the HTTP data to create a discount code.
        :return:
        dict The JSON object representation of the discount code
        """
        return {"discount_code": dict(
            (key, value) for key, value in self.__dict__.items() if key not in ["price_rule_id", "shop_credentials"])}

    @sleep_and_retry
    @limits(calls=4,period=1)
    def create(self, price_rule_id, shop_credentials: ShopCredentials):
        response = requests.post(url = shop_credentials.base_url+DiscountCodeEndpoints.CREATE_ONE.value.format(price_rule_id=price_rule_id),
                                 json=self.to_dict())
        if response.status_code == 201:
            logger.info(f"Discount code {self.code} with the following price rule id: {price_rule_id} has been succesfully created")
        elif response.status_code == 422:
            logger.warning(response.status_code)
            raise DiscountCodeAlreadyExistant("This discount code already exists")
