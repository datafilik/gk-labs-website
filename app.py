from flask import Flask, render_template, jsonify

flskApp = Flask(__name__)

JOBS = [{
  'id': 1,
  'title': 'Embedded Software Engineer',
  'location': 'Surrey, UK',
  'salary': '£35,000'
}, {
  'id': 2,
  'title': 'Python Developer',
  'location': 'Kent, UK'
}, {
  'id': 3,
  'title': 'Backend Engineer',
  'location': 'Remote',
  'salary': '£25,000'
}, {
  'id': 4,
  'title': 'Data Scientist',
  'location': 'Lagos, Nigeria',
  'salary': 'NGN300,000'
}]


@flskApp.route("/")
def hello_world():
  # return "<p>Hello, Viki!</p>"
  return render_template('home.html', jobs=JOBS, company_name='Gutenkraft')


@flskApp.route("/api/jobs")
def list_jobs():
  return jsonify(JOBS)


if __name__ == "__main__":
  flskApp.run(host="0.0.0.0", debug=True)
