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
    query = ('''
    SELECT ApplicationID, StudentID, JobID, SubmissionDate, Status
        FROM Applications
        WHERE JobID = %s
    ''')
    cursor.execute(query, jobID)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Making more requests for applications
# Submitting a job app per jobID
@applications.route('/applications/<int:job_id>', methods=['POST'])
def submitting_app(jobID):
    application_info = request.json
    student_id = application_info['student_id']
    submission_date = application_info['submission_date']

    cursor = db.get_db().cursor()
    query = ('''
    INSERT INTO Applications (StudentID, JobID, SubmissionDate, Status)
    VALUES(%s, %s, %s, %s)
    ''')
    cursor.execute(query, (student_id, job_id, submission_date, "UNDER REVIEW"))
    db.get_db().commit()

    response = {
        "message": "Application submitted.",
        "job_id": job_id,
        "student_id": student_id,
        "status": "UNDER REVIEW"
    }

    the_response = make_response(jsonify(response))
    the_response.status_code = 201  
    return the_response