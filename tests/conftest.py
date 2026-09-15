import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# NOTA: Importamos la Base de modelos.
try:
    from src.models import Base
except ImportError:
    Base = None

@pytest.fixture
def db_session():
    """Fixture que provee una sesión de base de datos SQLite en memoria para tests aislados."""
    engine = create_engine("sqlite:///:memory:")
    
    if Base is not None:
        Base.metadata.create_engine(bind=engine)
        
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.close()