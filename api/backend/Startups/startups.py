### FILE FOR APPLICATIONS FROM THE REST API MATRIX
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