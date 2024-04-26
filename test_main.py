import pydicom as pydicom
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# Testing that server is working
def test_read_main():
    """
        Test to verify the main endpoint.

        This test verifies that the main endpoint ("/") returns a successful response with the message "Hello ".
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello "}


# Testing login function with wrong email and password
def test_login_failed():
    """
        Test to verify unsuccessful login with incorrect email and password.

        This test checks if the login endpoint ("/auth/login/") returns a 400 status code for incorrect credentials.
    """
    response = client.post("/auth/login/", json={"email": "string", "password": "string"})
    assert response.status_code == 400


# Testing login function with right email and password
def test_login_success():
    """
       Test to verify successful login with correct email and password.

       This test checks if the login endpoint ("/auth/login/") returns a 200 status code and a token for correct credentials.
    """
    response = client.post("/auth/login/", json={"email": "admin@admin.com", "password": "1234"})
    assert response.status_code == 200
    assert response.json()['token']


# Testing get restaurant for the registered user
def test_get_restaurant():
    """
       Test to verify retrieval of restaurant data for a registered user.

       This test ensures that the endpoint ("/restaurant/") returns a successful response with restaurant data for a registered user.
    """
    response = client.get("/restaurant/", headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


# Testing get restaurant for the unregistered user
def test_get_restaurant_failed():
    """
       Test to verify failure in retrieving restaurant data for an unregistered user.

       This test checks if the endpoint ("/restaurant/") returns a 401 status code for an unregistered user.
    """
    response = client.get("/restaurant/", headers={'Authorization': 'Token failed'})
    assert response.status_code == 401


# Testing update restaurant with right credentials
def test_update_restaurant():
    """
       Test to verify successful update of restaurant data with correct credentials.

       This test checks if the endpoint ("/restaurant/") successfully updates restaurant data with correct credentials.
    """
    dicom_file = pydicom.read_file("SportBuddy.png")
    bytes_data = dicom_file.PixelData

    # files = {"uploaded_files": ("dicom_file", bytes_data, "multipart/form-data")}
    response = client.post("/restaurant/", data={'name': 'new name', 'email': 'new email', 'mobile': 'new mobile',
                                                 'address': 'new address', 'opening_time': 'new_opening_time',
                                                 'closing_time': 'new closing time', 'logo': bytes_data},
                           headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


# Testing update restaurant with passing wrong parameters
def test_update_restaurant_failed():
    """
        Test to verify failure in updating restaurant data with incorrect credentials.

        This test checks if the endpoint ("/restaurant/") returns a 400 status code for incorrect parameters.
    """
    response = client.post("/restaurant/", data={'name': 'new name', 'email': 'new email', 'mobile': 'new mobile',
                                                 'address': 'new address', 'opening_time': 'new_opening_time',
                                                 'closing_time': 'new closing time'},
                           headers={'Authorization': 'Token failed'})
    assert response.status_code == 400


# Testing get items/foods with registered user
def test_get_items():
    """
       Test to verify retrieval of items/foods for a registered user.

       This test ensures that the endpoint ("/items/{restaurant_id}/") returns a successful response with items/foods for a registered user.
    """
    response = client.get("/items/1/", headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


# Testing create item/food with authorized user
def test_create_item():
    """
        Test to verify successful creation of item/food with authorized user.

        This test checks if the endpoint ("/items/") successfully creates a new item/food with complete parameters and returns a 200 status code.
    """
    dicom_file = pydicom.read_file("SportBuddy.png")
    bytes_data = dicom_file.PixelData
    response = client.post("/items/",
                           data={'restaurant_id': 1, 'name': 'new item', 'description': 'description', 'cost': 500,
                                 'price': 1000, 'is_active': True, 'image': bytes_data},
                           headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


# Testing create item/food with passing incomplete parameters
def test_create_item_failed():
    """
        Test to verify failure in creating item/food with incomplete parameters.

        This test checks if the endpoint ("/items/") returns a 400 status code for incomplete parameters.
    """
    response = client.post("/items/",
                           data={'restaurant_id': 1, 'name': 'new item', 'description': 'description', 'cost': 500,
                                 'price': 1000, 'is_active': True},
                           headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 400


# Testing update item/food with complete/valid parameters
def test_update_item():
    """
        Test to verify successful update of item/food with complete/valid parameters.

        This test checks if the endpoint ("/items/{item_id}/") successfully updates an existing item/food with complete parameters and returns a 200 status code.
    """
    dicom_file = pydicom.read_file("SportBuddy.png")
    bytes_data = dicom_file.PixelData
    response = client.put("/items/1/",
                          data={'restaurant_id': 1, 'name': 'new item', 'description': 'description', 'cost': 500,
                                'price': 1000, 'is_active': True, 'image': bytes_data},
                          headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


# Testing update item/food with passing incomplete parameters
def test_update_item_failed():
    """
       Test to verify failure in updating item/food with incomplete parameters.

       This test checks if the endpoint ("/items/{item_id}/") returns a 400 status code for incomplete parameters.
    """
    response = client.post("/items/1/",
                           data={'restaurant_id': 1, 'name': 'new item', 'description': 'description', 'cost': 500,
                                 'price': 1000, 'is_active': True},
                           headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 400


# Testing delete item/food from the restaurant
def test_delete_itme():
    """
       Test to verify successful deletion of item/food from the restaurant.

       This test checks if the endpoint ("/items/{item_id}/") successfully deletes an existing item/food and returns a 200 status code.
    """
    response = client.post("/items/1/", headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


# Testing delete item/food with passing wrong/invalid item_id
def test_delete_itme_failed():
    """
        Test to verify failure in deleting item/food with wrong/invalid item_id.

        This test checks if the endpoint ("/items/{item_id}/") returns a 404 status code for wrong/invalid item_id.
    """
    response = client.post("/items/1000/", headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 404
