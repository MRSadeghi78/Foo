# import pydicom as pydicom
import os

from fastapi.testclient import TestClient

from main import app
from utils.auxiliary_service import ip_to_location

client = TestClient(app)


# Testing that server is working
def test_read_main():
    """
        Test to verify the main endpoint.

        This test verifies that the main endpoint ("/")
        returns a successful response with the message "Hello ".
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello "}


# Testing login function with wrong email and password
def test_login_failed():
    """
    Test to verify unsuccessful login with incorrect email and password.

    This test checks if the login endpoint ("/auth/login/")
    returns a 400 status code for incorrect credentials.
    """
    response = client.post("/auth/login/", json={"email": "string", "password": "string"})
    assert response.status_code == 400


# Testing login function with right email and password
def test_login_success():
    """
    Test to verify successful login with correct email and password.

    This test checks if the login endpoint ("/auth/login/")
    returns a 200 status code and a token for correct credentials.
    """
    response = client.post("/auth/login/", json={"email": "admin@admin.com", "password": "1234"})
    assert response.status_code == 200
    token = response.json()['token']
    assert token is not None
    return token


# Testing get restaurant for the unregistered user
def test_get_restaurant_failed():
    """
    Test to verify failure in retrieving restaurant data for an unregistered user.

    This test checks if the endpoint ("/restaurant/")
    returns a 401 status code for an unregistered user.
    """
    response = client.get("/restaurant/", headers={'Authorization': 'Token failed'})
    assert response.status_code == 401


# Testing update restaurant with right credentials
def test_update_restaurant():
    """
       Test to verify successful update of restaurant data with correct credentials.

       This test checks if the endpoint ("/restaurant/")
       successfully updates restaurant data with correct credentials.
    """
    token = test_login_success()
    headers = {
        'Authorization': f"Token {token}",
    }
    image_path = "SportBuddy.png"
    image_filename = os.path.basename(image_path)
    files = {
        "logo": (image_filename, open(image_path, "rb"), "image/jpeg")
    }
    response = client.put("/restaurant/", data={
        'name': 'new name', 'email': 'new email', 'mobile': 'new mobile',
        'address': 'new address', 'opening_time': 'new_opening_time',
        'closing_time': 'new closing time'
    }, headers=headers, files=files)
    assert response.status_code == 200


# Testing update restaurant with passing wrong parameters
def test_update_restaurant_failed():
    """
    Test to verify failure in updating restaurant data with incorrect credentials.
    This test checks if the endpoint ("/restaurant/")
    returns a 400 status code for incorrect parameters.
    """
    token = test_login_success()
    headers = {
        'Authorization': f"Token {token}",
    }
    image_path = "SportBuddy.png"
    image_filename = os.path.basename(image_path)
    files = {
        "logo": (image_filename, open(image_path, "rb"), "image/jpeg")
    }
    response = client.put("/restaurant/", data={
        'name': 'new name', 'email': 'new email', 'mobile': 'new mobile',
        'opening_time': 'new_opening_time', 'closing_time': 'new closing time'
    }, headers=headers, files=files)
    assert response.status_code == 400


# Testing get restaurant for the registered user
def test_get_restaurant():
    """
    Test to verify retrieval of restaurant data for a registered user.

    This test ensures that the endpoint ("/restaurant/")
    returns a successful response with restaurant data for a registered user.
    """
    token = test_login_success()
    test_update_restaurant()
    response = client.get("/restaurant/", headers={'Authorization': f"Token {token}"})
    restaurant_id = response.json()['id']
    assert response.status_code == 200
    return restaurant_id


# Testing get items/foods with registered user
def test_get_items_failed():
    """
    Test to verify retrieval of items/foods for a registered user.

    This test ensures that the endpoint ("/items/{restaurant_id}/")
    returns a failed response with items/foods for a registered user.
    """
    token = test_login_success()
    response = client.get("/items/500/", headers={'Authorization': f"Token {token}"})
    assert response.status_code == 404


# Testing get items/foods with registered user
def test_get_items_success():
    """
    Test to verify retrieval of items/foods for a registered user.

    This test ensures that the endpoint ("/items/{restaurant_id}/")
    returns a successful response with items/foods for a registered user.
    """
    token = test_login_success()
    restaurant_id = test_get_restaurant()
    response = client.get(f"/items/{restaurant_id}/", headers={'Authorization': f"Token {token}"})
    assert response.status_code == 200


# Testing create item/food with authorized user
def test_create_item():
    """
    Test to verify successful creation of item/food with authorized user.

    This test checks if the endpoint ("/items/")
    successfully creates a new item/food with complete parameters and returns a 200 status code.
    """
    token = test_login_success()
    headers = {
        'Authorization': f"Token {token}",
    }
    image_path = "SportBuddy.png"
    image_filename = os.path.basename(image_path)
    files = {
        "image": (image_filename, open(image_path, "rb"), "image/jpeg")
    }
    response = client.post("/items/", data={
        'restaurant_id': 1, 'name': 'new item', 'description': 'description', 'cost': 500,
        'price': 1000, 'is_active': True
    }, files=files, headers=headers)
    item_id = response.json()['id']
    assert response.status_code == 200
    return item_id


# Testing create item/food with authorized user
def test_create_item_failed():
    """
    Test to verify successful creation of item/food with authorized user.

    This test checks if the endpoint ("/items/")
    failed to create a new item/food with complete parameters and returns a 400 status code.
    """
    token = test_login_success()
    headers = {
        'Authorization': f"Token {token}",
    }
    image_path = "SportBuddy.png"
    image_filename = os.path.basename(image_path)
    files = {
        "image": (image_filename, open(image_path, "rb"), "image/jpeg")
    }
    response = client.post("/items/", data={
        'restaurant_id': 1, 'description': 'description', 'cost': 500,
        'price': 1000, 'is_active': True
    }, files=files, headers=headers)
    assert response.status_code == 400


# Testing update item/food with complete/valid parameters
def test_update_item():
    """
    Test to verify successful update of item/food with complete/valid parameters.

    This test checks if the endpoint ("/items/{item_id}/")
    successfully updates an existing item/food with complete parameters and
    returns a 200 status code.
    """
    token = test_login_success()
    item_id = test_create_item()
    headers = {
        'Authorization': f"Token {token}",
    }
    image_path = "SportBuddy.png"
    image_filename = os.path.basename(image_path)
    files = {
        "image": (image_filename, open(image_path, "rb"), "image/jpeg")
    }
    response = client.put(f"/items/{item_id}/", data={
        'restaurant_id': 1, 'name': 'new item', 'description': 'description', 'cost': 500,
        'price': 1000, 'is_active': True
    }, files=files, headers=headers)
    assert response.status_code == 200


# Testing update item/food with passing incomplete parameters
def test_update_item_failed():
    """
    Test to verify failure in updating item/food with incomplete parameters.
    This test checks if the endpoint ("/items/{item_id}/")
    returns a 400 status code for incomplete parameters.
    """
    token = test_login_success()
    headers = {
        'Authorization': f"Token {token}",
    }
    image_path = "SportBuddy.png"
    image_filename = os.path.basename(image_path)
    files = {
        "image": (image_filename, open(image_path, "rb"), "image/jpeg")
    }
    response = client.put("/items/1/", data={
        'restaurant_id': 1, 'description': 'description', 'cost': 500,
        'price': 1000, 'is_active': True
    }, files=files, headers=headers)
    assert response.status_code == 400


# Testing delete item/food from the restaurant
def test_delete_item():
    """
       Test to verify successful deletion of item/food from the restaurant.

       This test checks if the endpoint ("/items/{item_id}/")
       successfully deletes an existing item/food and returns a 200 status code.
    """
    token = test_login_success()
    item_id = test_create_item()
    response = client.delete(f"/items/{item_id}/", headers={'Authorization': f"Token {token}"})
    assert response.status_code == 200


# Testing delete item/food with passing wrong/invalid item_id
def test_delete_item_failed():
    """
    Test to verify failure in deleting item/food with wrong/invalid item_id.

    This test checks if the endpoint ("/items/{item_id}/")
    returns a 404 status code for wrong/invalid item_id.
    """
    token = test_login_success()
    response = client.delete("/items/1000/", headers={'Authorization': f"Token {token}"})
    assert response.status_code == 404


# Testing swagger documentation
def test_swagger():
    """
    Test to verify swagger documentation url

    This test checks if swagger path returns 200.
    """
    response = client.get("docs/")
    assert response.status_code == 200


# Testing swagger documentation
def test_auxiliary_service():
    """
    Test to check if auxiliary service is working

    This test checks if the service returns object or None.
    """
    response = ip_to_location("8.8.8.8")
    assert response is not None
