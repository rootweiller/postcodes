# postcodes
Practice for API postcodes


# Instalation

for install create a environment with pyenv and run

    <code>pip install -r requirements.txt</code>


# Run Django Rest Framework

for run server web run 

    <code>python manage.py runserver</code> 

into file_path api


# Run apache airflow

for run apache airflow run those commands

    <code>airflow db init</code>
    <code>airflow webserver -D </code>
    <code>airflow scheduler -D </code>

# Database

use postgresql, run docker for postgres

    <code>docker pull postgres</code>
    <code>docker run --name YOUR_DOCKER_NAME -e POSTGRES_PASSWORD=YOUR_PASSWORD -p 5432:5432 -d postgres</code>


# Documentation
When run webserver open browser <code>http://127.0.0.1:8000/redoc</code>
