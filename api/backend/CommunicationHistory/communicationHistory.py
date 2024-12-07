from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
communicationHistory = Blueprint('communicationHistory', __name__)

# Get all messages 
@communicationHistory.route('/', methods=['GET'])
def get_all_messages():
    try:
        cursor = db.get_db().cursor()
        query = 'SELECT * FROM CommunicationHistory'
        
        current_app.logger.warning(f"Executing query: {query}")
        cursor.execute(query)
        theData = cursor.fetchall()
        
        current_app.logger.warning(f"Retrieved {len(theData)} records")
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
        return the_response
        
    except Exception as e:
        current_app.logger.warning(f"Error in get_all_messages: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch communications"
        }), 500

# Get messages for specific student
@communicationHistory.route('/<int:student_id>', methods=['GET'])
def get_student_messages(student_id):
    try:
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
        cursor.execute(query, (student_id,))
        theData = cursor.fetchall()
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
        return the_response
        
    except Exception as e:
        current_app.logger.warning(f"Error getting student messages: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch student messages"
        }), 500

# Send new message
@communicationHistory.route('/<int:student_id>/send', methods=['POST'])
def create_new_message(student_id):
    try:
        current_app.logger.warning(f"Starting message creation for student {student_id}")
        message_info = request.json
        current_app.logger.warning(f"Message info received: {message_info}")
        
        cursor = db.get_db().cursor()
        
        # Start transaction
        cursor.execute("START TRANSACTION")
        
        # Check if student exists
        current_app.logger.warning("Checking student existence...")
        check_student = 'SELECT Communication FROM Student WHERE StudentID = %s'
        cursor.execute(check_student, (student_id,))
        student = cursor.fetchone()
        
        if not student:
            current_app.logger.warning(f"Student {student_id} not found")
            cursor.execute("ROLLBACK")
            return jsonify({"error": "Student not found"}), 404
            
        # Get next MessageID - handle empty table case
        current_app.logger.warning("Getting next message ID...")
        get_max_id_query = 'SELECT MAX(MessageID) as max_id FROM CommunicationHistory'
        cursor.execute(get_max_id_query)
        result = cursor.fetchone()
        
        # Debug the result
        current_app.logger.warning(f"MAX(MessageID) query returned: {result}")
        
        # Handle the case where result is None or empty
        if result is None or result['max_id'] is None:
            new_message_id = 1
        else:
            new_message_id = result['max_id'] + 1
            
        current_app.logger.warning(f"New message ID will be: {new_message_id}")
        
        try:
            # Insert new message
            current_app.logger.warning("Inserting new message...")
            insert_query = '''
            INSERT INTO CommunicationHistory (
                MessageID, MessageType, MessageContent, Timestamp
            ) VALUES (
                %s, %s, %s, NOW()
            )
            '''
            insert_values = (new_message_id, message_info['message_type'], message_info['message_content'])
            current_app.logger.warning(f"Insert values: {insert_values}")
            cursor.execute(insert_query, insert_values)
            
            # Update student's communication field
            current_app.logger.warning(f"Updating student {student_id} with message {new_message_id}")
            update_query = '''
            UPDATE Student
            SET Communication = %s
            WHERE StudentID = %s
            '''
            cursor.execute(update_query, (new_message_id, student_id))
            
            # Commit transaction
            current_app.logger.warning("Committing transaction...")
            db.get_db().commit()
            
            return_value = {
                "message": "Message sent successfully",
                "message_id": new_message_id,
                "student_id": student_id
            }
            
            current_app.logger.warning("Message creation completed successfully")
            return make_response(jsonify(return_value), 201)
            
        except Exception as e:
            # Rollback on error
            current_app.logger.error(f"Error during transaction: {str(e)}")
            cursor.execute("ROLLBACK")
            raise e
            
    except Exception as e:
        current_app.logger.error(f"Error sending message: {str(e)}")
        current_app.logger.error(f"Error type: {type(e)}")
        import traceback
        current_app.logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            "error": str(e),
            "message": "Failed to send message"
        }), 500

# Get messages by type
@communicationHistory.route('/<int:student_id>/type/<string:message_type>', methods=['GET'])
def get_messages_by_type(student_id, message_type):
    try:
        cursor = db.get_db().cursor()
        query = '''
        SELECT * 
        FROM CommunicationHistory
        WHERE MessageType = %s
        AND MessageID IN (
            SELECT Communication 
            FROM Student 
            WHERE StudentID = %s
        )
        '''
        cursor.execute(query, (message_type, student_id))
        theData = cursor.fetchall()
        
        if not theData:
            return make_response(
                jsonify({"message": f"No messages found for type '{message_type}' and student ID {student_id}."}),
                404
            )
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
        return the_response
        
    except Exception as e:
        current_app.logger.warning(f"Error getting messages by type: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch messages by type"
        }), 500

# Delete message
@communicationHistory.route('/<int:student_id>', methods=['DELETE'])
def delete_message(student_id):
    try:
        message_id = request.args.get('message_id')
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
        
        return_value = {
            "message": "Message(s) deleted successfully",
            "student_id": student_id,
            "message_id": message_id if message_id else "all"
        }
        
        the_response = make_response(jsonify(return_value))
        the_response.status_code = 200
        return the_response
        
    except Exception as e:
        current_app.logger.warning(f"Error deleting message: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Failed to delete message"
        }), 500


