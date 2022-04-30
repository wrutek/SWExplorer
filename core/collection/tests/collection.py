from unittest.mock import patch

import petl as etl
import pytest

from collection.models import Dataset

from collection.api import Http400


@pytest.mark.django_db
def test_collection_view(swapi_people, swapi_world, client):

    response = client.get('/')
    assert response.status_code == 200
    assert len(response.context['dataset_list']) == 0
    with patch(
        'collection.views.etl.appendcsv'
    ) as mock_appendcsv:
        client.get('/fetch/')
        mock_appendcsv.assert_called_once()
        table = mock_appendcsv.call_args[0][0]
        assert isinstance(table, etl.Table)
        assert len(table) == len(swapi_people['results']) + 1  # +1 for header
        # let's see if processing took place and went smoothly
        assert table['homeworld'][0] == 'world_name'  # first and the only record

        # time for checking the database. This shouldn't rise an error
        Dataset.objects.get(path=mock_appendcsv.call_args[0][1])


@pytest.mark.django_db
def test_collection_view_many_pages(swapi_people_two_page, swapi_world, client):

    response = client.get('/')
    assert response.status_code == 200
    assert len(response.context['dataset_list']) == 0
    with patch(
        'collection.views.etl.appendcsv'
    ) as mock_appendcsv:
        client.get('/fetch/')
        assert mock_appendcsv.call_count == 2
        # for two pages only one file and one record in DB
        assert len(Dataset.objects.all()) == 1


@pytest.mark.django_db
def test_collection_swapi_error(swapi_people_error, client):
    with pytest.raises(Http400):
        client.get('/fetch/')
