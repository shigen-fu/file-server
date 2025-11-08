"""
工具函数模块
"""
import os
import socket
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional


class FileUtils:
    """文件操作工具类"""
    
    @staticmethod
    def get_local_ip() -> str:
        """获取本地IP地址"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        except Exception:
            return "127.0.0.1"
    
    @staticmethod
    def format_size(size: int) -> str:
        """格式化文件大小"""
        for unit in ["B", "KB", "MB", "GB"]:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    @staticmethod
    def format_time(timestamp: float) -> str:
        """格式化时间戳"""
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_disk_usage(path: str) -> Dict[str, Any]:
        """获取磁盘使用情况"""
        try:
            total, used, free = shutil.disk_usage(path)
            return {
                "total": total,
                "used": used,
                "free": free,
                "total_formatted": FileUtils.format_size(total),
                "used_formatted": FileUtils.format_size(used),
                "free_formatted": FileUtils.format_size(free),
                "usage_percent": round((used / total) * 100, 2)
            }
        except Exception as e:
            return {
                "total": 0,
                "used": 0,
                "free": 0,
                "total_formatted": "0 B",
                "used_formatted": "0 B",
                "free_formatted": "0 B",
                "usage_percent": 0,
                "error": str(e)
            }
    
    @staticmethod
    def get_file_stats(path: str) -> Dict[str, Any]:
        """获取文件统计信息"""
        file_count = 0
        dir_count = 0
        total_size = 0
        
        try:
            for root, dirs, files in os.walk(path):
                dir_count += len(dirs)
                file_count += len(files)
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        total_size += os.path.getsize(file_path)
                    except OSError:
                        continue
        except OSError:
            pass
        
        return {
            "file_count": file_count,
            "dir_count": dir_count,
            "total_size": total_size,
            "total_size_formatted": FileUtils.format_size(total_size)
        }
    
    @staticmethod
    def get_file_type_stats(path: str) -> Dict[str, Any]:
        """获取文件类型统计信息"""
        file_type_stats = {}
        total_size = 0
        
        try:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        total_size += file_size
                        
                        # 获取文件扩展名
                        _, ext = os.path.splitext(file)
                        ext = ext.lower() if ext else '无扩展名'
                        
                        # 分类文件类型
                        file_type = '其他'
                        if ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg']:
                            file_type = '图片'
                        elif ext in ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']:
                            file_type = '视频'
                        elif ext in ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma']:
                            file_type = '音频'
                        elif ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt']:
                            file_type = '文档'
                        elif ext in ['.zip', '.rar', '.7z', '.tar', '.gz']:
                            file_type = '压缩包'
                        elif ext in ['.exe', '.dmg', '.pkg', '.deb', '.rpm']:
                            file_type = '应用程序'
                        elif ext in ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css', '.php']:
                            file_type = '代码文件'
                        
                        # 统计文件类型
                        if file_type not in file_type_stats:
                            file_type_stats[file_type] = {
                                'count': 0,
                                'size': 0,
                                'size_formatted': '0 B'
                            }
                        
                        file_type_stats[file_type]['count'] += 1
                        file_type_stats[file_type]['size'] += file_size
                        file_type_stats[file_type]['size_formatted'] = FileUtils.format_size(file_type_stats[file_type]['size'])
                        
                    except OSError:
                        continue
        except OSError:
            pass
        
        # 计算百分比
        for file_type in file_type_stats:
            if total_size > 0:
                percentage = round((file_type_stats[file_type]['size'] / total_size) * 100, 2)
            else:
                percentage = 0
            file_type_stats[file_type]['percentage'] = percentage
        
        return {
            'file_type_stats': file_type_stats,
            'total_size': total_size,
            'total_size_formatted': FileUtils.format_size(total_size)
        }
    
    @staticmethod
    def get_folder_size_stats(path: str) -> Dict[str, Any]:
        """获取文件夹大小统计信息"""
        folder_stats = {}
        
        try:
            # 获取直接子目录
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    # 计算文件夹大小
                    folder_size = 0
                    try:
                        for root, dirs, files in os.walk(item_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                try:
                                    folder_size += os.path.getsize(file_path)
                                except OSError:
                                    continue
                    except OSError:
                        continue
                    
                    folder_stats[item] = {
                        'size': folder_size,
                        'size_formatted': FileUtils.format_size(folder_size)
                    }
        except OSError:
            pass
        
        # 按大小排序
        sorted_folders = sorted(folder_stats.items(), key=lambda x: x[1]['size'], reverse=True)
        
        return {
            'folder_stats': dict(sorted_folders[:10]),  # 只返回前10个最大的文件夹
            'total_folders': len(folder_stats)
        }
    
    @staticmethod
    def get_files_and_dirs(path: str, base_path: str = "") -> List[Dict[str, Any]]:
        """获取目录下的文件和文件夹列表"""
        items = []
        
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                
                try:
                    item_type = "file" if os.path.isfile(item_path) else "dir"
                    
                    # 计算相对于base_path的相对路径
                    relative_path = ""
                    if base_path:
                        # 确保路径规范化
                        base_path = os.path.normpath(base_path)
                        item_path_norm = os.path.normpath(item_path)
                        
                        # 计算相对路径
                        if item_path_norm.startswith(base_path):
                            # 对于文件，计算文件相对于base_path的完整路径
                            if item_type == "file":
                                relative_path = os.path.relpath(item_path_norm, base_path)
                            # 对于目录，计算目录相对于base_path的路径
                            else:
                                relative_path = os.path.relpath(item_path_norm, base_path)
                    
                    # 文件大小计算增加错误处理
                    item_size = None
                    if item_type == "file":
                        try:
                            file_size = os.path.getsize(item_path)
                            item_size = FileUtils.format_size(file_size)
                        except (OSError, ValueError):
                            # 如果无法获取文件大小，设置为未知
                            item_size = "未知"
                    
                    # 权限和时间信息也增加错误处理
                    try:
                        item_permissions = oct(os.stat(item_path).st_mode)[-3:]
                        item_create_time = FileUtils.format_time(os.path.getctime(item_path))
                        item_modify_time = FileUtils.format_time(os.path.getmtime(item_path))
                    except (OSError, ValueError):
                        item_permissions = "---"
                        item_create_time = "未知"
                        item_modify_time = "未知"
                    
                    items.append({
                        "name": item,
                        "type": item_type,
                        "size": item_size,
                        "permissions": item_permissions,
                        "create_time": item_create_time,
                        "modify_time": item_modify_time,
                        "relative_path": relative_path,
                    })
                except OSError:
                    # 跳过无法访问的文件
                    continue
            
            # 按修改时间排序
            return sorted(items, key=lambda x: x["modify_time"], reverse=True)
        except OSError:
            return []
    
    @staticmethod
    def safe_delete(path: str) -> bool:
        """安全删除文件或目录"""
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            return True
        except Exception:
            return False
    
    @staticmethod
    def is_safe_path(base_path: str, target_path: str) -> bool:
        """检查路径是否安全（防止目录遍历攻击）"""
        try:
            base_path = os.path.abspath(base_path)
            target_path = os.path.abspath(target_path)
            
            # 如果两个路径完全相同，直接返回True
            if base_path == target_path:
                return True
            
            # 确保base_path以路径分隔符结尾，避免部分匹配问题
            if not base_path.endswith(os.path.sep):
                base_path += os.path.sep
                
            # 确保target_path也以路径分隔符结尾，用于目录比较
            if not target_path.endswith(os.path.sep):
                target_path += os.path.sep
                
            return target_path.startswith(base_path)
        except Exception:
            return False


class QRCodeUtils:
    """二维码工具类"""
    
    @staticmethod
    def generate_qrcode(address: str) -> None:
        """生成二维码（终端显示）"""
        try:
            import qrcode_terminal
            qrcode_terminal.draw(address, version=1)
        except ImportError:
            print("qrcode_terminal 未安装，跳过二维码生成")


class ValidationUtils:
    """验证工具类"""
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
        """验证文件扩展名"""
        _, ext = os.path.splitext(filename)
        return ext.lower() in allowed_extensions
    
    @staticmethod
    def validate_file_size(file_size: int, max_size: int) -> bool:
        """验证文件大小"""
        return file_size <= max_size