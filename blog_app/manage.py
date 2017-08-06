from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from blog_app.app import app
from blog_app.database import db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
