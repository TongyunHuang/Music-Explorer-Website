'''
we want to encapsulate the app inside this module
'''
import os
import sqlalchemy
from yaml import load, Loader
from flask import Flask
'''
connect to GCP database
'''
def init_connect_engine():
    # Detect if the server is running on a GCP instance or on a local computer
    if os.environ.get('GAE_ENV') != 'standard':
        variables = load(open("app.yaml"), Loader=Loader)
        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]
    
    # GCP instance feature: reads in the yaml file and sets the defined string right into its os env
    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST')
        )
    )
    return pool

db = init_connect_engine()


app = Flask(__name__)

from app import routes, songRoutes, albumRoutes, artistRoutes

    