from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sshtunnel import SSHTunnelForwarder
from wordpresser.connector import Connector

connector = Connector("wpdb", _log=False)
details = connector.details

server = SSHTunnelForwarder(
    (details["dbIp"]),
    ssh_username=details["wpUsername"],
    ssh_password=details["wpPass"],
    remote_bind_address=(details["bindAddress"], details["bindPort"]))

server.start()

SQLALCHEMY_DATABASE = 'mysql+pymysql://{user}:{password}@{host}:{port}/{db}'.format(user=details["wpDbUsername"],
                                                                                password=details["wpDbPass"],
                                                                                host=server.local_bind_host,
                                                                                port=server.local_bind_port,
                                                                                db=details["wpDb"])

wpEngine = create_engine(SQLALCHEMY_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=wpEngine)

Base = declarative_base()