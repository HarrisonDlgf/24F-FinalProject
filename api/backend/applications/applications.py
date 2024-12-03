### FILE FOR APPLICATIONS FROM THE REST API MATRIX
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db



#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
applications = Blueprint('applications', __name__)

# Making a request given the blueprint
# Looking at job applications given a job id
@applications.route('/applications/<int:job_id>', methods=['GET'])
def job_apps(jobID):
    cursor = db.get_db().cursor()
    cursor.execute('''
    TO BE DONE
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Making more requests for applications
