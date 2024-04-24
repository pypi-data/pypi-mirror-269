from src.rindegastos_revops.hubspot_api.objects.contacts.search import Search
from src.rindegastos_revops.hubspot_api.helpers.hubspot import HubspotConnectorApi

import unittest
import dotenv
import os, pathlib

from datetime import datetime, timezone, timedelta
dotenv.load_dotenv(pathlib.Path("/Users/joseizam/Desktop/rindegastos/hubspot_project/.env"))


class TestSearchContact(unittest.TestCase):

    def test_search_contact(self):

        client = HubspotConnectorApi(os.getenv('API_KEY'))

        current_date = datetime.now(tz=timezone.utc)
        from_date = datetime(current_date.year, current_date.month, current_date.day)
        to_date = from_date + timedelta(days=1)

        contacts_full_property_df = Search(
            client = client, 
            from_date=from_date, 
            to_date=to_date, 
            property_filter = "createdate", 
            full_property=True).get_dataframe()

        print(contacts_full_property_df)

if __name__ == '__main__':
    unittest.main()