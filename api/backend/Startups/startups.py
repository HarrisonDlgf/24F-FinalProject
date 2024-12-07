### FILE FOR STARTUPS FROM THE REST API MATRIX
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db



#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
startups = Blueprint('startups', __name__)

# Making a request given the blueprint
# Returns all startups given an industry ID, and their relevant information

@startups.route('/Startups/<int:IndustryID>', methods=['GET'])
def get_startups_by_industry(IndustryID):
    cursor = db.get_db().cursor()
    query = ('''
    SELECT *
        FROM Startups
        WHERE IndustryID = %s
    ''')
    cursor.execute(query, IndustryID)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


# Create a new startup
@startups.route('/Startups', methods=['POST'])
def create_startup():
    try:
        current_app.logger.info('Processing startup creation request')
        startup_details = request.json
        
        # Ensure required fields are present
        required_fields = ['StartupName', 'IndustryID', 'Location', 'Description', 'ContactEmail']
        missing_fields = [field for field in required_fields if field not in startup_details]
        
        if missing_fields:
            return make_response(jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400)
        
        # Insert new startup into the database
        query = '''
        INSERT INTO Startups (StartupName, IndustryID, Location, Description, ContactEmail)
        VALUES (%s, %s, %s, %s, %s)
        '''
        params = (
            startup_details['StartupName'],
            startup_details['IndustryID'],
            startup_details['Location'],
            startup_details['Description'],
            startup_details['ContactEmail']
        )
        cursor = db.get_db().cursor()
        cursor.execute(query, params)
        db.get_db().commit()
        
        return make_response(jsonify({"message": "Startup created successfully"}), 201)
        
    except Exception as e:
        return make_response(jsonify({"error": f"Error creating startup: {str(e)}"}), 500)

# Update an existing startup by StartupID
@startups.route('/Startups/<int:StartupID>', methods=['PUT'])
def update_startup(StartupID):
    try:
        current_app.logger.info(f'Processing startup update request for ID {StartupID}')
        updates = request.json
        
        # Dynamically construct update query
        query_parts = []
        params = []
        
        if 'StartupName' in updates:
            query_parts.append('StartupName = %s')
            params.append(updates['StartupName'])
        if 'IndustryID' in updates:
            query_parts.append('IndustryID = %s')
            params.append(updates['IndustryID'])
        if 'Location' in updates:
            query_parts.append('Location = %s')
            params.append(updates['Location'])
        if 'Description' in updates:
            query_parts.append('Description = %s')
            params.append(updates['Description'])
        if 'ContactEmail' in updates:
            query_parts.append('ContactEmail = %s')
            params.append(updates['ContactEmail'])
        
        if not query_parts:
            return make_response(jsonify({"error": "No valid fields provided for update"}), 400)
        
        query = f'UPDATE Startups SET {", ".join(query_parts)} WHERE StartupID = %s'
        params.append(StartupID)
        
        # Execute the query
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(params))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({"error": f"No startup found with ID {StartupID}"}), 404)
        
        return make_response(jsonify({"message": f"Startup {StartupID} updated successfully"}), 200)
        
    except Exception as e:
        return make_response(jsonify({"error": f"Error updating startup: {str(e)}"}), 500)

# Delete an existing startup by StartupID
@startups.route('/Startups/<int:StartupID>', methods=['DELETE'])
def delete_startup(StartupID):
    try:
        current_app.logger.info(f'Processing startup deletion request for ID {StartupID}')
        cursor = db.get_db().cursor()
        
        query = 'DELETE FROM Startups WHERE StartupID = %s'
        cursor.execute(query, (StartupID,))
        db.get_db().commit()
        
        if cursor.rowcount == 0:
            return make_response(jsonify({"error": f"No startup found with ID {StartupID}"}), 404)
        
        return make_response(jsonify({"message": f"Startup {StartupID} deleted successfully"}), 200)
        
    except Exception as e:
        return make_response(jsonify({"error": f"Error deleting startup: {str(e)}"}), 500)

# Search for startups with optional filters
@startups.route('/Startups/search', methods=['GET'])
def search_startups():
    try:
        current_app.logger.info('Processing startup search request')
        
        # Get filter parameters from the query string
        filters = {
            'StartupName': request.args.get('StartupName'),
            'IndustryID': request.args.get('IndustryID'),
            'Location': request.args.get('Location'),
            'Description': request.args.get('Description'),
        }
        
        # Start with the base query
        query = 'SELECT * FROM Startups WHERE 1=1'
        params = []
        
        # Dynamically add filters
        if filters['StartupName']:
            query += ' AND StartupName LIKE %s'
            params.append(f'%{filters["StartupName"]}%')
        
        if filters['IndustryID']:
            query += ' AND IndustryID = %s'
            params.append(filters['IndustryID'])
        
        if filters['Location']:
            query += ' AND Location LIKE %s'
            params.append(f'%{filters["Location"]}%')
        
        if filters['Description']:
            query += ' AND Description LIKE %s'
            params.append(f'%{filters["Description"]}%')
        
        # Execute the query
        cursor = db.get_db().cursor()
        cursor.execute(query, tuple(params))
        theData = cursor.fetchall()
        
        return make_response(jsonify(theData), 200)
        
    except Exception as e:
        return make_response(jsonify({"error": f"Error searching startups: {str(e)}"}), 500)

@startups.route('/<int:startup_id>', methods=['GET'])
def get_startup(startup_id):
    try:
        cursor = db.get_db().cursor()
        query = 'SELECT * FROM Startups WHERE StartupID = %s'
        cursor.execute(query, (startup_id,))
        startup = cursor.fetchone()
        
        if startup:
            return make_response(jsonify(startup), 200)
        else:
            return make_response(jsonify({"error": "Startup not found"}), 404)
            
    except Exception as e:
        current_app.logger.warning(f"Error in get_startup: {str(e)}")
        return jsonify({
            "error": str(e),
            "message": "Failed to fetch startup"
        }), 500

