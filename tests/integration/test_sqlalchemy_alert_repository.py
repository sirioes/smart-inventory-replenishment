import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from domain.entities.alert import Alert
from infrastructure.db.models import AlertModel, Base
from infrastructure.repositories.sqlalchemy_alert_repository import (
    SQLAlchemyAlertRepository,
)

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    db_session = SessionLocal()
    yield db_session
    db_session.close()

def test_alert_repository_save_persists_row(session):
    repo = SQLAlchemyAlertRepository(session)
    alert = Alert(recommendation_id="rec-1", status="open", channel="dashboard")

    repo.save(alert)

    saved = session.query(AlertModel).filter_by(recommendation_id="rec-1").first()
    assert saved is not None
    assert saved.status == "open"
    assert saved.channel == "dashboard"
