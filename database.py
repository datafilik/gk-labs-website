import os
from sqlalchemy import create_engine, text

host = os.getenv("DB_HOST")
user = os.getenv("DB_USERNAME")
passwd = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")

db_connection_uri = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
  user, passwd, host, db_name)

engine = create_engine(db_connection_uri,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_jobs_from_db():
  with engine.connect() as conn:
    query = "select * from jobs"
    result = conn.execute(text(query))

    jobs = []
    for row in result.all():
      jobs.append(dict(row._mapping))
    return jobs
