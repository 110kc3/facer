from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()
dbUrl = os.environ.get("_DATABASE_URL")
print(dbUrl)
engine = create_engine(
    "postgresql+psycopg2://sqgspjyu:LNOQ-mDRqHuUVaHyAo-OU15QYm7ryT08@tyke.db.elephantsql.com/sqgspjyu")
Session = sessionmaker(bind=engine)
session = Session()
