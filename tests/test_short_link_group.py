import pytest
import requests
import allure


@pytest.fixture(scope="module")
def test_data():
    headers = {
        "Content-Type": "application/json",
        "token": "ea9828ed-a379-4d0f-b987-9f21366b5d0d",
        "username": "cuntian"
    }
    return headers


@allure.feature('Short Link Group Management')
@allure.story('Create Group')
@allure.title('Test Create Short Link Group')
@allure.description('This test case creates a new short link group named "视频网站".')
def test_short_link_group_create(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/group"
    data = {
        "name": "视频网站"
    }
    headers = test_data
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)


@allure.feature('Short Link Group Management')
@allure.story('Search Group')
@allure.title('Test Search Short Link Group')
@allure.description('This test case searches for a short link group named "视频网站".')
def test_short_link_group_search(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/group"
    params = {
        "name": "视频网站"
    }
    headers = test_data
    response = requests.get(url, params=params, headers=headers)
    response_data = response.json()

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)


@allure.feature('Short Link Group Management')
@allure.story('Update Group')
@allure.title('Test Update Short Link Group')
@allure.description('This test case updates the name of a short link group with gid "BNstwQ" to "影音网站111".')
def test_short_link_group_update(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/group"
    data = {
        "gid": "BNstwQ",
        "name": "影音网站111"
    }
    headers = test_data
    response = requests.put(url, json=data, headers=headers)
    response_data = response.json()

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)


@allure.feature('Short Link Group Management')
@allure.story('Delete Group')
@allure.title('Test Delete Short Link Group')
@allure.description('This test case deletes a short link group with gid "we1IvT".')
def test_short_link_group_update_delete(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/group"
    params = {
        "gid": "we1IvT"
    }
    headers = test_data
    response = requests.delete(url, params=params, headers=headers)
    response_data = response.json()

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)


@allure.feature('Short Link Group Management')
@allure.story('Sort Group')
@allure.title('Test Sort Short Link Group')
@allure.description('This test case sorts the short link groups.')
def test_short_link_group_update_sort(test_data):
    url = "http://127.0.0.1:8002/api/short-link/admin/v1/group/sort"
    data = [
        {
            "gid": "BNstwQ",
            "sortOrder": 0
        },
        {
            "gid": "we1lvT",
            "sortOrder": 1
        }
    ]
    headers = test_data
    response = requests.post(url, json=data, headers=headers)
    response_data = response.json()

    with allure.step("Verify the response status code"):
        assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    with allure.step("Verify the response content"):
        assert response_data.get('success') is True, "Expected success to be True"
        allure.attach(response.text, name='Response', attachment_type=allure.attachment_type.JSON)
