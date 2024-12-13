import requests
from django.conf import settings

from apps_bridge.exceptions import ApiAccessError
from user.models import Client


class EOfficeApi:
    __base_url = settings.EOFFICE_API_URL

    @property
    def base_url(self):
        return f"{'https' if self.secure else 'http'}://{self.__base_url}/api"

    @property
    def api_key_url(self):
        return f"{self.base_url}/apiKey/planning"

    @property
    def add_user_service_url(self):
        return f"{self.base_url}/add-user-service"

    @property
    def client_list_url(self):
        return f"{self.base_url}/clientListInfo"

    @property
    def authorization_header(self):
        return {"X-Authorization": self.api_access_key}

    def __init__(self, secure=True):
        self.secure = secure
        self.load_api_key()
        self.client_list = self.get_client_list()

    def load_api_key(self):
        api_key_data = self._get_api_key()
        if not api_key_data.get("success", False):
            raise ApiAccessError("Failed to load API key")
        response_data = api_key_data.get("data")
        self.app_name = response_data.get("app_name")
        self.api_access_key = response_data.get("api_access_key")

    def _get_api_key(self):
        response = requests.get(self.api_key_url)
        response.raise_for_status()
        return response.json()

    def get_client_list(self):
        response = requests.get(
            self.client_list_url,
            headers=self.authorization_header,
        )

        res = response.json()

        if not res.get("success", False):
            raise ApiAccessError(res.get("message"))

        return res.get("data")

    def add_user_service(self, user):
        client = Client.objects.filter(
            municipality__code=user.assigned_municipality.code
        ).first()

        if not client:
            raise ApiAccessError("Client not found")

        if client.client_id not in self.client_list:
            client_id = self.client_list[-1]["central_app_client_id"]
        else:
            client_id = client.client_id

        payload = {
            "client_id": client_id,
            "branch_code": "1" if not user.assigned_ward else "",
            "ward_no": user.assigned_ward.ward_number if user.assigned_ward else "",
            "full_name": user.full_name if user.full_name else user.email,
            "email": user.email,
            "mobile_no": "",
            "is_employee_user": str(True).lower(),
            "is_representative_user": str(False).lower(),
            "login_user_name": "",
        }

        response = requests.post(
            self.add_user_service_url,
            headers=self.authorization_header,
            data=payload,
        )

        res = response.json()

        if not res.get("success", False):
            print(res)
            raise ApiAccessError(res.get("message"))

        user.eoffice_reference_code = res.get("data").get("user_service_code")
        user.save()
