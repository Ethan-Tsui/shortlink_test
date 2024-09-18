import pytest
import requests
import uuid
import random
import allure

# 测试用的用户名和密码
valid_credentials = {
    "username": "myth",
    "password": "Ch096368"
}

invalid_credentials = {
    "username": "invalidUser",
    "password": "invalidPassword"
}

missing_username = {
    "username": "",
    "password": "validPassword"
}

missing_password = {
    "username": "validUser",
    "password": ""
}


def generate_unique_username():
    return f"user_{uuid.uuid4().hex}"


def generate_unique_real_name():
    return f"用户_{uuid.uuid4().hex[:6]}"


def generate_unique_phone():
    return f"186{random.randint(10000000, 99999999)}"


def generate_unique_email():
    return f"{uuid.uuid4().hex[:8]}@example.com"


@pytest.fixture
def get_login_token():
    login_url = "http://127.0.0.1:8002/api/short-link/admin/v1/user/login"
    response = requests.post(login_url, json=valid_credentials)
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    json_response = response.json()
    assert json_response["code"] == "0", f"Expected code '0', but got {json_response['code']}"
    assert json_response["message"] is None, "Expected message to be None"
    assert json_response["success"] is True, "Expected success to be True"
    # 验证 token 是否存在
    assert "token" in json_response["data"], "Response data should contain 'token'"
    assert isinstance(json_response["data"]["token"], str), "Token should be a string"
    return json_response["data"]["token"], valid_credentials["username"]


@allure.feature('User Login')
@allure.title('User Login Test Cases')
@pytest.mark.parametrize("credentials, expected_code, expected_message, expected_success, token_expected", [
    (valid_credentials, "0", None, True, True),
    (invalid_credentials, "A000001", "用户不存在", False, False),
    (missing_username, "A000001", "用户不存在", False, False),
    (missing_password, "A000001", "用户不存在", False, False),
])
@allure.description('Test the user login functionality with various credentials.')
def test_short_link_user_login(credentials, expected_code, expected_message, expected_success, token_expected):
    login_url = "http://127.0.0.1:8002/api/short-link/admin/v1/user/login"
    response = requests.post(login_url, json=credentials)

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    json_response = response.json()

    with allure.step("Verify the response content"):
        assert json_response[
                   "code"] == expected_code, f"Expected code '{expected_code}', but got {json_response['code']}"
        assert json_response[
                   "message"] == expected_message, f"Expected message '{expected_message}', but got {json_response['message']}"
        assert json_response[
                   "success"] == expected_success, f"Expected success '{expected_success}', but got {json_response['success']}"

    if token_expected:
        with allure.step("Verify the token in response"):
            assert "token" in json_response["data"], "Response data should contain 'token'"
            assert isinstance(json_response["data"]["token"], str), "Token should be a string"
    else:
        with allure.step("Verify the response data is None"):
            assert json_response["data"] is None, "Expected data to be None"


@allure.feature('User Login Status')
@allure.title('Check User Login Status')
@pytest.mark.parametrize("username, token, expected_data", [
    ("validUser", "validToken", True),
    ("validUser", "invalidToken", False),  # 测试无效 token
    ("invalidUser", "validToken", False)  # 测试无效用户名
])
@allure.description('Test the check-login functionality with various username and token combinations.')
def test_short_link_check_login(get_login_token, username, token, expected_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/user/check-login"
    valid_token, valid_username = get_login_token
    if username == "validUser":
        username = valid_username
    if token == "validToken":
        token = valid_token
    params = {
        "username": username,
        "token": token
    }
    response = requests.get(url, params=params)

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    json_response = response.json()

    with allure.step("Verify the response content"):
        assert json_response["code"] == "0", f"Expected code '0', but got {json_response['code']}"
        assert json_response["message"] is None, "Expected message to be None"
        assert json_response["success"] is True, "Expected success to be True"
        assert json_response[
                   "data"] is expected_data, f"Expected data to be {expected_data}, but got {json_response['data']}"


@allure.feature('User Logout')
@allure.title('User Logout Test Cases')
@pytest.mark.parametrize("token_type, expected_code, expected_message, expected_success", [
    ("validToken", "0", None, True),
    ("invalidToken", "A000001", "用户Token不存在或用户未登录", False),
    ("logoutTwice", "A000001", "用户Token不存在或用户未登录", False)
])
@allure.description('Test the user logout functionality with various token scenarios.')
def test_short_link_user_logout(get_login_token, token_type, expected_code, expected_message, expected_success):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/user/logout"
    valid_token, username = get_login_token
    if token_type == "validToken":
        token = valid_token
    elif token_type == "invalidToken":
        token = "invalidToken"
    elif token_type == "logoutTwice":
        # 首先正常退出登录
        params = {
            "username": username,
            "token": valid_token
        }
        logout_response = requests.delete(url, params=params)
        assert logout_response.status_code == 200, f"Expected status code 200, but got {logout_response.status_code}"
        json_response = logout_response.json()
        assert json_response["code"] == "0", f"Expected code '0', but got {json_response['code']}"
        # 再次尝试退出，使用相同的 token
        token = valid_token

    params = {
        "username": username,
        "token": token
    }
    response = requests.delete(url, params=params)

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    json_response = response.json()

    with allure.step("Verify the response content"):
        assert json_response[
                   "code"] == expected_code, f"Expected code '{expected_code}', but got {json_response['code']}"
        assert json_response[
                   "message"] == expected_message, f"Expected message '{expected_message}', but got {json_response['message']}"
        assert json_response[
                   "success"] == expected_success, f"Expected success '{expected_success}', but got {json_response['success']}"


@allure.feature('User Registration')
@allure.title('User Registration Test Cases')
@pytest.mark.parametrize("new_user_data, expected_code, expected_message, expected_success", [
    (lambda: {
        "username": generate_unique_username(),
        "password": "12345678",
        "realName": generate_unique_real_name(),
        "phone": generate_unique_phone(),
        "mail": generate_unique_email()
    }, "0", None, True),
    ({
         "username": "positive12",
         "password": "12345678",
         "realName": "重复用户",
         "phone": "18640654564",
         "mail": "existingUser@qq.com"
     }, "B000201", "用户名已存在", False)
])
@allure.description('Test the user registration functionality with new and existing user data.')
def test_user_register(new_user_data, expected_code, expected_message, expected_success):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/user"
    user_data = new_user_data() if callable(new_user_data) else new_user_data
    response = requests.post(url, json=user_data)

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    json_response = response.json()

    with allure.step("Verify the response content"):
        assert json_response[
                   "code"] == expected_code, f"Expected code '{expected_code}', but got {json_response['code']}"
        assert json_response[
                   "message"] == expected_message, f"Expected message '{expected_message}', but got {json_response['message']}"
        assert json_response[
                   "success"] == expected_success, f"Expected success '{expected_success}', but got {json_response['success']}"
