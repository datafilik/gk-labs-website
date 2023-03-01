from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db

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


@gkLabsApp.route("/job/<id>/apply", methods=['post'])
def apply_for_job(id):
  data = request.form  # request.args used for GET requests
  job = load_job_from_db(id)
  add_application_to_db(id, data)  # store application data to database
  return render_template('applicationsubmitted.html', form_data=data, job=job)


if __name__ == "__main__":
  gkLabsApp.run(host="0.0.0.0", debug=True)
