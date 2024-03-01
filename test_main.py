import pydicom as pydicom
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello "}


def test_login_failed():
    response = client.post("/auth/login/", json={"email": "string", "password": "string"})
    assert response.status_code == 400


def test_login_success():
    response = client.post("/auth/login/", json={"email": "admin@admin.com", "password": "1234"})
    assert response.status_code == 200
    assert response.json()['token']


def test_get_restaurant():
    response = client.get("/restaurant/", headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


def test_get_restaurant_failed():
    response = client.get("/restaurant/", headers={'Authorization': 'Token failed'})
    assert response.status_code == 401


def test_update_restaurant():
    dicom_file = pydicom.read_file("SportBuddy.png")
    bytes_data = dicom_file.PixelData

    # files = {"uploaded_files": ("dicom_file", bytes_data, "multipart/form-data")}
    response = client.post("/restaurant/", data={'name': 'new name', 'email': 'new email', 'mobile': 'new mobile', 'address': 'new address', 'opening_time': 'new_opening_time', 'closing_time': 'new closing time', 'logo': bytes_data}, headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


def test_update_restaurant_failed():
    response = client.post("/restaurant/", data={'name': 'new name', 'email': 'new email', 'mobile': 'new mobile', 'address': 'new address', 'opening_time': 'new_opening_time', 'closing_time': 'new closing time'}, headers={'Authorization': 'Token failed'})
    assert response.status_code == 400


def test_get_items():
    response = client.get("/items/1/", headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


def test_create_item():
    dicom_file = pydicom.read_file("SportBuddy.png")
    bytes_data = dicom_file.PixelData
    response = client.post("/items/", data={'restaurant_id': 1, 'name': 'new item', 'description': 'description', 'cost': 500, 'price': 1000, 'is_active': True, 'image': bytes_data}, headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


def test_create_item_failed():
    response = client.post("/items/", data={'restaurant_id': 1, 'name': 'new item', 'description': 'description', 'cost': 500, 'price': 1000, 'is_active': True}, headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 400


def test_update_item():
    dicom_file = pydicom.read_file("SportBuddy.png")
    bytes_data = dicom_file.PixelData
    response = client.put("/items/1/", data={'restaurant_id': 1, 'name': 'new item', 'description': 'description', 'cost': 500, 'price': 1000, 'is_active': True, 'image': bytes_data}, headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


def test_update_item_failed():
    response = client.post("/items/1/", data={'restaurant_id': 1, 'name': 'new item', 'description': 'description', 'cost': 500, 'price': 1000, 'is_active': True}, headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 400


def test_delete_itme():
    response = client.post("/items/1/", headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 200


def test_delete_itme_failed():
    response = client.post("/items/1000/", headers={'Authorization': 'Token 47fe017a65fa475d99d2afe16df76fa5'})
    assert response.status_code == 404

