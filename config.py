"""
配置文件管理模块

该模块提供配置文件的管理功能，包括：
- 默认配置加载
- 用户配置文件的读取和合并
- 配置值的获取和设置
- 用户管理功能
- 配置验证和保存

配置文件格式为JSON，支持嵌套配置项。
"""
import os
import json
from typing import Dict, Any, List, Optional


class Config:
    """
    配置文件管理类
    
    该类负责管理应用程序的配置，包括：
    - 加载默认配置和用户配置
    - 配置项的获取和设置
    - 用户认证和管理
    - 配置文件的保存
    
    Attributes:
        config_file (str): 配置文件路径
        config (Dict[str, Any]): 当前配置数据
    """
    
    def __init__(self, config_file: str = "config.json"):
        """
        初始化配置管理器
        
        Args:
            config_file (str): 配置文件路径，默认为"config.json"
        """
        self.config_file = config_file
        self.config = self._load_default_config()
        self._load_config()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """
        加载默认配置
        
        Returns:
            Dict[str, Any]: 默认配置字典，包含所有必要的配置项
            
        默认配置包括：
        - server: 服务器相关配置（主机、端口、调试模式、密钥）
        - upload: 文件上传配置（上传文件夹、最大文件大小、允许的扩展名）
        - users: 用户列表（默认包含admin和user两个用户）
        - session: 会话配置（超时时间、安全设置）
        - dashboard: 仪表板配置（刷新间隔、显示选项）
        """
        return {
            "server": {
                "host": "0.0.0.0",
                "port": 9000,
                "debug": False,
                "secret_key": "your-secret-key-change-in-production"
            },
            "upload": {
                "folder": "uploads",
                "max_file_size": 5000,
                "allowed_extensions": [".txt", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".jpg", ".jpeg", ".png", ".gif", ".zip", ".rar", ".mp4", ".mp3", ".avi", ".mov"]
            },
            "users": [
                {
                    "username": "admin",
                    "password": "admin123",
                    "role": "admin"
                },
                {
                    "username": "user",
                    "password": "user123",
                    "role": "user"
                }
            ],
            "session": {
                "timeout": 3600,
                "secure": False
            },
            "dashboard": {
                "refresh_interval": 30000,
                "show_file_stats": True,
                "show_disk_usage": True
            }
        }
    
    def _load_config(self):
        """
        加载用户配置文件
        
        如果配置文件存在，则加载并合并到默认配置中。
        如果配置文件不存在或加载失败，则使用默认配置。
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                self._merge_config(user_config)
                print(f"配置文件加载成功: {self.config_file}")
            except Exception as e:
                print(f"加载配置文件失败: {e}")
                print("使用默认配置")
        else:
            print(f"配置文件不存在: {self.config_file}")
            print("使用默认配置")
    
    def _merge_config(self, user_config: Dict[str, Any]):
        """
        合并用户配置到默认配置
        
        Args:
            user_config (Dict[str, Any]): 用户提供的配置字典
            
        使用递归方式合并配置，用户配置会覆盖默认配置中的相同项。
        """
        def merge_dict(d1, d2):
            """
            递归合并字典
            
            Args:
                d1: 目标字典（将被修改）
                d2: 源字典（提供新值）
            """
            for key, value in d2.items():
                if key in d1 and isinstance(d1[key], dict) and isinstance(value, dict):
                    merge_dict(d1[key], value)
                else:
                    d1[key] = value
        
        merge_dict(self.config, user_config)
    
    def save_config(self):
        """
        保存配置到文件
        
        将当前配置保存到配置文件，使用JSON格式，缩进为2个空格。
        如果保存失败，会打印错误信息。
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"配置文件保存成功: {self.config_file}")
        except Exception as e:
            print(f"保存配置文件失败: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key (str): 配置键，支持点分隔符（如"server.port"）
            default (Any): 默认值，如果配置不存在则返回此值
            
        Returns:
            Any: 配置值，如果配置不存在则返回默认值
            
        Example:
            >>> config.get("server.port", 8080)
            9000
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        设置配置值
        
        Args:
            key (str): 配置键，支持点分隔符（如"server.port"）
            value (Any): 要设置的配置值
            
        Example:
            >>> config.set("server.port", 8080)
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def validate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        验证用户凭据
        
        Args:
            username (str): 用户名
            password (str): 密码
            
        Returns:
            Optional[Dict[str, Any]]: 如果验证成功返回用户信息，否则返回None
            
        Example:
            >>> config.validate_user("admin", "admin123")
            {'username': 'admin', 'password': 'admin123', 'role': 'admin'}
        """
        users = self.get('users', [])
        for user in users:
            if user.get('username') == username and user.get('password') == password:
                return user
        return None
    
    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        根据用户名获取用户信息
        
        Args:
            username (str): 用户名
            
        Returns:
            Optional[Dict[str, Any]]: 用户信息字典，如果用户不存在则返回None
            
        Example:
            >>> config.get_user_by_username("admin")
            {'username': 'admin', 'password': 'admin123', 'role': 'admin'}
        """
        users = self.get('users', [])
        for user in users:
            if user.get('username') == username:
                return user
        return None
    
    def add_user(self, username: str, password: str, role: str = "user"):
        """
        添加新用户
        
        Args:
            username (str): 用户名
            password (str): 密码
            role (str): 用户角色，默认为"user"
            
        Raises:
            ValueError: 如果用户名已存在
            
        Example:
            >>> config.add_user("newuser", "password123", "user")
        """
        users = self.get('users', [])
        
        # 检查用户是否已存在
        for user in users:
            if user.get('username') == username:
                raise ValueError(f"用户 {username} 已存在")
        
        users.append({
            "username": username,
            "password": password,
            "role": role
        })
        
        self.set('users', users)
        self.save_config()
    
    def remove_user(self, username: str):
        """
        删除用户
        
        Args:
            username (str): 要删除的用户名
            
        Note:
            如果用户名不存在，此方法不会报错，只是忽略删除操作
            
        Example:
            >>> config.remove_user("user")
        """
        users = self.get('users', [])
        users = [user for user in users if user.get('username') != username]
        
        self.set('users', users)
        self.save_config()
    
    def update_user_password(self, username: str, new_password: str):
        """
        更新用户密码
        
        Args:
            username (str): 用户名
            new_password (str): 新密码
            
        Raises:
            ValueError: 如果用户名不存在
            
        Example:
            >>> config.update_user_password("admin", "newpassword123")
        """
        users = self.get('users', [])
        
        for user in users:
            if user.get('username') == username:
                user['password'] = new_password
                self.set('users', users)
                self.save_config()
                return
        
        raise ValueError(f"用户 {username} 不存在")
    
    def get_server_config(self) -> Dict[str, Any]:
        """
        获取服务器配置
        
        Returns:
            Dict[str, Any]: 服务器配置字典，包含host、port等设置
            
        Example:
            >>> config.get_server_config()
            {'host': '127.0.0.1', 'port': 9000, 'debug': True}
        """
        return self.get('server', {})
    
    def get_upload_config(self) -> Dict[str, Any]:
        """
        获取上传配置
        
        Returns:
            Dict[str, Any]: 上传配置字典，包含allowed_extensions、max_file_size等设置
            
        Example:
            >>> config.get_upload_config()
            {'allowed_extensions': ['.txt', '.jpg', '.png'], 'max_file_size': 10485760}
        """
        return self.get('upload', {})
    
    def get_session_config(self) -> Dict[str, Any]:
        """
        获取会话配置
        
        Returns:
            Dict[str, Any]: 会话配置字典，包含secret_key、max_age等设置
            
        Example:
            >>> config.get_session_config()
            {'secret_key': 'your-secret-key', 'max_age': 3600}
        """
        return self.get('session', {})
    
    def get_dashboard_config(self) -> Dict[str, Any]:
        """
        获取仪表板配置
        
        Returns:
            Dict[str, Any]: 仪表板配置字典，包含enable_stats、refresh_interval等设置
            
        Example:
            >>> config.get_dashboard_config()
            {'enable_stats': True, 'refresh_interval': 300}
        """
        return self.get('dashboard', {})


# 全局配置实例
config = Config()
"""
全局配置实例，用于在整个应用程序中访问和管理配置

该实例在模块加载时自动创建，并加载默认配置和用户配置。
应用程序的其他模块可以直接导入并使用此实例。

Example:
    >>> from config import config
    >>> port = config.get('server.port')
    >>> print(f"服务器端口: {port}")
"""