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
@applications.route('/job/<int:job_id>', methods=['GET'])
def job_apps(job_id):
    cursor = db.get_db().cursor()
    query = ('''
    SELECT *
        FROM Applications
        WHERE JobID = %s
    ''')
    cursor.execute(query, (job_id,))
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Making more requests for applications
# Submitting a job app per jobID
@applications.route('/<int:job_id>', methods=['POST'])
def submitting_app(job_id):
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

# A Delete route for JobID in applications
@applications.route('/<int:job_id>', methods=['DELETE'])
def delete_application(job_id):
    application_info = request.json
    student_id = application_info['student_id']

    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM Applications
        WHERE StudentID = %s AND JobID = %s
    '''
    cursor.execute(query, (student_id, job_id))
    db.get_db().commit()

    return jsonify({"message": "Application deleted."}), 200

# Return all under review applications
@applications.route('/under_review', methods=['GET'])
def get_under_review():
    cursor = db.get_db().cursor()
    query = '''
        SELECT *
        FROM Applications
        WHERE Status = 'UNDER REVIEW'
    '''
    cursor.execute(query)
    theData = cursor.fetchall()

    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Based on STATUS, which is an ENUM
# GET route, returns all applications based on status
@applications.route('/<string:status>', methods=['GET'])
def get_applications_by_status(status):
    cursor = db.get_db().cursor()
    query = '''
    SELECT *
    FROM Applications
    WHERE Status = %s
    '''
    cursor.execute(query, status)
    applications = cursor.fetchall()

    response = make_response(jsonify(applications))
    response.status_code = 200
    return response

# POST route, setting the value of status
@applications.route('/<string:status>', methods=['POST'])
def set_status(status):
    application_info = request.json
    application_id = application_info['application_id']

    cursor = db.get_db().cursor()
    query = '''
    UPDATE Applications
    SET Status = %s
    WHERE ApplicationID = %s
    '''

    cursor.execute(query, (status, application_id))
    db.get_db().commit()

    response = {
        "message": f"Application {application_id} is now an updated status.",
        "new_status": status
    }

    the_response = make_response(jsonify(response))
    the_response.status_code = 200
    return the_response

# PUT route to reject an application 
@applications.route('/reject/<int:application_id>', methods=['PUT'])
def reject_application(application_id):
    cursor = db.get_db().cursor()
    query = '''
    UPDATE Applications
    SET Status = 'REJECTED'
    WHERE ApplicationID = %s
    '''

    cursor.execute(query, (application_id,))
    db.get_db().commit()

    response = {
        "message": f"Application {application_id} has been rejected.",
        "new_status": "REJECTED"
    }

    the_response = make_response(jsonify(response))
    the_response.status_code = 200
    return the_response

<<<<<<< HEAD
@applications.route('/applications/student/<int:student_id>', methods=['GET'])
=======
@applications.route('/student/<student_id>', methods=['GET'])
>>>>>>> 4397aef20a0e55207dbd58a16b38c4ba66ab14c1
def get_student_applications(student_id):
    try:
        cursor = db.get_db().cursor()
        
        # Join with Positions to get position details
        query = '''
            SELECT a.ApplicationID, a.StudentID, a.JobID, a.SubmissionDate,
                   p.PositionTitle, p.Location, p.PositionType
            FROM Applications a
            JOIN Positions p ON a.JobID = p.JobID
            WHERE a.StudentID = %s
            ORDER BY a.SubmissionDate DESC
        '''
        
        cursor.execute(query, (student_id,))
        applications = cursor.fetchall()
        
        return make_response(jsonify(applications), 200)
        
    except Exception as e:
        current_app.logger.error(f"Error in get_student_applications: {str(e)}")
        return make_response(jsonify({
            "error": str(e),
            "message": "Failed to fetch applications"
        }), 500)

