### FILE FOR POSITIONS FROM THE REST API MATRIX
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db



#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
positions = Blueprint('positions', __name__)

@positions.route('/', methods=['GET'])
def get_positions():
    try:
        cursor = db.get_db().cursor()
        
        # Base query with JOIN to get startup name
        query = '''
            SELECT p.*, s.Name as CompanyName 
            FROM Positions p 
            INNER JOIN Startups s ON p.StartUpID = s.StartupID 
            WHERE 1=1
        '''
        params = []
        
        # Add filters if they exist
        if request.args.get('JobID'):
            query += ' AND p.JobID = %s'
            params.append(request.args.get('JobID'))
        
        cursor.execute(query, tuple(params))
        theData = cursor.fetchall()
        
        return make_response(jsonify(theData), 200)
        
    except Exception as e:
        current_app.logger.warning(f"Error in get_positions: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch positions"
        }), 500

# POST new position request
@positions.route('/', methods=['POST'])
def create_position():
    try:
        current_app.logger.info('Processing position creation request')
        position_details = request.json
        
        cursor = db.get_db().cursor()
        cursor.execute('''
        INSERT INTO positions (
            PositionTitle,
            ContactEmail,
            ExperienceRequired,
            Industry,
            Location,
            StartDate,
            Skills,
            SalaryRange,
            PositionType,
            StartUpName,
            StartUpID,
            JobID
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )''', (
            position_details['PositionTitle'],
            position_details['ContactEmail'],
            position_details['ExperienceRequired'],
            position_details['Industry'],
            position_details['Location'],
            position_details['StartDate'],
            position_details['Skills'],
            position_details['SalaryRange'],
            position_details['PositionType'],
            position_details['StartUpName'],
            position_details['StartUpID'],
            position_details['JobID']
        ))
        
        db.get_db().commit()
        
        return_value = {
            'message': 'Position created successfully'
        }
        
        the_response = make_response(jsonify(return_value))
        the_response.status_code = 201  # 201 means "Created"
        return the_response
        
    except KeyError as e:
        return_value = {
            'error': f'Missing required field: {str(e)}'
        }
        return make_response(jsonify(return_value), 400)
    except Exception as e:
        return_value = {
            'error': f'Error creating position: {str(e)}'
        }
        return make_response(jsonify(return_value), 500)

# Deleting position from database
@positions.route('/<int:job_id>', methods=['DELETE'])
def delete_position(job_id):
    try:
        cursor = db.get_db().cursor()
        cursor.execute('DELETE FROM positions WHERE JobID = %s', (job_id,))
        
        if cursor.rowcount == 0:
            # No position found with this ID
            return_value = {
                'error': f'No position found with ID {job_id}'
            }
            return make_response(jsonify(return_value), 404)
        
        db.get_db().commit()
        
        return_value = {
            'message': f'Position {job_id} deleted successfully'
        }
        return make_response(jsonify(return_value), 200)
        
    except Exception as e:
        return_value = {
            'error': f'Error deleting position: {str(e)}'
        }
        return make_response(jsonify(return_value), 500)

# Making a request given the blueprint
# Updating a position
@positions.route('/<int:job_id>', methods=['PATCH'])
def update_position(job_id):
    try:
        current_app.logger.info(f'Processing position update request for ID {job_id}')
        updates = request.json
        
        # Start building the dynamic update query
        query_parts = []
        params = []
        
        # Build query dynamically based on provided fields
        if 'PositionTitle' in updates:
            query_parts.append('PositionTitle = %s')
            params.append(updates['PositionTitle'])
            
        if 'ContactEmail' in updates:
            query_parts.append('ContactEmail = %s')
            params.append(updates['ContactEmail'])
            
        if 'ExperienceRequired' in updates:
            query_parts.append('ExperienceRequired = %s')
            params.append(updates['ExperienceRequired'])
            
        if 'Industry' in updates:
            query_parts.append('Industry = %s')
            params.append(updates['Industry'])
            
        if 'Location' in updates:
            query_parts.append('Location = %s')
            params.append(updates['Location'])
            
        if 'StartDate' in updates:
            query_parts.append('StartDate = %s')
            params.append(updates['StartDate'])
            
        if 'Skills' in updates:
            query_parts.append('Skills = %s')
            params.append(updates['Skills'])
            
        if 'SalaryRange' in updates:
            query_parts.append('SalaryRange = %s')
            params.append(updates['SalaryRange'])
            
        if 'PositionType' in updates:
            query_parts.append('PositionType = %s')
            params.append(updates['PositionType'])
            
        if 'StartUpName' in updates:
            query_parts.append('StartUpName = %s')
            params.append(updates['StartUpName'])
        
        if not query_parts:
            return_value = {
                'error': 'No valid fields provided for update'
            }
            return make_response(jsonify(return_value), 400)
        
        # Construct the final query
        query = 'UPDATE positions SET ' + ', '.join(query_parts) + ' WHERE JobID = %s'
        params.append(job_id)
        
        # Execute the update
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(params))
        
        if cursor.rowcount == 0:
            return_value = {
                'error': f'No position found with ID {job_id}'
            }
            return make_response(jsonify(return_value), 404)
        
        db.get_db().commit()
        
        return_value = {
            'message': f'Position {job_id} updated successfully'
        }
        return make_response(jsonify(return_value), 200)
        
    except Exception as e:
        return_value = {
            'error': f'Error updating position: {str(e)}'
        }
        return make_response(jsonify(return_value), 500)

# Replacing all details of a position
@positions.route('/<int:job_id>', methods=['PUT'])
def replace_position(job_id):
    try:
        current_app.logger.info(f'Processing position replacement request for ID {job_id}')
        new_position = request.json
        
        # Ensure all required fields are provided
        required_fields = [
            'PositionTitle', 'ContactEmail', 'ExperienceRequired', 
            'Industry', 'Location', 'StartDate', 'Skills', 
            'SalaryRange', 'PositionType', 'StartUpName', 'StartUpID'
        ]
        missing_fields = [field for field in required_fields if field not in new_position]
        
        if missing_fields:
            return_value = {
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }
            return make_response(jsonify(return_value), 400)
        
        # Replace the position details
        query = '''
        UPDATE positions 
        SET 
            PositionTitle = %s, 
            ContactEmail = %s, 
            ExperienceRequired = %s, 
            Industry = %s, 
            Location = %s, 
            StartDate = %s, 
            Skills = %s, 
            SalaryRange = %s, 
            PositionType = %s, 
            StartUpName = %s, 
            StartUpID = %s
        WHERE JobID = %s
        '''
        params = (
            new_position['PositionTitle'],
            new_position['ContactEmail'],
            new_position['ExperienceRequired'],
            new_position['Industry'],
            new_position['Location'],
            new_position['StartDate'],
            new_position['Skills'],
            new_position['SalaryRange'],
            new_position['PositionType'],
            new_position['StartUpName'],
            new_position['StartUpID'],
            job_id
        )
        
        cursor = db.get_db().cursor()
        cursor.execute(query, params)
        
        if cursor.rowcount == 0:
            return_value = {
                'error': f'No position found with ID {job_id}'
            }
            return make_response(jsonify(return_value), 404)
        
        # Commit the transaction
        db.get_db().commit()
        
        return_value = {
            'message': f'Position {job_id} replaced successfully'
        }
        return make_response(jsonify(return_value), 200)
        
    except Exception as e:
        return_value = {
            'error': f'Error replacing position: {str(e)}'
        }
        return make_response(jsonify(return_value), 500)
