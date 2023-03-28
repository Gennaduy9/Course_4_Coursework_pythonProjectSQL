import pytest

from project.models import Movie


class TestMoviesView:
    @pytest.fixture
    def movie(self, db):
        obj = Movie(title='test_movie_1',
                  description='Прошло много лет с тех пор, как мальчик с паранормальными способностями Дэнни Торранс пережил кошмарный сезон в отеле «Оверлук», где стал свидетелем безумия и гибели своего отца. Повзрослев, Дэн вёл жизнь маргинала-алкоголика, а теперь пытается завязать и даже устроился на работу в дом престарелых. Там он безошибочно определяет, кому из постояльцев подошла очередь покинуть этот мир, за что и получил прозвище Доктор Сон. Однажды с Дэном устанавливает связь невероятно одарённая «сияющая» девочка Абра. Вскоре ей потребуется его помощь, чтобы противостоять членам организации «Истинный узел» – группы охотников за особенными детьми.',
                  trailer='https://www.youtube.com/watch?v=bkhjbv9UbPI',
                  year=2019,
                  rating=7.3,
                  genre_id=1,
                  director_id=1)
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, movie):
        response = client.get("/movies/")
        assert response.status_code == 200
        assert response.json == [{"id": movie.id,
                                  "title": movie.title,
                                  "description": movie.description,
                                  "trailer": movie.trailer,
                                  "year": movie.year,
                                  "rating": movie.rating,
                                  "genre_id": movie.genre_id,
                                  "director_id": movie.director_id
                                  }]

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
        assert response.json == {"id": movie.id,
                                 "title": movie.title,
                                  "description": movie.description,
                                  "trailer": movie.trailer,
                                  "year": movie.year,
                                  "rating": movie.rating,
                                  "genre_id": movie.genre_id,
                                  "director_id": movie.director_id
                                 }

    def test_movie_not_found(self, client, movie):
        response = client.get("/movies/2/")
        assert response.status_code == 404
