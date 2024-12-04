from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

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

# Update message types 
@communicationHistory.route('/communicationHistory/<int:student_id>/type/<string:old_type>', methods=['PUT'])
def update_message_types(student_id, old_type):
    message_info = request.json
    new_type = message_info.get('new_message_type')
    
    # Error handling
    if not new_type:
        return make_response(jsonify({"error": "new_message_type is required"}), 400)
    
    cursor = db.get_db().cursor()
    query = '''
    UPDATE CommunicationHistory
    SET MessageType = %s
    WHERE MessageID IN (
        SELECT Communication 
        FROM Student 
        WHERE StudentID = %s
    ) AND MessageType = %s
    '''
    cursor.execute(query, (new_type, student_id, old_type))
    db.get_db().commit()
    
    
    response = {
        "message": "Successfully updated messages",
        "student_id": student_id,
        "old_type": old_type,
        "new_type": new_type
    }
    
    the_response = make_response(jsonify(response))
    the_response.status_code = 200
    return the_response

# Delete a specific message or all messages for a student
@communicationHistory.route('/communicationHistory/<int:student_id>', methods=['DELETE'])
def delete_messages(student_id):
    message_id = request.args.get('message_id', default=None)
    cursor = db.get_db().cursor()
    
    if message_id:

        query = '''
        DELETE FROM CommunicationHistory
        WHERE MessageID = %s
        AND MessageID IN (
            SELECT Communication 
            FROM Student 
            WHERE StudentID = %s
        )
        '''
        cursor.execute(query, (message_id, student_id))
    else:
        query = '''
        DELETE FROM CommunicationHistory
        WHERE MessageID IN (
            SELECT Communication 
            FROM Student 
            WHERE StudentID = %s
        )
        '''
        cursor.execute(query, (student_id,))
    

    db.get_db().commit()
    
    response = {
        "message": "Successfully deleted messages",
        "student_id": student_id,
        "message_id": message_id if message_id else "all"
    }
    
    the_response = make_response(jsonify(response))
    the_response.status_code = 200
    return the_response

