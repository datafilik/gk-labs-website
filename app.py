from flask import Flask, render_template, jsonify, request
from database import load_jobs_from_db, load_job_from_db, add_application_to_db

gkLabsApp = Flask(__name__)

jobs = load_jobs_from_db()  # job list


@gkLabsApp.route("/")
def home():
  return render_template('home.html')
  
@gkLabsApp.route("/projects")
def projects():
  return render_template('projects.html')
  
@gkLabsApp.route("/resources")
def resources():
  return render_template('resources.html')
  
@gkLabsApp.route("/careers")
def career():
  return render_template('careers.html', jobs=jobs)

@gkLabsApp.route("/about")
def about():
  return render_template('about.html')


@gkLabsApp.route("/api/careers/jobs")
def list_jobs():
  return jsonify(jobs)


@gkLabsApp.route("/careers/job/<id>")
def show_job(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404

  return render_template('jobpage.html', job=job)


@gkLabsApp.route("/api/careers/job/<id>")
def get_job_data(id):
  job = load_job_from_db(id)
  if not job:
    return "Not Found", 404

  return jsonify(job)


@gkLabsApp.route("/careers/job/<id>/apply", methods=['post'])
def apply_for_job(id):
  data = request.form  # request.args used for GET requests
  job = load_job_from_db(id)
  add_application_to_db(id, data)  # store application data to database
  return render_template('applicationsubmitted.html', form_data=data, job=job)

@gkLabsApp.route("/ops/embed_op")
def embed_op():
  return render_template('embed_op.html')

@gkLabsApp.route("/ops/snc_op")
def signal_op():
  return render_template('snc_op.html')

@gkLabsApp.route("/ops/cadnm_op")
def cadnm_op():
  return render_template('cadnm_op.html')

@gkLabsApp.route("/ops/algo_op")
def algo_op():
  return render_template('algo_op.html')

@gkLabsApp.route("/ops/data_op")
def data_op():
  return render_template('data_op.html')

@gkLabsApp.route("/ops/sim_op")
def sim_op():
  return render_template('sim_op.html')

@gkLabsApp.route("/ops/digart_op")
def digart_op():
  return render_template('digart_op.html')
  
if __name__ == "__main__":
  gkLabsApp.run(host="0.0.0.0", debug=True)
