import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pymysql

from dotenv import load_dotenv

Base = declarative_base()


class DBConnection:
    def __init__(self):
        load_dotenv()

        host = os.getenv("DB.HOST_MYSQL")
        port = os.getenv("DB.PORT_MYSQL")
        user = os.getenv("DB.USER_MYSQL")
        password = os.getenv("DB.PASSWORD_MYSQL")
        database = os.getenv("DB.DATABASE_MYSQL")

        try:
            conn = pymysql.connect(host=host, user=user, password=password)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            conn.commit()
            conn.close()

            self.engine = create_engine(
                f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
            )
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            print("Conexión exitosa a la base de datos con MySQL LISTA!")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {str(e)}")
            self.Session = None
