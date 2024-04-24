from src.rindegastos_revops.hubspot_api.helpers.hubspot import HubspotConnectorApi, Endpoints

import requests
import pandas as pd



def read_all_properties(client:HubspotConnectorApi, endpoint:Endpoints) -> dict:

    response = requests.request("GET", client.endpoint(endpoint), headers=client.headers)

    context = {
        "status_done" : False,
    }

    if response.status_code == 200:
        response_json = response.json()

        # Verificamos la existencia de los resultados
        if "results" in response_json.keys():
            df = pd.json_normalize(response_json, record_path="results", sep="_")
            context["df"] = df
            context["status_done"] = True

    else:
        print("status_code: ", response.status_code)
        print("response:", response.text)
    
    return context
