from app.model.models import db, flask_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(flask_app, db)
manager = Manager(flask_app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    
