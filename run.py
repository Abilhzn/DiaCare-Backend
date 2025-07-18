import os
from app import create_app, db

app = create_app(os.getenv('FLASK_ENV') or 'development')

if __name__ == '__main__':
    app.run()