from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder
from wordpresser.connector import Connector

connector = Connector("wmapdb", _log=False)
details = connector.details

server = SSHTunnelForwarder(
    (details["dbIp"]),
    ssh_username=details["wmapUsername"],
    ssh_password=details["wmapPass"],
    remote_bind_address=(details["bindAddress"], details["bindPort"]))

server.start()

SQLALCHEMY_DATABASE = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(user=details["wmapDbUsername"],
                                                                                password=details["wmapDbPass"],
                                                                                host=server.local_bind_host,
                                                                                port=server.local_bind_port,
                                                                                db=details["wmapDb"])

wmapEngine = create_engine(SQLALCHEMY_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=wmapEngine)

Base = declarative_base()