from flask import Flask
from flasgger import Swagger
from routes.home import home_bp
from routes.user import user_bp
from models.user import db, User

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(user_bp)

swagger = Swagger(app)

if __name__ == "__main__":
    if db.is_closed():
        db.connect()

    db.create_tables([User], safe=True)
    app.run(debug=True)