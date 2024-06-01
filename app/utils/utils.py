import logging
import os
from functools import wraps

import yaml
from flask import redirect, session, url_for


def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


def verify_user(username, password):
    config = load_config('app/config.yaml')
    users = config['users']
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True
    return False


def configure_logging(level, log_format):
    logging.basicConfig(level=getattr(logging, level), format=log_format)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def get_file_size(filepath):
    size = os.path.getsize(filepath)
    return size


def format_file_size(size):
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    else:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"
