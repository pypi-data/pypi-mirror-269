from etiket_client.remote.client import client
from etiket_client.remote.endpoints.models.user import UserReadWithScopes

def api_version() -> str:
    response = client.get("/version/")
    return response