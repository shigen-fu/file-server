"""
用户认证模块
"""
from functools import wraps
from flask import session, redirect, url_for, request, flash
import config


def login_required(f):
    """登录装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """管理员权限装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login', next=request.url))
        
        # 检查是否为管理员（这里简单实现，可根据需要扩展）
        if session.get('user_id') != 'admin':
            flash('需要管理员权限', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function


class AuthManager:
    """认证管理器"""
    
    @staticmethod
    def initialize(config_manager):
        """初始化认证管理器"""
        # 这里可以添加初始化逻辑，比如加载用户配置等
        pass
    
    @staticmethod
    def authenticate(username: str, password: str) -> bool:
        """验证用户凭据"""
        return config.config.validate_user(username, password)
    
    @staticmethod
    def login(username: str):
        """登录用户"""
        session['user_id'] = username
        session['username'] = username
        session['logged_in'] = True
    
    @staticmethod
    def logout():
        """登出用户"""
        session.clear()
    
    @staticmethod
    def get_current_user() -> str:
        """获取当前登录用户"""
        return session.get('user_id', 'guest')
    
    @staticmethod
    def is_logged_in() -> bool:
        """检查用户是否已登录"""
        return session.get('logged_in', False)
    
    @staticmethod
    def is_admin() -> bool:
        """检查是否为管理员"""
        return session.get('user_id') == 'admin'