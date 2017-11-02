from flask_login import UserMixin
import psycopg2 as dbapi2
from database import database
from passlib.apps import custom_app_context as pwd_context
import datetime
from flask_login import current_user

class User(UserMixin):
    def __init__(self, id, username, password, lastLoginDate):
        self.id = id
        self.username = username
        self.password = password
        self.lastLoginDate = lastLoginDate

class UserDatabase:
    @classmethod
    def add_user(cls, TypeID, PositionID, BirthCityID, No, Birthday, Name, Surname, username, password):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            if TypeID == 2:
                query = """INSERT INTO StatisticsInfo"""
                cursor.execute(query)
                query = """SELECT MAX(ID) FROM StatisticsInfo"""
                cursor.execute(query)
                id = cursor.fetchone()

                query = """INSERT INTO UserInfo (TypeID, PositionID, BirthCityID, CreateUserID, StatisticID, No, Birthday, 
                                                              CreateDate, Name, Surname) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (TypeID, PositionID, BirthCityID, current_user.id, id, No, Birthday, datetime.datetime.now(), Name, Surname,))
            else:
                query = """INSERT INTO UserInfo (TypeID, PositionID, BirthCityID, CreateUserID, No, Birthday, 
                                              CreateDate, Name, Surname) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(query, (TypeID, PositionID, BirthCityID, current_user.id, No, Birthday, datetime.datetime.now(), Name, Surname,))

            query = """INSERT INTO LogInfo (Username, Password) VALUES (
                                                  %s,
                                                  %s
                                )"""
            hashp = pwd_context.encrypt(password)
            try:
                cursor.execute(query, (username, hashp,))
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

    @classmethod
    def select_user(cls, username):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM LogInfo WHERE Username=%s"""

            user_data = None

            try:
                cursor.execute(query, (username,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data:
                return User(id=user_data[0], username=user_data[1], password=user_data[2], lastLoginDate = user_data[3])
            else:
                return -1

    @classmethod
    def select_user_with_id(cls, user_id):
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """SELECT * FROM LogInfo WHERE UserID=%s"""

            try:
                cursor.execute(query, (user_id,))
                user_data = cursor.fetchone()
            except dbapi2.Error:
                connection.rollback()
            else:
                connection.commit()

            cursor.close()

            if user_data:
                return User(id=user_data[0], username=user_data[1], password=user_data[2], lastLoginDate = user_data[3])
            else:
                return -1

    @classmethod
    def setLastLoginDate(cls, user):
        user.lastLoginDate = datetime.datetime.now()
        with dbapi2.connect(database.config) as connection:
            cursor = connection.cursor()

            query = """UPDATE LogInfo SET LastLoginDate =%s WHERE (UserID = %s)"""
            cursor.execute(query, (datetime.datetime.now(), user.id,))
            connection.commit()
            cursor.close()

