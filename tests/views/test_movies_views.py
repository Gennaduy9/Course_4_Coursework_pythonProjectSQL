import pytest

from project.models import Movie


class TestMoviesView:
    @pytest.fixture
    def movie(self, db):
        obj = Movie(title='movie')
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, movie):
        response = client.get("/movies/")
        assert response.status_code == 200
        assert response.json == [{"id": movie.id, "title": movie.title}]

    def test_movie_pages(self, client, movie):
        response = client.get("/movies/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 1

        response = client.get("/movies/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 0

    def test_movie(self, client, movie):
        response = client.get("/movies/1/")
        assert response.status_code == 200
        assert response.json == {"id": movie.id, "title": movie.title}

    def test_movie_not_found(self, client, movie):
        response = client.get("/movies/2/")
        assert response.status_code == 404
