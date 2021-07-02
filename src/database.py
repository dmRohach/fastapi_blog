from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import settings


engine = create_engine(
    settings.database_url,
    connect_args={'check_same_thread': False},  # because SQLite working just in one thread
)

Session = sessionmaker(engine)


def get_session() -> Session:
    session = Session()
    try:
        yield session
    finally:
        session.close()
