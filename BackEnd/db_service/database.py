from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL pour connecter la bd
DATABASE_URL = "mysql+pymysql://myuser:mypassword@192.168.37.38:3306/projetintegrateur"

# Creer l'engine et la session
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # connection test
    pool_recycle=3600,   # recycle connection
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Fonctions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


