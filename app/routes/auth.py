from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth = Blueprint('auth', __name__)

auth_controller = AuthController()

auth.add_url_rule('/login', view_func=auth_controller.login,
                  methods=['GET', 'POST'])
auth.add_url_rule('/logout', view_func=auth_controller.logout)
