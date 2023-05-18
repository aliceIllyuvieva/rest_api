from sqlalchemy import create_engine, MetaData, Table, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_string = 'sqlite:///vk.db'
base = declarative_base()
db = create_engine(db_string)
base.metadata.create_all(db)

def connect():
    base.metadata.create_all(db)
    Session = sessionmaker(db)
    session = Session()
    return session

class Vk_Parsing(base):
    __tablename__ = 'vk_parsing'
    dt = Column(DateTime, primary_key=True)
    parameters = Column(String)
    groups = Column(String)

def add_vk_parsing(dt, parameters, groups, session):
    obj = Vk_Parsing(dt=dt, parameters=parameters, groups=groups)
    session.add(obj)
    session.commit()

def get_from_vk_parsing(session):
    query = session.query(Vk_Parsing).all()
    result = []
    for row in query:
        if '[]' in row.groups:
            pass
        else:
            for i in row.groups.split(','):
                result.append(i.strip())

    return list(set(result))
