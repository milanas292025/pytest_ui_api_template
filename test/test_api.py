import pytest
from page.ApiPage import APIClient
from config import *
 
@pytest.fixture
def client():
    return APIClient()

@pytest.mark.api
@pytest.mark.parametrize("query", VALID_SEARCHES)
def test_search_valid_queries(client, query):
    response = client.search_movies(query)

    assert response.status_code == 200
    data = response.json()
    assert "docs" in data
    assert isinstance(data["docs"], list)

@pytest.mark.api
def test_get_movie_by_id(client):
    response = client.get_movie_by_id(VALID_MOVIE_ID)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == VALID_MOVIE_ID
    assert "name" in data

@pytest.mark.api
def test_empty_query(client):
    response = client.search_movies(EMPTY_QUERY)
    assert response.status_code in [400, 422, 200]

@pytest.mark.api
def test_invalid_query(client):
    response = client.search_movies(INVALID_QUERY)
    assert response.status_code == 200
    data = response.json()
    assert len(data.get("docs", [])) == 0

@pytest.mark.api
def test_special_chars_query(client):
    response = client.search_movies(SPECIAL_CHARS_QUERY)
    assert response.status_code in [200, 400, 422]

@pytest.mark.api
def test_russian_no_spaces(client):
    response = client.search_movies(RUSSIAN_NO_SPACES)
    assert response.status_code == 200
    assert len(response.json().get("docs", [])) == 0

@pytest.mark.api
def test_without_token(client):
    response = client.get_movie_by_id(INVALID_MOVIE_ID, use_auth=False)
    assert response.status_code == 401

@pytest.mark.xfail
@pytest.mark.api
def test_wrong_http_method(client):
    response = client.request('DELETE', 'movie',
                            params={'query': 'Зеленая миля', 'page': 1, 'limit': 10})
    assert response.status_code == 405
    