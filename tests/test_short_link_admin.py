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


@allure.feature('Short Link Management')
@allure.story('Create Short Link')
@allure.title('Test Create Short Link')
@allure.description('This test case creates a new short link.')
def test_create_short_link(test_data):
    headers = test_data
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/create"
    data = {
        "domainProtocol": "http://",
        "domain": "nurl.ink",
        "originUrl": "https://nageoffer.com/",
        "gid": "dKgtNk",
        "createdType": 1,
        "validDateType": 1,
        "validDate": "",
        "describe": "default short url"
    }
    response = requests.post(url, json=data, headers=headers)

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    response_data = response.json()

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        assert response_data.get('code') == "0", "Expected code to be '0'"

        data = response_data.get('data')
        assert data is not None, "Response data should not be None"
        assert data.get('gid') == "dKgtNk", "Expected gid to be 'dKgtNk'"
        assert data.get('originUrl') == "https://nageoffer.com/", "Expected originUrl to be 'https://nageoffer.com/'"
        assert data.get('fullShortUrl') is not None, "Expected fullShortUrl to be present"

        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)


@allure.feature('Short Link Management')
@allure.story('Update Short Link')
@allure.title('Test Update Short Link')
@allure.description('This test case updates a short link.')
def test_update_short_link(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/update"
    data = {
        "fullShortUrl": "http://baidu.com/2z9dv1",
        "originUrl": "http://nageoffer.com",
        "gid": "dKgtNk",
        "validDateType": 1,
        "validDate": "2022-01-01 00:00:00",
        "describe": "hello"
    }
    headers = test_data
    response = requests.post(url, json=data, headers=headers)

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    response_data = response.json()

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        assert response_data.get('code') == "0", "Expected code to be '0'"
        assert response_data.get('data') is None, "Expected data to be None"
        assert response_data.get('message') is None, "Expected message to be None"
        assert response_data.get('requestId') is None, "Expected requestId to be None"

        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)


@allure.feature('Short Link Management')
@allure.story('Page Short Link')
@allure.title('Test Page Short Link')
@allure.description('This test case retrieves a paginated list of short links.')
def test_page_short_link(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/page"
    params = {
        "gid": "dKgtNk",
        "current": "1",
        "size": "10",
        "orderTag": "createTime"
    }
    headers = test_data
    response = requests.get(url, params=params, headers=headers)
    response_data = response.json()

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"

        data = response_data["data"]
        assert "records" in data, "Response data should contain 'records'"
        assert isinstance(data["records"], list), "'records' should be a list"

        for record in data["records"]:
            assert "id" in record, "Each record should contain 'id'"
            assert "shortUri" in record, "Each record should contain 'shortUri'"
            assert "fullShortUrl" in record, "Each record should contain 'fullShortUrl'"
            assert "originUrl" in record, "Each record should contain 'originUrl'"

        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)
