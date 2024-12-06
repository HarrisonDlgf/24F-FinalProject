from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
feedback = Blueprint('feedback', __name__)

# Existing routes for /feedback/{JobID} remain unchanged

#------------------------------------------------------------
# Get all feedback instances for a specific JobID
@feedback.route('/feedback/<JobID>', methods=['GET'])
def get_feedback(JobID):
    current_app.logger.info(f'GET /feedback/<JobID> route for {JobID}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT Ratings, Comments, SubmittedBy, SubmittedFor, JobID, FeedbackID 
                      FROM feedback 
                      WHERE JobID = %s''', (JobID,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Post feedback for a specific JobID
@feedback.route('/feedback', methods=['POST'])
def post_feedback():
    current_app.logger.info('POST /feedback route')
    feedback_info = request.json
    ratings = feedback_info['Ratings']
    comments = feedback_info['Comments']
    submitted_by = feedback_info['SubmittedBy']
    submitted_for = feedback_info['SubmittedFor']
    job_id = feedback_info['JobID']

    query = '''INSERT INTO feedback (Ratings, Comments, SubmittedBy, SubmittedFor, JobID)
               VALUES (%s, %s, %s, %s, %s)'''
    data = (ratings, comments, submitted_by, submitted_for, job_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return make_response('Feedback added successfully!', 201)

#------------------------------------------------------------
# Edit feedback for a specific JobID
# Used by Maddy and Jeff after potential career growth
@feedback.route('/feedback/<JobID>', methods=['PUT'])
def update_feedback_for_job(JobID):
    current_app.logger.info(f'PUT /feedback/<JobID> route for {JobID}')
    feedback_info = request.json
    ratings = feedback_info.get('Ratings', None)
    comments = feedback_info.get('Comments', None)

    # Build query dynamically based on provided fields
    fields_to_update = []
    data = []
    if ratings:
        fields_to_update.append('Ratings = %s')
        data.append(ratings)
    if comments:
        fields_to_update.append('Comments = %s')
        data.append(comments)
    
    if not fields_to_update:
        return make_response('No valid fields provided to update.', 400)

    query = f'''UPDATE feedback SET {", ".join(fields_to_update)} 
                WHERE JobID = %s'''
    data.append(JobID)
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(data))
    db.get_db().commit()
    return make_response('Feedback updated successfully!', 200)

#------------------------------------------------------------
# Get all feedback instances for a specific StudentID
# Used by Maddy and Jeff to view feedback on their application
@feedback.route('/feedback/student/<StudentID>', methods=['GET'])
def get_feedback_for_student(StudentID):
    current_app.logger.info(f'GET /feedback/student/<StudentID> route for {StudentID}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT Ratings, Comments, SubmittedBy, SubmittedFor, JobID, FeedbackID 
                      FROM feedback 
                      WHERE SubmittedFor = %s''', (StudentID,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Post feedback for a specific StudentID
# Used by Alex to provide feedback after an application
@feedback.route('/feedback/student', methods=['POST'])
def post_feedback_for_student():
    current_app.logger.info('POST /feedback/student route')
    feedback_info = request.json
    ratings = feedback_info['Ratings']
    comments = feedback_info['Comments']
    submitted_by = feedback_info['SubmittedBy']
    submitted_for = feedback_info['SubmittedFor']

    query = '''INSERT INTO feedback (Ratings, Comments, SubmittedBy, SubmittedFor)
               VALUES (%s, %s, %s, %s)'''
    data = (ratings, comments, submitted_by, submitted_for)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return make_response('Feedback for student added successfully!', 201)

#------------------------------------------------------------
# Delete a specific feedback instance
# Used by Maddy and Jeff to remove incorrect or outdated feedback
@feedback.route('/feedback/<FeedbackID>', methods=['DELETE'])
def delete_feedback(FeedbackID):
    current_app.logger.info(f'DELETE /feedback/<FeedbackID> route for {FeedbackID}')
    cursor = db.get_db().cursor()

    # Check if the feedback exists before attempting deletion
    cursor.execute('SELECT * FROM feedback WHERE FeedbackID = %s', (FeedbackID,))
    feedback = cursor.fetchone()
    if not feedback:
        return make_response(f'Feedback with FeedbackID {FeedbackID} not found.', 404)

    # Execute the delete operation
    cursor.execute('DELETE FROM feedback WHERE FeedbackID = %s', (FeedbackID,))
    db.get_db().commit()

    # Return confirmation response
    return make_response(f'Feedback with FeedbackID {FeedbackID} deleted successfully!', 200)
