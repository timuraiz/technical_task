from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .tables import Base
from .settings import settings

engine = create_engine(
    settings.DATABASE_URL,
)

Session = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
)

Base.metadata.create_all(engine)


def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()
