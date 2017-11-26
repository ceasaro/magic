import json

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.parametrize('username, email, p1, p2', [
    ('ceasaro', 'ceasaro@gmail.com', 'motdepasse', 'motdepasse')
])
def test_register(api_client, username, email, p1, p2):
    response = api_client.post('/api/users/register/',
                               {'username': username, 'email': email, 'password': p1, 'password2': p2})
    assert response.status_code == status.HTTP_201_CREATED
    ceasaro = User.objects.get(username=username)
    assert ceasaro.email == email


@pytest.mark.django_db
def test_get_token(api_client, player_cees):
    response = api_client.post(reverse('api:token_obtain_pair'),
                               json.dumps({'username': player_cees.user.username, 'password': 'pwd'}),
                               content_type='application/json')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['access'], 'expected refresh token in response'
    assert response.json()['refresh'], 'expected refresh token in response'


@pytest.mark.django_db
def test_access_secure_view(api_client, player_cees, user_admin):
    response = api_client.post('/api/users/', content_type='application/json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED, "No authentication, expected 401 Unauthorized"

    # test unauthorized user cees
    resp = api_client.post(reverse('api:token_obtain_pair'),
                               json.dumps({'username': player_cees.user.username, 'password': 'pwd'}),
                               content_type='application/json')
    response = api_client.get('/api/users/', content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer '+resp.json()['access'])
    assert response.status_code == status.HTTP_403_FORBIDDEN, \
        "player cees is not authorized, expected 403 Forbidden"

    # test authorized user admin
    resp = api_client.post(reverse('api:token_obtain_pair'),
                               json.dumps({'username': user_admin.username, 'password': 'secret'}),
                               content_type='application/json')
    response = api_client.get('/api/users/', content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer '+resp.json()['access'])
    assert response.status_code == status.HTTP_200_OK, \
        "admin user should rights to access the endpont, expected 200 OK"


@pytest.mark.django_db
@freeze_time("2017-11-14 00:00:00")
def test_access_token_expire_time(api_client, user_admin):
    resp = api_client.post(reverse('api:token_obtain_pair'),
                               json.dumps({'username': user_admin.username, 'password': 'secret'}),
                               content_type='application/json')
    response = api_client.get('/api/users/', content_type='application/json',
                               HTTP_AUTHORIZATION='Bearer '+resp.json()['access'])
    assert response.status_code == status.HTTP_200_OK, \
        "admin user should rights to access the endpont, expected 200 OK"

    with freeze_time("2017-11-14 00:04:59"):
        response = api_client.get('/api/users/', content_type='application/json',
                                  HTTP_AUTHORIZATION='Bearer ' + resp.json()['access'])
        assert response.status_code == status.HTTP_200_OK, \
            "admin user should rights to access the endpont, expected 200 OK"

    with freeze_time("2017-11-14 00:05:00"):
        response = api_client.get('/api/users/', content_type='application/json',
                                  HTTP_AUTHORIZATION='Bearer ' + resp.json()['access'])
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            "admin user deniend access cause token was expired (>5 min), expected 401 Unauthorized"
