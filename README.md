# Gutenkraft site

Codebase for Gutenkraft website. Built on Flask framework.

# Install app dependencies

Run the command ```pip install -r requirements.txt ```.

# Update environment variables

Use the template in ```.env.example ``` to create a ```.env``` file at the directory root mostly for development environment. Same variables and value can be filled as environment secrets for hosting platform used.

# Start up Application

### In development  environment 

Run the command ``` Flask run ```.

### For production environment 

Use WSGI server Gunicorn. Find more details at https://flask.palletsprojects.com/en/stable/deploying/gunicorn/



