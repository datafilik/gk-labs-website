import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# load environment variable from .env file
load_dotenv()

# host = os.getenv("DB_HOST")
# user = os.getenv("DB_USERNAME")
# passwd = os.getenv("DB_PASSWORD")
# db_name = os.getenv("DB_NAME")

host = os.environ["DB_HOST"]
user = os.environ["DB_USERNAME"]
passwd = os.environ["DB_PASSWORD"]
db_name = os.environ["DB_NAME"]

db_connection_uri = "mysql+pymysql://{}:{}@{}/{}?charset=utf8mb4".format(
  user, passwd, host, db_name)

engine = create_engine(db_connection_uri,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_jobs_from_db():
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs"))

    jobs = []
    for row in result.all():
      jobs.append(dict(row._mapping))
    return jobs


def load_job_from_db(id):
  with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM jobs WHERE id = {}".format(id)))
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return dict(rows[0]._mapping)


def add_application_to_db(job_id, data):
  with engine.connect() as conn:
    query = text(
      "INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) VALUES (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)"
    )

    conn.execute(
      query, {
        "job_id": job_id,
        "full_name": data['full_name'],
        "email": data['email'],
        "linkedin_url": data['linkedin_url'],
        "education": data['education'],
        "work_experience": data['work_experience'],
        "resume_url": data['resume_url']
      })
