from enum import Enum


class PriceRuleEndpoints(Enum):
    """
    A class that groups all endpoints related to price rules

    Attributes
    ----------
    GET_ALL:
        The endpoint to fetch all price rules of a particular shop
    GET_ONE:
        The endpoint to fetch a particular price rule by its id
    """
    GET_ALL = "/admin/api/2021-07/price_rules.json"
    GET_ONE = "/admin/api/2021-07/price_rules/{price_rule_id}.json"
    CREATE_ONE = "/admin/api/2021-07/price_rules.json"
    DELETE_ONE = "/admin/api/2021-07/price_rules/{price_rule_id}.json"

class DiscountCodeEndpoints(Enum):
    """
    A class that groups all endpoints related to discount codes

    Attributes
    ----------
    GET_ALL:
        The endpoint to fetch all discount codes of a particular shop
    GET_ONE:
        The endpoint to fetch a particular discount code by its id
    """
    GET_ALL = ""
    GET_ONE = "/admin/api/2021-07/price_rules/{price_rule_id}/discount_codes.json"
    CREATE_ONE = "/admin/api/2021-07/price_rules/{price_rule_id}/discount_codes.json"

