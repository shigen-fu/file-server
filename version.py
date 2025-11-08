"""
项目版本管理模块

该模块定义了项目的版本号，遵循语义化版本规范（Semantic Versioning）。
"""

# 项目版本号 - 遵循语义化版本规范 (MAJOR.MINOR.PATCH)
__version__ = "2.0.0"

# 版本信息元组
VERSION_INFO = (1, 0, 0)

# 版本描述
VERSION_DESCRIPTION = "file-server v2.0.0 - 稳定版本"

# 版本发布日期
RELEASE_DATE = "2024-12-19"

# 版本变更日志
CHANGELOG = {
    "2.0.0": [
        "初始稳定版本发布",
        "实现完整的文件上传下载功能",
        "添加用户认证和权限管理",
        "实现文件统计和仪表板功能",
        "支持Docker容器化部署",
        "优化前端界面和用户体验"
    ]
}

def get_version() -> str:
    """
    获取项目版本号
    
    Returns:
        str: 项目版本号字符串
    """
    return __version__

def get_version_info() -> tuple:
    """
    获取版本信息元组
    
    Returns:
        tuple: (主版本号, 次版本号, 修订号)
    """
    return VERSION_INFO

def get_version_description() -> str:
    """
    获取版本描述
    
    Returns:
        str: 版本描述信息
    """
    return VERSION_DESCRIPTION

def get_release_date() -> str:
    """
    获取版本发布日期
    
    Returns:
        str: 发布日期字符串
    """
    return RELEASE_DATE

def get_changelog(version: str = None) -> list:
    """
    获取版本变更日志
    
    Args:
        version (str): 指定版本号，如果为None则返回最新版本的变更日志
        
    Returns:
        list: 变更日志列表
    """
    if version is None:
        version = __version__
    return CHANGELOG.get(version, [])