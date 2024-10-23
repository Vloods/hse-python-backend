from http import HTTPStatus
from http.client import UNPROCESSABLE_ENTITY
from typing import Any
from uuid import uuid4
import datetime

import pytest
from fastapi.testclient import TestClient

from lecture_4.demo_service.api.main import create_app
from lecture_4.demo_service.core.users import UserRole

app = create_app()


@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client


def test_register_user(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == "pro100user"


def test_get_user_by_id(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    ).json()

    response = client.post(
        "/user-get",
        params={"id": response["uid"]},
        auth=("admin", "superSecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == "pro100user"


def test_get_user_by_id(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    ).json()

    response = client.post(
        "/user-get",
        params={"id": response["uid"]},
        auth=("admin", "superSecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == "pro100user"


def test_get_user_by_username(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    ).json()

    response = client.post(
        "/user-get",
        params={"username": response["username"]},
        auth=("admin", "superSecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["username"] == "pro100user"


def test_promote_user(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    ).json()

    uid = response["uid"]

    response = client.post(
        "/user-promote",
        params={"id": uid},
        auth=("admin", "superSecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.OK

    response = client.post(
        "/user-get",
        params={"id": uid},
        auth=("admin", "superSecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()["role"] == UserRole.ADMIN


def test_get_user_by_username_none(client):

    response = client.post(
        "/user-get",
        params={"username": "ohsatana"},
        auth=("admin", "superSecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_promote_not_admin_pass(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    ).json()

    uid = response["uid"]

    response = client.post(
        "/user-promote",
        params={"id": uid},
        auth=("pro100user", "VerySecretPassword123"),
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_get_username_id_and_username(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    ).json()

    response = client.post(
        "/user-get",
        params={"username": response["username"], "id": response["uid"]},
        auth=("admin", "superSecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_username_not_id_and_username(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    ).json()

    response = client.post(
        "/user-get",
        
        auth=("admin", "superSecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_get_username_nan_username(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    ).json()

    response = client.post(
        "/user-get",
        params={"username": "ghost"},
        auth=("admin", "superSecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

def test_wrong_pass(client):
    response = client.post(
        "/user-get",
        params={"username": "ghost"},
        auth=("admin", "SecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

def test_duplicate_user(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    )
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "VerySecretPassword123",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_promote_unkownn_user(client):

    response = client.post(
        "/user-promote",
        params={"id": 777},
        auth=("admin", "superSecretAdminPassword123"),
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_pass_check(client):
    response = client.post(
        "/user-register",
        json={
            "username": "pro100user",
            "name": "user",
            "birthdate": datetime.datetime.now().isoformat(),
            "password": "123",
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST