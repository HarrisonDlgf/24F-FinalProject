from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
workexperiences = Blueprint('workexperiences', __name__)

#------------------------------------------------------------
# Get all work experiences of a specific StudentID
# Used by Alex to view candidate experience
@workexperiences.route('/workexperiences/<int:student_id>', methods=['GET'])
def get_workexperiences(student_id):
    current_app.logger.info(f'GET /workexperiences/<student_id> route for {student_id}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT StudentID, StartDate, EndDate, JobID, Feedback 
                      FROM workexperiences 
                      WHERE StudentID = %s''', (student_id,))
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
@workexperiences.route('/workexperiences/<int:job_id>', methods=['PUT'])
def update_workexperience(job_id):
    current_app.logger.info(f'PUT /workexperiences/<job_id> route for {job_id}')
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
    data.append(job_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(data))
    db.get_db().commit()
    return make_response('Work experience updated successfully!', 200)

#------------------------------------------------------------
# Delete a specific instance of work experience
# Used by Maddy and Jeff to remove incorrect or outdated entries
@workexperiences.route('/workexperiences/<int:job_id>', methods=['DELETE'])
def delete_workexperience(job_id):
    current_app.logger.info(f'DELETE /workexperiences/<job_id> route for {job_id}')
    cursor = db.get_db().cursor()

    # Execute the delete operation
    cursor.execute('DELETE FROM workexperiences WHERE JobID = %s', (job_id,))
    db.get_db().commit()

    # Return confirmation response
    return make_response(f'Work experience with JobID {job_id} deleted successfully!', 200)

#------------------------------------------------------------
# Get the most recent work experience of a specific StudentID
# Used by Alex to view the latest experience for candidates
@workexperiences.route('/workexperiences/<int:student_id>/latest', methods=['GET'])
def get_latest_workexperience(student_id):
    current_app.logger.info(f'GET /workexperiences/<student_id>/latest route for {student_id}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT StudentID, StartDate, EndDate, JobID, Feedback 
                      FROM workexperiences 
                      WHERE StudentID = %s
                      ORDER BY EndDate DESC
                      LIMIT 1''', (student_id,))
    theData = cursor.fetchone()
    
    if not theData:
        return make_response(f'No work experiences found for StudentID {student_id}', 404)
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
