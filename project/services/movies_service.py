from typing import Optional

from project.dao import MoviesDAO
from project.exceptions import ItemNotFound
from project.models import Movie


class MoviesService:
    def __init__(self, dao: MoviesDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> Movie:
        """
        Сервис получения одного фильма
        :param pk:
        :return:
        """
        if movie := self.dao.get_by_id(pk):
            return movie
        raise ItemNotFound(f'Movie with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None, status: Optional[str] = None) -> list[Movie]:
        """
        Сервис получения всех фильмов с возможномтью сортировки по самым новым

        """
        return self.dao.get_all_by_filter(page=page, status=status)