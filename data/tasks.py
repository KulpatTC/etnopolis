import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import *


class Task(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'tasks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    question = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answer1 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answer2 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    answer3 = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    correct = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'), nullable=True)
    tag_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tags.id'), nullable=True)
