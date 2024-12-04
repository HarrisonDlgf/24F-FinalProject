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
feedback = Blueprint('feedback', __name__)

#------------------------------------------------------------
# Get all feedback instances for a specific JobID
# Used by Jeff, Maddy, and David to view/analyze feedback
@feedback.route('/feedback/<JobID>', methods=['GET'])
def get_feedback(JobID):
    current_app.logger.info(f'GET /feedback/<JobID> route for {JobID}')
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT FeedbackID, JobID, FeedbackText, PostedDate, StudentID 
                      FROM feedback 
                      WHERE JobID = %s''', (JobID,))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Post feedback for a specific JobID
# Used by Maddy and Jeff after completing internships
@feedback.route('/feedback', methods=['POST'])
def post_feedback():
    current_app.logger.info('POST /feedback route')
    feedback_info = request.json
    job_id = feedback_info['JobID']
    feedback_text = feedback_info['FeedbackText']
    posted_date = feedback_info.get('PostedDate')  # Optional: Defaults to server timestamp in DB
    student_id = feedback_info['StudentID']

    query = '''INSERT INTO feedback (JobID, FeedbackText, PostedDate, StudentID)
               VALUES (%s, %s, %s, %s)'''
    data = (job_id, feedback_text, posted_date, student_id)
    cursor = db.get_db().cursor()
    cursor.execute(query, data)
    db.get_db().commit()
    return make_response('Feedback added successfully!', 201)