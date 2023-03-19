from typing import Optional

from flask_sqlalchemy import BaseQuery

from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError

from werkzeug.exceptions import NotFound

from project.models import Genre
from project.models import Director
from project.models import Movie
from project.models import User

from project.exceptions import UserAlreadyExists

from project.tools.security import generate_password_hash


from project.dao.base import BaseDAO


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie

    def get_all_by_filter(self, status: Optional[str], page: Optional[int] = None) -> list[Movie]:
        stmt: BaseQuery = self._db_session.query(self.__model__)
        if status == 'new':
            stmt = stmt.order_by(desc(self.__model__.year))
        else:
            stmt = stmt.order_by(self.__model__.year)
        if page:
            try:
                return stmt.paginate(page, self._items_per_page).items
            except NotFound:
                return []
        return stmt.all()

class UserDAO(BaseDAO[User]):
    __model__ = User


    def get_one(self, uid):
        return self._db_session.query(User).get(uid)

    def get_by_email(self, email):
        return self._db_session.query(User).filter(User.email == email).first()

    def get_all(self):
        return self._db_session.query(User).all()

    def create(self, user_d):
        try:
            user = User(**user_d)
            self._db_session.add(user)
            self._db_session.commit()
        except IntegrityError:
            raise UserAlreadyExists
        return user

    def delete(self, uid):
        user = self.get_one(uid)
        self._db_session.delete(user)
        self._db_session.commit()

    def update(self, user):
        self._db_session.add(user)
        self._db_session.commit()
        try:
            self._db_session.add(user)
            self._db_session.commit()
        except IntegrityError:
            raise UserAlreadyExists

    def update_password(self, email, new_password):
        user = self.get_by_email(email)
        user.password = generate_password_hash(new_password)

        self._db_session.add(user)
        self._db_session.commit()

