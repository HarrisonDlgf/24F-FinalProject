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
# Used by Jeff and Maddy to see employee feedback
# Used by David to analyze success rates
@feedback.route('/feedback/<JobID>', methods=['GET'])
def get_feedback(JobID):
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
# Used by Maddy and Jeff after completing internships
@feedback.route('/feedback', methods=['POST'])
def post_feedback():
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
# Edit feedback for a specific FeedbackID
# Used by Maddy and Jeff after potential career growth
@feedback.route('/feedback/<FeedbackID>', methods=['PUT'])
def update_feedback(FeedbackID):
    current_app.logger.info(f'PUT /feedback/<FeedbackID> route for {FeedbackID}')
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
                WHERE FeedbackID = %s'''
    data.append(FeedbackID)
    cursor = db.get_db().cursor()
    cursor.execute(query, tuple(data))
    db.get_db().commit()
    return make_response('Feedback updated successfully!', 200)