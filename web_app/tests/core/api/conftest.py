import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_cees(api_client, player_cees):
    api_client.force_authenticate(player_cees.user)
    return api_client