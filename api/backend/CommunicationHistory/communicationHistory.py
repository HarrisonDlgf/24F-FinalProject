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
communicationHistory = Blueprint('communicationHistory', __name__)

#------------------------------------------------------------
# All communication for a student
@communicationHistory.route('/communicationHistory/<int:student_id>', methods=['GET'])
def get_communication_history(student_id):
    cursor = db.get_db().cursor()
    query = '''
    SELECT * 
    FROM CommunicationHistory
    WHERE MessageID IN (
        SELECT Communication 
        FROM Student 
        WHERE StudentID = %s
    )
    '''
    cursor.execute(query, student_id)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# Sending a message to an applicant based on their student ID
@communicationHistory.route('/communicationHistory/<int:student_id>', methods=['POST'])
def send_message(student_id):
    message_info = request.json
    message_type = message_info['message_type']
    message_content = message_info['message_content']
    
    cursor = db.get_db().cursor()
    query = '''
    INSERT INTO CommunicationHistory (MessageType, MessageContent)
    VALUES (%s, %s)
    '''
    cursor.execute(query, (message_type, message_content))
    db.get_db().commit()
    
    new_message_id = cursor.lastrowid
    
    update_query = '''
    UPDATE Student
    SET Communication = %s
    WHERE StudentID = %s
    '''
    cursor.execute(update_query, (new_message_id, student_id))
    db.get_db().commit()
    
    response = {
        "message": "Message sent successfully.",
        "student_id": student_id,
        "message_id": new_message_id
    }
    
    the_response = make_response(jsonify(response))
    the_response.status_code = 201
    return the_response