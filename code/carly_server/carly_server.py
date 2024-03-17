from flask import Flask, request, jsonify
from helper import execute_login, execute_change_password, execute_change_language
from authorizer import token_required, require_version

app = Flask(__name__)



@app.route('/login', methods=['POST'])
@require_version
def login():
    """_summary_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        data = request.get_json()

        if not (data and 'email' in data and 'password' in data):
            return jsonify({"error": "Missing email or password in request body"}), 400

        email = data.get('email')
        password = data.get('password')
        
        # Verify user credentials
        user = execute_login(email, password)

        if user:
            # Return customer_id and language on successful login
            return jsonify(user), 200
        else:
            # Return an error message for invalid credentials
            return jsonify({"error": "Invalid email or password"}), 400



@app.route('/changepassword', methods=['POST'])
@require_version
@token_required
def change_password():

    """_summary_

    Returns:
        _type_: _description_
    """
    
    data = request.get_json()
 
    if not (data and 'customer_id' in data and 'email' in data and 'newpassword' in data):
        return jsonify({"error": "Please provide email, customer_id and new password"}), 400
    
    customer_id = data.get('customer_id')
    email = data.get('email')
    newpassword = data.get('newpassword')
    updatefield = {'password': newpassword}

    result = execute_change_password(customer_id, email, updatefield)
    if(result):
        return jsonify({"success": "password has been changed successfully"}), 200
    else:
        return jsonify({"error": "password updated failed, please check credentials"}), 400


@app.route('/changelanguage', methods=['POST'])
@require_version
@token_required
def change_language():

    """_summary_

    Returns:
        _type_: _description_
    """
    
    data = request.get_json()
 
    if not (data and 'customer_id' in data and 'email' in data and 'language' in data):
        return jsonify({"error": "Please provide email, customer_id and langauge"}), 400
    
    if (data.get('language') not in ['de', 'en']):
        return jsonify({"error": "Language not supported, please select german or english"}), 400
    
    customer_id = data.get('customer_id')
    email = data.get('email')
    language = data.get('language')
    updatefield = {'language': language}

    result = execute_change_language(customer_id, email, updatefield)
    if(result):
        return jsonify({"success": "language has been changed successfully"}), 200
    else:
        return jsonify({"error": "language updated failed, Please check credentials"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port='8890')