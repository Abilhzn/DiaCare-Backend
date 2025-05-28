from app import create_app, db
from flask_migrate import Migrate
import os

# Muat variabel lingkungan dari .env
from dotenv import load_dotenv
load_dotenv()

app = create_app(os.getenv('FLASK_ENV') or 'default')
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)