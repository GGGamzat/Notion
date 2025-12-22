import socket
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    

if not DATABASE_URL:
    try:
        socket.gethostbyname('db')
        DATABASE_URL = "postgresql://postgres:postgres@db:5432/notion_db"
    except socket.gaierror:
        DATABASE_URL = "postgresql://postgres:0000@localhost:5432/notion_db"



# def is_running_in_docker():
#     try:
#         socket.gethostbyname('db')
#         return True
#     except socket.gaierror:
#         return False

# if is_running_in_docker():
#     DATABASE_URL = "postgresql://postgres:postgres@db:5432/notion_db"
# else:
#     DATABASE_URL = "postgresql://postgres:0000@localhost:5432/notion_db"




engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()