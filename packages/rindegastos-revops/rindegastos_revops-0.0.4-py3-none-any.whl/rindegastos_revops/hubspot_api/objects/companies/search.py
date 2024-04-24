from hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints
from hubspot_api.helpers.dates import str_isoformat

from hubspot_api.properties import read_all

import requests
import pandas as pd
from datetime import datetime
import json


def search_contacts(from_date:datetime, to_date:datetime, after:int = 0, limit:int = 100, full_property:bool = False, properties:list =[]) -> dict:
    
    if full_property:
        properties = read_all.read_all_properties()["df"]["name"].to_list()

    payload = {
        "limit": limit,
        "after": after,
        "filterGroups": [
            {
                "filters": [
                    {"propertyName": "createdate", "value": str_isoformat(from_date), "operator": "GTE"},
                    {"propertyName": "createdate", "value": str_isoformat(to_date), "operator": "LTE"},
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


    response = requests.request("POST", client.endpoint(Endpoints.CONTACTS_SEARCH), headers=client.headers, data=json.dumps(payload))

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


def get_dataframe(from_date:datetime, to_date:datetime, full_property:bool = False):
    after, limit = 0, 100
    has_next_page = True

    dataframes = []
    while has_next_page:
        response = search_contacts(from_date, to_date, after, limit, full_property)

        if response["status_done"]:
            has_next_page = response["has_next_page"]
            df = response["df"]
            dataframes.append(df)

        if has_next_page:
            after = response["next_page"]

    data = pd.concat(dataframes)

    return data        