from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId
from functools import wraps
import jwt
import bcrypt
import os
from anthropic import Anthropic

app = Flask(__name__)

chat_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
conversation_history = []

# MongoDB connection
uri = "mongodb+srv://Unknown00x:bibhu%40123@cluster0.l1sa8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['theragene_db']

# MongoDB Collections
users = db.users
genetic_data = db.genetic_data
medical_records = db.medical_records
lifestyle_data = db.lifestyle_data
treatment_plans = db.treatment_plans

# Login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Public routes
@app.route('/')
def home():
    """Landing page route - serves index.html"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page route"""
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if request.method == 'POST':
        data = request.form
        user = db.users.find_one({'email': data['email']})
        
        if user and user['password'] == data['password']:  # In production, use proper password hashing
            session['user_id'] = str(user['_id'])
            return redirect(url_for('dashboard'))
        
        return render_template('index.html', error='Invalid credentials')
    
    return render_template('index.html')

# Protected routes (require login)
@app.route('/dashboard')
@login_required
def dashboard():
    """Main dashboard route"""
    user = db.users.find_one({'_id': session['user_id']})
    return render_template('dashboard.html', user=user)

@app.route('/profile')
@login_required
def profile():
    """User profile route"""
    user = db.users.find_one({'_id': session['user_id']})
    return render_template('profile.html', user=user)

@app.route('/treatment')
@login_required
def treatment():
    """Treatment page route"""
    return render_template('treatment.html')

# API routes
@app.route('/api/user-data')
@login_required
def get_user_data():
    """API route to get user data"""
    user = db.users.find_one({'_id': session['user_id']})
    return jsonify({
        'name': user['name'],
        'email': user['email'],
        # Add other user data as needed
    })

@app.route('/api/submit-genetic-data', methods=['POST'])
@login_required
def submit_genetic_data():
    """API route to submit genetic data"""
    data = request.json
    db.genetic_data.insert_one({
        'user_id': session['user_id'],
        'data': data
    })
    return jsonify({'message': 'Data submitted successfully'})

@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    return redirect(url_for('home'))

# User Authentication Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    if users.find_one({'email': data['email']}):
        return jsonify({'error': 'Email already registered'}), 400
    
    # Hash password
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    
    user = {
        'email': data['email'],
        'password': hashed_password,
        'name': data['name'],
        'created_at': datetime.utcnow()
    }
    
    users.insert_one(user)
    return jsonify({'message': 'User registered successfully'}), 201

# Data Input Routes
@app.route('/api/genetic-data', methods=['POST'])
def upload_genetic_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    genetic_info = {
        'user_id': ObjectId(session['user_id']),
        'dna_sequence': data['dna_sequence'],
        'genetic_markers': data['genetic_markers'],
        'uploaded_at': datetime.utcnow()
    }
    genetic_data.insert_one(genetic_info)
    return jsonify({'message': 'Genetic data uploaded successfully'})

@app.route('/api/medical-records', methods=['POST'])
def upload_medical_records():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    medical_info = {
        'user_id': ObjectId(session['user_id']),
        'conditions': data['conditions'],
        'medications': data['medications'],
        'allergies': data['allergies'],
        'uploaded_at': datetime.utcnow()
    }
    medical_records.insert_one(medical_info)
    return jsonify({'message': 'Medical records uploaded successfully'})

@app.route('/api/lifestyle-data', methods=['POST'])
def upload_lifestyle_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    lifestyle_info = {
        'user_id': ObjectId(session['user_id']),
        'diet': data['diet'],
        'exercise': data['exercise'],
        'sleep': data['sleep'],
        'stress_levels': data['stress_levels'],
        'uploaded_at': datetime.utcnow()
    }
    lifestyle_data.insert_one(lifestyle_info)
    return jsonify({'message': 'Lifestyle data uploaded successfully'})

# Analysis and Treatment Routes
@app.route('/api/analyze', methods=['GET'])
def analyze_health_data():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = ObjectId(session['user_id'])
    
    # Gather all user data
    genetic = genetic_data.find_one({'user_id': user_id})
    medical = medical_records.find_one({'user_id': user_id})
    lifestyle = lifestyle_data.find_one({'user_id': user_id})
    
    # Perform analysis (implement your AI logic here)
    analysis_results = {
        'disease_risks': analyze_disease_risks(genetic, medical, lifestyle),
        'drug_reactions': analyze_drug_reactions(genetic, medical),
        'lifestyle_recommendations': analyze_lifestyle(lifestyle)
    }
    
    return jsonify(analysis_results)

@app.route('/api/treatment-plan', methods=['GET'])
def get_treatment_plan():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    user_id = ObjectId(session['user_id'])
    plan = treatment_plans.find_one({'user_id': user_id})
    
    if not plan:
        return jsonify({'error': 'No treatment plan found'}), 404
    
    return jsonify(plan)

# Helper functions for analysis (implement your AI logic here)
def analyze_disease_risks(genetic, medical, lifestyle):
    # Implement disease risk analysis
    return {}

def analyze_drug_reactions(genetic, medical):
    # Implement drug reaction analysis
    return {}

def analyze_lifestyle(lifestyle):
    # Implement lifestyle analysis
    return {}

if __name__ == '__main__':
    app.run(debug=True)