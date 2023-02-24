from flask import Flask, render_template, jsonify
from database import load_jobs_from_db

gkLabsApp = Flask(__name__)

jobs = load_jobs_from_db()  # job list

@gkLabsApp.route("/")
def home():
  return render_template('home.html', jobs=jobs, company_name='Gutenkraft')


@gkLabsApp.route("/api/jobs")
def list_jobs():
  return jsonify(jobs)


if __name__ == "__main__":
  gkLabsApp.run(host="0.0.0.0", debug=True)
