from flask import Flask
from flask_cors import CORS

from backend.db_connection import db
from backend.simple.simple_routes import simple_routes
from backend.applications.applications import applications
from backend.CommunicationHistory.communicationHistory import communicationHistory
from backend.coop.coop import coop
from backend.feedback.feedback import feedback
from backend.positions.positions import positions
from backend.Startups.startups import startups
from backend.upload.upload import upload_bp
from backend.workexperiences.workexperiences import workexperiences



import os
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'startupsrule'
    app.config['MYSQL_DATABASE_HOST'] = 'mysql_db'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_DB'] = 'StartUpConnect'  # Change this to your DB name

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)


    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(simple_routes)
    app.register_blueprint(applications, url_prefix='/applications')
    app.register_blueprint(communicationHistory, url_prefix='/communication-history')
    app.register_blueprint(coop, url_prefix='/coop')
    app.register_blueprint(feedback, url_prefix='/feedback')
    app.register_blueprint(positions, url_prefix='/positions')
    app.register_blueprint(startups, url_prefix='/startups')
    app.register_blueprint(upload_bp, url_prefix='/upload')
    app.register_blueprint(workexperiences, url_prefix='/work-experiences')

    # Don't forget to return the app object
    return app

