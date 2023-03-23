
import pytest

from project.dao import MoviesDAO
from project.models import Movie


class TestMoviesDAO:

    @pytest.fixture
    def movies_dao(self, db):
        return MoviesDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        movie_one = Movie(
            id=1,
            title='doctor_sleep',
            description='Прошло много лет с тех пор, как мальчик с паранормальными способностями Дэнни Торранс пережил кошмарный сезон в отеле «Оверлук», где стал свидетелем безумия и гибели своего отца. Повзрослев, Дэн вёл жизнь маргинала-алкоголика, а теперь пытается завязать и даже устроился на работу в дом престарелых. Там он безошибочно определяет, кому из постояльцев подошла очередь покинуть этот мир, за что и получил прозвище Доктор Сон. Однажды с Дэном устанавливает связь невероятно одарённая «сияющая» девочка Абра. Вскоре ей потребуется его помощь, чтобы противостоять членам организации «Истинный узел» – группы охотников за особенными детьми.',
            trailer='https://www.youtube.com/watch?v=bkhjbv9UbPI',
            year=2019,
            rating=7.3,
            genre_id=1,
            director_id=1,
            )

        db.session.add(movie_one)
        db.session.commit()
        return movie_one

    @pytest.fixture
    def movie_2(self, db):
        movia_two = Movie(
            id=1,
            title='cheburashka',
            description='Иногда, чтобы вернуть солнце и улыбки в мир взрослых, нужен один маленький ушастый герой. Мохнатого непоседливого зверька из далекой апельсиновой страны ждут удивительные приключения в тихом приморском городке, где ему предстоит найти себе имя, друзей и дом',
            trailer='https://www.youtube.com/watch?v=x1qvJL7NF9s',
            year=2022,
            rating=7.4,
            genre_id=2,
            director_id=2,
        )

        db.session.add(movia_two)
        db.session.commit()
        return movia_two


    def test_get_movie_by_id(self, movie_1, movies_dao):
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_by_id(1)

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all() == [movie_1, movie_2]

    def test_get_movies_by_page(self, app, movies_dao, movie_1, movie_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert movies_dao.get_all(page=1) == [movie_1]
        assert movies_dao.get_all(page=2) == [movie_2]
        assert movies_dao.get_all(page=3) == []
