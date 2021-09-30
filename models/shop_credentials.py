from configparser import SectionProxy


class ShopCredentials:

    """
    A class with the sole purpose of holding credentials

    Attributes
    -----------
    api_key:
        The shop's api key
    password:
        The shop's password
    site_name:
        The shop's site name
    base_url:
        The shop's base url that will be used for api calls.
    """


    def __init__(self, section: SectionProxy):

        self.api_key = section.get("API_KEY")
        self.password =  section.get("PASSWORD")
        self.site_name =  section.get("SITE_NAME")
        self.base_url = f"https://{self.api_key}:{self.password}@{self.site_name}.myshopify.com"

    def to_dict(self):
        return self.__dict__