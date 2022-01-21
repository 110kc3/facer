from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()
dbUrl = os.environ.get("DATABASE_URL")

# engine = create_engine(dbUrl)
# Session = sessionmaker(bind=engine)
# session = Session()
session = 5
