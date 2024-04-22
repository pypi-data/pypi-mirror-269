import pandas as pd

from marcuslion.restcontroller import RestController


class DataProviders(RestController):
    """
    MarcusLion Providers class
    $ curl 'https://qa1.marcuslion.com/core/providers'
    """

    def __init__(self):
        super().__init__("/datasets")

    def list(self) -> any:
        """
        Providers.list()
        """
        return super().verify_get("providers", {})

    # def search(self, search) -> pd.DataFrame:
    #     """
    #     Providers.search(search)
    #     """
    #     params = {"search": search}
    #     return super().verify_get("search",  params)

    def query(self, uid) -> pd.DataFrame:
        """
        Providers.query()
        """
        params = {"id": uid}
        return super().verify_get("query",  params)


