from enum import Enum

class Endpoints(Enum):
    # Contacts
    CONTACTS = "objects/contacts"
    CONTACTS_SEARCH = "objects/contacts/search"
    # Companies
    COMPANIES_SEARCH = "objects/companies/search"
    # Properties
    PROPERTIES_CONTACTS_READ_ALL = "properties/contacts"
    PROPERTIES_COMPANIES_READ_ALL = "properties/companies"
    PROPERTIES_DEALS_READ_ALL = "properties/deals"
    PROPERTIES_TICKETS_READ_ALL = "properties/tickets"


class HubspotConnectorApi:
    def __init__(self, hubspot_api_key):
        self.base_url = "https://api.hubapi.com/crm/v3"

        self.headers = {
            'accept': "application/json",
            'content-type': "application/json",
            'authorization': f"Bearer {hubspot_api_key}"
        }
    def endpoint(self, endpoint:Endpoints):
        return f"{self.base_url}/{endpoint.value}"
