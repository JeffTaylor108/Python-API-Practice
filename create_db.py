from flask_api import app, db

# script that creates database
with app.app_context():
    db.create_all()