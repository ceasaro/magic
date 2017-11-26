import pytest
from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_cees(api_client, player_cees):
    api_client.force_authenticate(player_cees.user)
    return api_client


@pytest.fixture
def api_request_factory():
    return APIRequestFactory()