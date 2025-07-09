from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define database models
class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.String(10), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    aadhar_number = db.Column(db.String(12), unique=True, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    biometric = db.Column(db.String(200), nullable=False)
    voter_id = db.Column(db.String(20), unique=True, nullable=False)

class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    aadhar = db.Column(db.String(12), unique=True, nullable=False)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    biometric = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<Officer {self.name}>"

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.String(20), nullable=False)
    vote = db.Column(db.String(100), nullable=False)

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Login Route (for simplicity, it's just a mock login)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # You can add authentication logic here
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Voter Registration Route
@app.route('/voter_registration', methods=['GET', 'POST'])
def voter_registration():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        father_name = request.form['father_name']
        aadhar_number = request.form['aadhar_number']
        address = request.form['address']
        biometric = request.form['biometric']  # Biometrics simulation for now
        voter_id = 'V' + str(db.session.query(Voter).count() + 1)  # Simple Voter ID generation

        new_voter = Voter(name=name, dob=dob, father_name=father_name, aadhar_number=aadhar_number,
                          address=address, biometric=biometric, voter_id=voter_id)
        db.session.add(new_voter)
        db.session.commit()

        return render_template('voter_registration_success.html', voter_id=voter_id)
    return render_template('voter_registration.html')

# Officer Registration Route
@app.route('/officer_registration', methods=['GET', 'POST'])
def officer_registration():
    if request.method == 'POST':
        name = request.form['name']
        aadhar = request.form['aadhar']
        employee_id = request.form['employee_id']
        biometric = request.form['biometric']  # Biometrics simulation for now

        new_officer = Officer(name=name, aadhar=aadhar, employee_id=employee_id, biometric=biometric)
        db.session.add(new_officer)
        db.session.commit()

        # Redirect to dashboard with a success message
        return redirect(url_for('dashboard', message="Officer Registered Successfully!"))
    return render_template('officer_registration.html')


@app.route('/officer_list')
def officer_list():
    officers = Officer.query.all()  # Query all officers from the database
    return render_template('officer_list.html', officers=officers)


# Voting Routes
@app.route('/voting_local', methods=['GET', 'POST'])
def voting_local():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        biometric = request.form['biometric']

        voter = Voter.query.filter_by(voter_id=voter_id).first()

        # Match biometric (simplified)
        if voter and voter.biometric == biometric:
            return redirect(url_for('voting_page', voter_id=voter_id))
        else:
            return "Error: Invalid credentials!"

    return render_template('voting_local.html')

@app.route('/voting_global', methods=['GET', 'POST'])
def voting_global():
    if request.method == 'POST':
        state = request.form['state']
        city = request.form['city']
        name = request.form['name']
        voter_id = request.form['voter_id']
        biometric = request.form['biometric']
        
        voter = Voter.query.filter_by(voter_id=voter_id).first()
        
        # Match biometric (simplified)
        if voter and voter.biometric == biometric:
            return redirect(url_for('voting_page', voter_id=voter_id))
        else:
            return "Error: Invalid credentials!"

    return render_template('voting_global.html')

# Voting Page Route
@app.route('/voting_page/<voter_id>', methods=['GET', 'POST'])
def voting_page(voter_id):
    if request.method == 'POST':
        vote = request.form['vote']
        new_vote = Vote(voter_id=voter_id, vote=vote)
        db.session.add(new_vote)
        db.session.commit()
        return "Successfully voted!"
    return render_template('voting_page.html')

@app.route('/support')
def support():
    return render_template('support.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
