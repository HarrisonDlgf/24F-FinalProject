from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
workexperiences = Blueprint('workexperiences', __name__)

#------------------------------------------------------------
# Get all work experiences of a specific StudentID
# Used by Alex to view candidate experience
@workexperiences.route('/workexperiences/<StudentID>', methods=['GET'])
def get_workexperiences(StudentID):
    current_app.logger.info(f'GET /workexperiences/<StudentID> route for {StudentID}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT StudentID, StartDate, EndDate, JobID, Feedback 
                      FROM workexperiences 
                      WHERE StudentID = %s''', (StudentID,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Post a new instance of work experience
# Used by Maddy and Jeff to create work experience entries
@workexperiences.route('/workexperiences', methods=['POST'])
def post_workexperience():
    current_app.logger.info('POST /workexperiences route')
    work_info = request.json
    student_id = work_info['StudentID']
    start_date = work_info['StartDate']
    end_date = work_info['EndDate']
    job_id = work_info['JobID']
    feedback = work_info.get('Feedback', None)  # Optional field

    query = '''INSERT INTO workexperiences (StudentID, StartDate, EndDate, JobID, Feedback)
               VALUES (%s, %s, %s, %s, %s)'''
    data = (student_id, start_date, end_date, job_id, feedback)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return make_response('Work experience added successfully!', 201)

#------------------------------------------------------------
# Update mutable attributes of a specific instance of work experience
# Used by Maddy and Jeff to keep work experience up to date
@workexperiences.route('/workexperiences/<JobID>', methods=['PUT'])
def update_workexperience(JobID):
    current_app.logger.info(f'PUT /workexperiences/<JobID> route for {JobID}')
    work_info = request.json
    start_date = work_info.get('StartDate', None)
    end_date = work_info.get('EndDate', None)
    feedback = work_info.get('Feedback', None)

    # Build query dynamically based on provided fields
    fields_to_update = []
    data = []
    if start_date:
        fields_to_update.append('StartDate = %s')
        data.append(start_date)
    if end_date:
        fields_to_update.append('EndDate = %s')
        data.append(end_date)
    if feedback:
        fields_to_update.append('Feedback = %s')
        data.append(feedback)
    
    if not fields_to_update:
        return make_response('No valid fields provided to update.', 400)

    query = f'''UPDATE workexperiences SET {", ".join(fields_to_update)} 
                WHERE JobID = %s'''
    data.append(JobID)
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(data))
    db.get_db().commit()
    return make_response('Work experience updated successfully!', 200)

    #------------------------------------------------------------
# Delete a specific instance of work experience
# Used by Maddy and Jeff to remove incorrect or outdated entries
@workexperiences.route('/workexperiences/<JobID>', methods=['DELETE'])
def delete_workexperience(JobID):
    current_app.logger.info(f'DELETE /workexperiences/<JobID> route for {JobID}')
    cursor = db.get_db().cursor()

    # Execute the delete operation
    cursor.execute('DELETE FROM workexperiences WHERE JobID = %s', (JobID,))
    db.get_db().commit()

    # Return confirmation response
    return make_response(f'Work experience with JobID {JobID} deleted successfully!', 200)

    #------------------------------------------------------------
# Get the most recent work experience of a specific StudentID
# Used by Alex to view the latest experience for candidates
@workexperiences.route('/workexperiences/<StudentID>/latest', methods=['GET'])
def get_latest_workexperience(StudentID):
    current_app.logger.info(f'GET /workexperiences/<StudentID>/latest route for {StudentID}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT StudentID, StartDate, EndDate, JobID, Feedback 
                      FROM workexperiences 
                      WHERE StudentID = %s
                      ORDER BY EndDate DESC
                      LIMIT 1''', (StudentID,))
    theData = cursor.fetchone()
    
    if not theData:
        return make_response(f'No work experiences found for StudentID {StudentID}', 404)
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
