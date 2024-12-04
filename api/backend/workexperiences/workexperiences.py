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
workexperiences = Blueprint('work experiences', __name__)


#------------------------------------------------------------
# Get all workexperiences from the system
@workexperiences.route('/workexperiences', methods=['GET'])
def get_workexperiences():

    cursor = db.get_db().cursor()
    cursor.execute('''SELECT StudentID, StartDate, EndDate,
                    JobID, Feedback FROM workexperiences
    ''')
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response