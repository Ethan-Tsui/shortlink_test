import pytest
import requests

login_url = "http://127.0.0.1:8002/api/short-link/admin/v1/user/login"

valid_credentials = {
    "username": "myth",
    "password": "Ch096368"
}


@pytest.fixture(scope="module")
def get_login_token():
    response = requests.post(login_url, json=valid_credentials)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    json_response = response.json()
    assert json_response["code"] == "0", f"Expected code '0', but got {json_response['code']}"
    assert json_response["message"] is None, "Expected message to be None"
    assert json_response["success"] is True, "Expected success to be True"
    assert "token" in json_response["data"], "Response data should contain 'token'"
    assert isinstance(json_response["data"]["token"], str), "Token should be a string"
    print(json_response["data"]["token"])
    return json_response["data"]["token"], valid_credentials["username"]
