from sqlalchemy import create_engine, Column, String, MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import insert
import os

DATABASE_URL = 'sqlite:///files.db'
engine = create_engine(DATABASE_URL)
metadata = MetaData()

files_table = Table(
    'files', metadata,
    Column('path', String, primary_key=True),
    Column('url', String),
    Column('sha', String)
)

def init_db():
    if not os.path.exists('files.db'):
        metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def get_session():
    return Session()

def upsert_files(file_list, session):
    for file in file_list:
        if file['name'].endswith('.json'):
            existing_file = session.query(files_table).filter_by(path=file['path']).first()
            if existing_file and existing_file.sha != file['sha']:
                os.remove(os.path.join('downloads', file['name']))
            stmt = insert(files_table).values(path=file['path'], url=file['download_url'], sha=file['sha'])
            do_update_stmt = stmt.on_conflict_do_update(
                index_elements=['path'],
                set_=dict(url=file['download_url'], sha=file['sha'])
            )
            session.execute(do_update_stmt)
    session.commit()

def get_file_list(session):
    return [f.path for f in session.query(files_table).all()]
