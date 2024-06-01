from flask import Blueprint
from app.controllers.file_controller import FileController

files = Blueprint('files', __name__)

file_controller = FileController()

files.add_url_rule('/', view_func=file_controller.home)
files.add_url_rule('/home', view_func=file_controller.home)
files.add_url_rule('/upload', view_func=file_controller.upload,
                   methods=['GET', 'POST'])
files.add_url_rule('/download/<filename>', view_func=file_controller.download)
files.add_url_rule('/delete/<filename>',
                   view_func=file_controller.delete_file, methods=['POST'])
