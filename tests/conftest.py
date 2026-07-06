import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        future=True,
    )

    Base.metadata.create_all(bind=engine)

    yield engine

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db(engine):
    connection = engine.connect()
    transaction = connection.begin()

    Session = sessionmaker(bind=connection)

    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
