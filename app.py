from flask import Flask,render_template, url_for, request, redirect,session,jsonify
from flask_session import Session
## for objectid in database
from bson.objectid import ObjectId
from conn import model_DB
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Configure DATABASE
admin = model_DB('orca_db','admins')


# Configure App
app = Flask(__name__, static_url_path='/static')

# Session Configure
app.config["SESSION_PERMANENT"] = True
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# INDEX ROUTES
@app.route('/')
def index():
    admin_name = session.get('admin_login')
    if admin_name:
        return render_template('admin/dashboard.html')
    else:
        return redirect('/admin/login')
    

#================ ADMIN CONFIGURATION ============================# 
# LOGIN ADMIN
@app.route('/admin/login' , methods=['GET', 'POST'])
def admin_login_page():
    if 'admin_name' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        admin_login = request.form['admin_login']
        password_login = request.form['password_login']
        
        # Empty Error Message
        if not admin_login or not password_login:
            return jsonify({'ok': False, 'message': 'Input fields are Required'})
         
        # Retrieve admin data from MongoDB
        hash_pass = admin.collection.find_one({'admin_email': admin_login})
        
        # Check if user exists and password matches
        if hash_pass and check_password_hash(hash_pass['password'], password_login):
            # Store admin's name in session
            session['admin_name'] = admin_login
            return redirect(url_for('dashboard'))
        else:
            return jsonify({'ok': False})
    return render_template('admin/login.html')

# CREATE SUPER ADMIN
@app.route('/super_admin/create',methods=['GET', 'POST'])
def store_super_admin():
    if 'admin_name' in session:
        if request.method == 'POST':
            admin_username = request.form['admin_username']
            admin_reg = request.form['admin_register']
            password_reg = request.form['password_register']

            # Check if provide an input
            if not admin_reg or not password_reg:
                return jsonify({'ok': False, 'message': 'Input field are required'})

            #HASH the Password
            hash_password = generate_password_hash(password_reg)
            
            # Count documents with 'admin' role
            admin_count = admin.collection.count_documents({'role': 'super admin'})

            # Check if there's only one admin
            if admin_count == 1:
                return jsonify({ 'ok': False, 'message': 'Super Admin Already Exists.'})
            else:
                #Layout Document
                document = {
                'admin_username': admin_username,
                'admin_email': admin_reg,
                'password': hash_password,
                'role': 'super admin',
                'created_at': datetime.now(),
                'updated_at' : datetime.now()
                }
                admin.insert_document(document)
                return jsonify({"ok": True, "message": "Super Admin Created"}), 200
        return render_template('admin/register.html')   
    return jsonify({'ok': False, 'message': 'Access Unauthorized'}), 401

ADMIN_TYPE = ['Admission Admin',"Registrar Admin", 'IT Admin', 'Cashier Admin']
# CREATE ADMINS
@app.route('/admin/create',methods=['GET', 'POST'])
def store_admin():
    if 'admin_name' in session:
        if request.method == 'POST':
            admin_username = request.form['admin_username']
            admin_reg = request.form['admin_register']
            password_reg = request.form['password_register']
            role = request.form['admin_type']

            # Check if provide an input
            if not admin_reg or not password_reg:
                return jsonify({'ok': False, 'message': 'Input field are required'})

            #HASH the Password
            hash_password = generate_password_hash(password_reg)
            
            email_exists = admin.collection.find_one({'admin_email': admin_reg})
            # Check if there's only one admin
            if email_exists:
                return jsonify({ 'ok': False, 'message': 'Email Already Exists.'})
            else:
                #Layout Document
                document = {
                'admin_username': admin_username,
                'admin_email': admin_reg,
                'password': hash_password,
                'role': role,
                'created_at': datetime.now(),
                'updated_at' : datetime.now()
                }
                admin.insert_document(document)
                return jsonify({"ok": True, "message": "New Admin Created"}), 201
        return render_template('admin/register.html', admin_type = ADMIN_TYPE)   
    return jsonify({'ok': False, 'message': 'Access Unauthorized'}), 401

# LOGOUT
@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('index'))
    

# ADMIN MODULES
@app.route('/dashboard')
def dashboard():
    if 'admin_name' in session:
        return render_template('admin/dashboard.html')
    return jsonify({"ok": False, 'message': 'Access Unauthorized'})



# USER MODULES
@app.route('/chatbot')
def chatbot():
    return render_template('users/index.html')

if __name__ == "__main__":
    app.run(debug=True)
