import os
import dotenv
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import now


# Base = declarative_base()

# class TempHumi(Base):
#     id = sa.Column(sa.Integer, primary_key=True)
#     temp = sa.Column(sa.Float)
#     humi = sa.Column(sa.Float)
#     time = sa.Column(sa.DateTime)

conn_local = f"mariadb+mariadbconnector://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}/rpi"

engine = sa.create_engine(conn_local)

