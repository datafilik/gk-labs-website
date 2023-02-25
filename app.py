from flask import Flask, render_template, jsonify
from database import load_jobs_from_db, load_job_from_db

gkLabsApp = Flask(__name__)

jobs = load_jobs_from_db()  # job list


@gkLabsApp.route("/")
def home():
  return render_template('home.html', jobs=jobs)


@gkLabsApp.route("/api/jobs")
def list_jobs():
  return jsonify(jobs)


@gkLabsApp.route("/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404

  return render_template('jobpage.html', job=job)


if __name__ == "__main__":
  gkLabsApp.run(host="0.0.0.0", debug=True)
