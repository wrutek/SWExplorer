import re

import pytest
import requests
import requests_mock


@pytest.fixture
def request_mock():
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def swapi_people(request_mock):
    swapi_resp = {
        'count': 1,
        'next': '',
        'previous': None,
        'results': [
            {
                'name': 'Luke Skywalker',
                'height': '172',
                'mass': '77',
                'hair_color': 'blond',
                'skin_color': 'fair',
                'eye_color': 'blue',
                'birth_year': '19BBY',
                'gender': 'male',
                'homeworld': 'https://swapi.dev/api/planets/100000/',
                'films': [
                    'https://swapi.dev/api/films/1/',
                    'https://swapi.dev/api/films/2/',
                    'https://swapi.dev/api/films/3/',
                    'https://swapi.dev/api/films/6/',
                ],
                'species': [],
                'vehicles': [
                    'https://swapi.dev/api/vehicles/14/',
                    'https://swapi.dev/api/vehicles/30/',
                ],
                'starships': [
                    'https://swapi.dev/api/starships/12/',
                    'https://swapi.dev/api/starships/22/',
                ],
                'created': '2014-12-09T13:50:51.644000Z',
                'edited': '2014-12-20T21:17:56.891000Z',
                'url': 'https://swapi.dev/api/people/1/',
            },
        ],
    }
    request_mock.get('https://swapi.dev/api/people/', json=swapi_resp)
    return swapi_resp


@pytest.fixture
def swapi_people_two_page(request_mock):
    swapi_resp_1 = {
        'count': 2,
        'next': 'https://swapi.dev/api/people/?page=2',
        'previous': None,
        'results': [
            {
                'name': 'Luke Skywalker',
                'height': '172',
                'mass': '77',
                'hair_color': 'blond',
                'skin_color': 'fair',
                'eye_color': 'blue',
                'birth_year': '19BBY',
                'gender': 'male',
                'homeworld': 'https://swapi.dev/api/planets/100000/',
                'films': [
                    'https://swapi.dev/api/films/1/',
                    'https://swapi.dev/api/films/2/',
                    'https://swapi.dev/api/films/3/',
                    'https://swapi.dev/api/films/6/',
                ],
                'species': [],
                'vehicles': [
                    'https://swapi.dev/api/vehicles/14/',
                    'https://swapi.dev/api/vehicles/30/',
                ],
                'starships': [
                    'https://swapi.dev/api/starships/12/',
                    'https://swapi.dev/api/starships/22/',
                ],
                'created': '2014-12-09T13:50:51.644000Z',
                'edited': '2014-12-20T21:17:56.891000Z',
                'url': 'https://swapi.dev/api/people/1/',
            },
        ],
    }
    swapi_resp_2 = {
        'count': 2,
        'next': '',
        'previous': None,
        'results': [
            {
                'name': 'Luke Skywalker',
                'height': '172',
                'mass': '77',
                'hair_color': 'blond',
                'skin_color': 'fair',
                'eye_color': 'blue',
                'birth_year': '19BBY',
                'gender': 'male',
                'homeworld': 'https://swapi.dev/api/planets/100000/',
                'films': [
                    'https://swapi.dev/api/films/1/',
                    'https://swapi.dev/api/films/2/',
                    'https://swapi.dev/api/films/3/',
                    'https://swapi.dev/api/films/6/',
                ],
                'species': [],
                'vehicles': [
                    'https://swapi.dev/api/vehicles/14/',
                    'https://swapi.dev/api/vehicles/30/',
                ],
                'starships': [
                    'https://swapi.dev/api/starships/12/',
                    'https://swapi.dev/api/starships/22/',
                ],
                'created': '2014-12-09T13:50:51.644000Z',
                'edited': '2014-12-20T21:17:56.891000Z',
                'url': 'https://swapi.dev/api/people/1/',
            },
        ],
    }
    request_mock.get('https://swapi.dev/api/people/', [{'json':swapi_resp_1}, {'json':swapi_resp_2}])


@pytest.fixture
def swapi_people_error(request_mock):
    request_mock.get('https://swapi.dev/api/people/', status_code=501)


@pytest.fixture
def swapi_world(request_mock):
    matcher = re.compile('https://swapi.dev/api/planets/.*')
    request_mock.get(matcher, json={'name': 'world_name'})
