import functools
import decimal
from application import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError
from application.exception.util import raise_server_exc
from application.exception.error_code import DATABASE_UNKNOWN_ERROR

engines = {}

for role, role_settings in config.MYSQL.items():
    role_url = ("mysql+pymysql://{user}:{passwd}@{host}:{port}/{database}"
                "?charset=utf8".format(**role_settings))
    engines[role] = create_engine(role_url,
                                  pool_size=100,
                                  max_overflow=-1,
                                  pool_recycle=10)

DBSession = scoped_session(
    sessionmaker(autocommit=False, autoflush=True, bind=engines['master']))


ModelBase = declarative_base()


def make_commit_decorator(DBSession):
    """Make a decorator to commit session::

        DBSession = make_db_session(engines)
        defer_commit = make_commit_decorator(DBSession)

        @defer_commit
        def do_things():
            pass
    """

    def decorated(func):
        @functools.wraps(func)
        def func_(*args, **kwargs):
            ret = func(*args, **kwargs)
            session = DBSession()
            try:
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise_server_exc(DATABASE_UNKNOWN_ERROR, exc=e)
            except BaseException as e:
                session.rollback()
                raise_server_exc(DATABASE_UNKNOWN_ERROR, exc=e)
            finally:
                session.close()
            return ret

        return func_

    return decorated


db_commit = make_commit_decorator(DBSession)


class BreezeModel(object):
    def to_dict(self):
        result = {}
        for key, value in self.__dict__.iteritems():
            if key.startswith('_'):
                continue
            if isinstance(value, decimal.Decimal):
                result[key] = float(value)
            else:
                result[key] = value
        return result
