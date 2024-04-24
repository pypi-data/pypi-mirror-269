from hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints
from hubspot_api.helpers.dates import str_isoformat
from hubspot_api.properties import read_all

from datetime import datetime
import json
import pandas as pd

import requests


class Search():
    def __init__(self,
                 client:HubspotConnectorApi, 
                 from_date:datetime, 
                 to_date:datetime, 
                 property_filter:str ="createdate", 
                 full_property:bool = False):
        
        self.client = client
        self.from_date = from_date
        self.to_date = to_date
        self.property_filter = property_filter
        self.full_property = full_property


    def call(self, after:int = 0, limit:int = 100) -> dict:
        
        if self.full_property:
            properties = read_all.read_all_properties(self.client, Endpoints.PROPERTIES_CONTACTS_READ_ALL)["df"]["name"].to_list()
        else:
            properties = [
                "hubspot_owner_id",
                "industry"
            ]

        payload = {
            "limit": limit,
            "after": after,
            "filterGroups": [
                {
                    "filters": [
                        {"propertyName": self.property_filter, "value": str_isoformat(self.from_date), "operator": "GTE"},
                        {"propertyName": self.property_filter, "value": str_isoformat(self.to_date), "operator": "LTE"},
                    ]
                }
            ],
            "sorts": [
                {
                "propertyName": "createdate",
                "direction": "DESCENDING"
                }
            ],
            "properties": properties
        }


        response = requests.request("POST", self.client.endpoint(Endpoints.CONTACTS_SEARCH), headers=self.client.headers, data=json.dumps(payload))

        context = {
            "status_done" : False,
            "has_next_page" : False
        }

        if response.status_code == 200:
            response_json = response.json()

            # Verificamos la existencia de los resultados
            if "results" in response_json.keys():
                df = pd.json_normalize(response_json, record_path="results", sep="_")
                context["df"] = df
                context["status_done"] = True

            # Verificamos la existencia de una página siguiente
            if "paging" in response_json.keys():
                context["next_page"] = int(response_json["paging"]["next"]["after"])
                context["has_next_page"] = True
            else:
                context["has_next_page"] = False

        else:
            print("status_code: ", response.status_code)
            print("response:", response.text)
        
        return context


    def get_dataframe(self):
        after, limit = 0, 100
        has_next_page = True

        dataframes = []
        while has_next_page:
            response = self.call(after, limit)

            if response["status_done"]:
                has_next_page = response["has_next_page"]
                df = response["df"]
                dataframes.append(df)

            if has_next_page:
                after = response["next_page"]

        data = pd.concat(dataframes)

        return data        