from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = 'postgresql://postgres:112002@localhost:5432/Nikhilesh'

engine = create_engine(db_url)

Session = sessionmaker(bind=engine)