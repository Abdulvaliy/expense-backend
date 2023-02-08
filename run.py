from app import app, db
from app.models import User


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    # manager.run()
    app.run(debug=True)

# python run.py

# to make changes db
    # python run.py db migrate
    # python run.py db upgrade
