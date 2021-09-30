from configuration.config import sections
from configuration.logger import logger
from models.shop_credentials import ShopCredentials
from models.shopify_store import ShopifyStore
from typing import List
from threading import Thread

if __name__ == '__main__':
    stores: List[ShopifyStore] = []

    logger.info("Loading all shop credentials")
    shop_credentials_list = [ShopCredentials(section) for section in sections]

    logger.info("Instantiating all shopify stores")

    stores: List[ShopifyStore] = [ShopifyStore(shop_credentials=shop_credentials) for shop_credentials in shop_credentials_list]

    store_threads = dict()

    for store in stores:
        store_threads[store.shop_credentials.site_name]= Thread(target=store.fetch_last_hour_price_rules)

    for thread in store_threads.values():
        thread.start()

    for thread in store_threads.values():
        thread.join()

    price_rules_available_in_all_stores = []

    logger.info("Gathering all the price rules available across the stores")
    for store in stores:
        price_rules_available_in_all_stores+= store.price_rules

    price_rules_available_in_all_stores = list(set(price_rules_available_in_all_stores))

    threads = dict()
    for store in stores:
        threads[store.shop_credentials.site_name]= Thread(target=store.add_missing_price_rules, args=(price_rules_available_in_all_stores,))
        # store.add_missing_price_rules(price_rules_available_in_all_stores=price_rules_available_in_all_stores)

    for thread in threads.values():
        thread.start()

    for thread in threads.values():
        thread.join()