import requests
import pytest
import allure


@pytest.fixture(scope="module")
def test_data():
    headers = {
        "Content-Type": "application/json",
        "token": "ea9828ed-a379-4d0f-b987-9f21366b5d0d",
        "username": "cuntian"
    }
    return headers


@allure.feature('Short Link Stats')
@allure.story('Get Short Link Stats')
@allure.title('Test Get Short Link Stats')
@allure.description('This test case retrieves the stats for a specific short link.')
def test_short_link_stats(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/stats"
    params = {
        "fullShortUrl": "nurl.ink:8001/TFhdJ",
        "gid": "tSUBMP",
        "startDate": "2024-2-3",
        "endDate": "2024-2-6"
    }
    headers = test_data
    response = requests.get(url, params=params, headers=headers)
    response_data = response.json()

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)


@allure.feature('Short Link Stats')
@allure.story('Get Group Stats')
@allure.title('Test Get Group Stats')
@allure.description('This test case retrieves the stats for a specific group of short links.')
def test_short_link_stats_group(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/stats/group"
    params = {
        "gid": "tSUBMP",
        "startDate": "2024-2-3",
        "endDate": "2024-2-21"
    }
    headers = test_data
    response = requests.get(url, params=params, headers=headers)
    response_data = response.json()

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)


@allure.feature('Short Link Stats')
@allure.story('Get Access Record')
@allure.title('Test Get Access Record')
@allure.description('This test case retrieves the access record for a specific short link.')
def test_short_link_stats_access_record(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/stats/access-record"
    params = {
        "fullShortUrl": "nurl.ink:8001/TFhdJ",
        "gid": "tSUBMP",
        "startDate": "2024-2-3",
        "endDate": "2024-2-21",
        "current": 1,
        "size": 10
    }
    headers = test_data
    response = requests.get(url, params=params, headers=headers)
    response_data = response.json()

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)


@allure.feature('Short Link Stats')
@allure.story('Get Group Access Record')
@allure.title('Test Get Group Access Record')
@allure.description('This test case retrieves the access record for a specific group of short links.')
def test_short_link_stats_access_record_group(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/stats/access-record/group"
    params = {
        "gid": "tSUBMP",
        "startDate": "2024-2-3",
        "endDate": "2024-2-21",
        "current": 1,
        "size": 10
    }
    headers = test_data
    response = requests.get(url, params=params, headers=headers)
    response_data = response.json()

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)
