"""
文件服务器主应用
重构版本：模块化、高性能、支持用户认证和可视化大屏幕
"""
import os
import json
import re
from flask import Flask, request, jsonify, render_template, send_file, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from config import config
from utils import FileUtils, QRCodeUtils, ValidationUtils
from auth import login_required, admin_required, AuthManager
from version import get_version, get_version_description, get_release_date

app = Flask(__name__)

# 从配置中加载设置
server_config = config.get_server_config()
upload_config = config.get_upload_config()
session_config = config.get_session_config()

def parse_file_size(size_str):
    """解析易懂的文件大小表示（如2GB、4MB、500KB等）"""
    if isinstance(size_str, (int, float)):
        # 如果是数字，默认单位为MB
        return int(size_str * 1024 * 1024)
    
    if isinstance(size_str, str):
        size_str = size_str.strip().upper()
        
        # 提取数字和单位
        import re
        match = re.match(r'^(\d+(?:\.\d+)?)\s*([KMGTP]?B?)$', size_str)
        if not match:
            raise ValueError(f"无效的文件大小格式: {size_str}")
        
        size_value = float(match.group(1))
        unit = match.group(2)
        
        # 根据单位转换为字节
        unit_multipliers = {
            'B': 1,
            'KB': 1024,
            'MB': 1024 * 1024,
            'GB': 1024 * 1024 * 1024,
            'TB': 1024 * 1024 * 1024 * 1024,
            'K': 1024,
            'M': 1024 * 1024,
            'G': 1024 * 1024 * 1024,
            'T': 1024 * 1024 * 1024 * 1024,
            '': 1024 * 1024  # 默认单位为MB
        }
        
        multiplier = unit_multipliers.get(unit)
        if multiplier is None:
            raise ValueError(f"不支持的单位: {unit}")
        
        return int(size_value * multiplier)
    
    raise ValueError(f"不支持的文件大小类型: {type(size_str)}")

app.secret_key = server_config.get('secret_key', 'your-secret-key-change-in-production')

# 设置UTF-8编码配置
app.config['JSON_AS_ASCII'] = False  # 确保JSON响应使用UTF-8
app.config['ENCODING'] = 'utf-8'    # 设置默认编码

# 处理上传文件夹路径，支持 ~ 扩展
upload_folder = upload_config.get('folder', 'uploads')
if upload_folder.startswith('~'):
    upload_folder = os.path.expanduser(upload_folder)
app.config['UPLOAD_FOLDER'] = os.path.abspath(upload_folder)
app.config['MAX_CONTENT_LENGTH'] = parse_file_size(upload_config.get('max_file_size', '5000MB'))

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 初始化认证管理器
AuthManager.initialize(config)

# 服务器信息
server_host = server_config.get('host', '0.0.0.0')
server_port = server_config.get('port', 9000)
server_address = f"http://{FileUtils.get_local_ip()}:{server_port}"


# 错误处理
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', 
                         error_code=404,
                         error_message='页面未找到'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', 
                         error_code=500,
                         error_message='服务器内部错误'), 500

@app.errorhandler(413)
def too_large_error(error):
    return render_template('error.html', 
                         error_code=413,
                         error_message='文件太大'), 413

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('error.html', 
                         error_code=403,
                         error_message='访问被拒绝'), 403


# 路由定义
@app.route('/')
@login_required
def index():
    """首页 - 可视化大屏幕"""
    try:
        # 获取磁盘使用情况
        disk_usage = FileUtils.get_disk_usage(app.config['UPLOAD_FOLDER'])
        
        # 获取文件统计信息
        file_stats = FileUtils.get_file_stats(app.config['UPLOAD_FOLDER'])
        # 添加上传路径信息
        file_stats['upload_folder'] = app.config['UPLOAD_FOLDER']
        
        # 获取版本信息
        version_info = {
            'version': get_version(),
            'description': get_version_description(),
            'release_date': get_release_date()
        }
        
        return render_template('dashboard.html', 
                             disk_usage=disk_usage,
                             file_stats=file_stats,
                             address=server_address,
                             current_user=session.get('username'),
                             version_info=version_info)
    except Exception as e:
        return render_template('error.html', 
                             error_code=500,
                             error_message=f"获取系统信息失败: {str(e)}"), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    # 如果用户已登录，重定向到首页
    if session.get('logged_in'):
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('请输入用户名和密码！', 'error')
        elif AuthManager.authenticate(username, password):
            AuthManager.login(username)
            flash('登录成功！', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('用户名或密码错误！', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """用户登出"""
    AuthManager.logout()
    flash('已成功登出！', 'success')
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET'])
@login_required
def upload_file():
    """文件上传页面"""
    # 计算前端需要的最大文件大小（MB单位）
    max_filesize_mb = app.config['MAX_CONTENT_LENGTH'] / (1024 * 1024)
    
    return render_template('upload.html', 
                          address=server_address,
                          max_content_length=app.config['MAX_CONTENT_LENGTH'],
                          max_filesize_mb=max_filesize_mb,
                          allowed_extensions=upload_config.get('allowed_extensions', []),
                          current_user=session.get('username'))

@app.route('/upload', methods=['POST'])
@login_required
def handle_upload():
    """处理文件上传"""
    try:
        # 获取当前路径参数（从文件列表页面传递）
        current_path = request.form.get('current_path', '').strip()
        
        # 检查是否有文件上传
        file = None
        
        # 查找文件字段
        for field_name in request.files.keys():
            if field_name.startswith('file'):
                file = request.files[field_name]
                break
        
        # 如果没有找到，尝试常见的字段名
        if not file:
            for field_name in ['file', 'files[]', 'dzfile', 'file[0]']:
                if field_name in request.files:
                    file = request.files[field_name]
                    break
        
        if not file:
            return jsonify({'error': '请选择文件'}), 400
        
        # 检查文件名是否为空
        if not file or file.filename == '' or file.filename is None:
            return jsonify({'error': '请选择有效的文件'}), 400
        
        # 验证文件类型
        allowed_extensions = upload_config.get('allowed_extensions', [])
        if not ValidationUtils.validate_file_extension(file.filename, allowed_extensions):
            return jsonify({'error': f'不支持的文件类型。支持的类型: {", ".join(allowed_extensions)}'}), 400
        
        # 验证文件大小（前端验证可能被绕过）
        file.seek(0, 2)  # 移动到文件末尾
        file_size = file.tell()
        file.seek(0)  # 重置文件指针
        
        max_size = app.config['MAX_CONTENT_LENGTH']
        if file_size > max_size:
            max_size_mb = max_size / (1024 * 1024)
            file_size_mb = file_size / (1024 * 1024)
            return jsonify({
                'error': f'文件大小超出限制',
                'details': f'文件大小: {file_size_mb:.2f}MB, 最大限制: {max_size_mb:.2f}MB'
            }), 413
        
        # 保持原始文件名，正确处理中文文件名
        original_filename = file.filename
        
        # 检查是否为中文文件名，如果是则进行特殊处理
        try:
            # 尝试使用UTF-8编码
            original_filename.encode('utf-8')
            # 如果文件名包含非ASCII字符，保留原始文件名但进行安全处理
            if any(ord(char) > 127 for char in original_filename):
                # 中文文件名：保留原始文件名，但替换危险字符
                safe_filename = re.sub(r'[\\/:"*?<>|]', '_', original_filename)
            else:
                # 英文文件名：使用secure_filename
                safe_filename = secure_filename(original_filename)
        except UnicodeEncodeError:
            # 如果UTF-8编码失败，使用安全文件名
            safe_filename = secure_filename(original_filename)
        
        # 如果安全处理后文件名为空，使用原始文件名（进行基本清理）
        if not safe_filename:
            safe_filename = re.sub(r'[^\w\d\.\-]', '_', original_filename)
        
        # 构建文件路径，考虑当前浏览路径
        if current_path:
            # 安全检查当前路径
            target_folder = os.path.join(app.config['UPLOAD_FOLDER'], current_path)
            if not FileUtils.is_safe_path(app.config['UPLOAD_FOLDER'], target_folder):
                return jsonify({'error': '访问路径不安全'}), 403
            
            # 确保目标文件夹存在
            os.makedirs(target_folder, exist_ok=True)
            file_path = os.path.join(target_folder, safe_filename)
        else:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        
        # 检查文件是否已存在，如果存在则生成唯一文件名
        counter = 1
        name, ext = os.path.splitext(safe_filename)
        while os.path.exists(file_path):
            safe_filename = f"{name}_{counter}{ext}"
            if current_path:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], current_path, safe_filename)
            else:
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            counter += 1
        
        # 保存文件
        file.save(file_path)
        
        return jsonify({
            'success': True,
            'message': f'文件 {safe_filename} 上传成功！',
            'filename': safe_filename,
            'file_size': file_size
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': '文件上传失败',
            'details': str(e)
        }), 500


@app.route('/files')
@app.route('/files/<path:path>')
@login_required
def file_list(path=''):
    """文件列表页面"""
    try:
        # 正确处理路径，确保没有多余的斜杠
        if path:
            current_path = os.path.join(app.config['UPLOAD_FOLDER'], path)
        else:
            current_path = app.config['UPLOAD_FOLDER']
        
        # 规范化路径，移除多余的斜杠
        current_path = os.path.normpath(current_path)
        
        # 安全检查
        if not FileUtils.is_safe_path(app.config['UPLOAD_FOLDER'], current_path):
            return render_template('error.html', 
                                 error_code=403,
                                 error_message='访问路径不安全'), 403
        
        files_and_dirs = FileUtils.get_files_and_dirs(current_path, app.config['UPLOAD_FOLDER'])
        
        return render_template('file_list.html',
                             files_and_dirs=files_and_dirs,
                             current_path=current_path,
                             upload_folder=app.config['UPLOAD_FOLDER'],
                             address=server_address,
                             current_user=session.get('username'))
    except Exception as e:
        return render_template('error.html', 
                             error_code=500,
                             error_message=f'获取文件列表失败: {str(e)}'), 500


@app.route('/download/<path:filepath>')
@login_required
def download(filepath):
    """文件下载/预览"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filepath)
        file_path = os.path.normpath(file_path)
        
        # 安全检查
        if not FileUtils.is_safe_path(app.config['UPLOAD_FOLDER'], file_path):
            return render_template('error.html', 
                                 error_code=403,
                                 error_message='访问路径不安全'), 403
        
        if not os.path.exists(file_path):
            return render_template('error.html', 
                                 error_code=404,
                                 error_message='文件不存在'), 404
        
        # 检查是否为文件夹
        if os.path.isdir(file_path):
            return render_template('error.html', 
                                 error_code=400,
                                 error_message='下载路径指向文件夹，请选择具体文件'), 400
        
        as_attachment = request.args.get('as_attachment', 'true').lower() == 'true'
        
        # 直接返回文件，让浏览器处理文件名编码
        return send_file(file_path, as_attachment=as_attachment)
            
    except Exception as e:
        return render_template('error.html', 
                             error_code=500,
                             error_message=f'文件操作失败: {str(e)}'), 500


@app.route('/delete/<path:filename>', methods=['DELETE'])
@login_required
def delete_file(filename):
    """删除文件"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # 安全检查
        if not FileUtils.is_safe_path(app.config['UPLOAD_FOLDER'], file_path):
            return jsonify({'error': '访问路径不安全'}), 403
        
        if not os.path.exists(file_path):
            return jsonify({'error': '文件不存在'}), 404
        
        # 安全删除文件
        FileUtils.safe_delete(file_path)
        return jsonify({'message': '文件删除成功'}), 200
    except Exception as e:
        return jsonify({'error': f'删除文件失败: {str(e)}'}), 500


@app.route('/create_folder', methods=['POST'])
@login_required
def create_folder():
    """创建文件夹"""
    try:
        data = request.get_json()
        if not data or 'folder_name' not in data:
            return jsonify({'error': '文件夹名不能为空'}), 400
        
        folder_name = data['folder_name'].strip()
        if not folder_name:
            return jsonify({'error': '文件夹名不能为空'}), 400
        
        # 获取当前路径（如果有）
        current_path = data.get('current_path', '')
        
        # 构建完整路径
        if current_path:
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], current_path, folder_name)
        else:
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        
        # 安全检查
        if not FileUtils.is_safe_path(app.config['UPLOAD_FOLDER'], full_path):
            return jsonify({'error': '访问路径不安全'}), 403
        
        # 创建文件夹
        os.makedirs(full_path, exist_ok=True)
        
        return jsonify({
            'success': True,
            'message': f'文件夹 "{folder_name}" 创建成功！'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'创建文件夹失败: {str(e)}'}), 500


@app.route('/api/stats')
@login_required
def api_stats():
    """API接口：获取系统统计信息"""
    try:
        disk_usage = FileUtils.get_disk_usage(app.config['UPLOAD_FOLDER'])
        file_stats = FileUtils.get_file_stats(app.config['UPLOAD_FOLDER'])
        
        return jsonify({
            'disk_usage': disk_usage,
            'file_stats': file_stats,
            'server_info': {
                'address': server_address,
                'upload_folder': app.config['UPLOAD_FOLDER'],
                'max_file_size': app.config['MAX_CONTENT_LENGTH']
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/file_type_stats')
@login_required
def api_file_type_stats():
    """获取文件类型统计信息"""
    try:
        stats = FileUtils.get_file_type_stats(app.config['UPLOAD_FOLDER'])
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/folder_size_stats')
@login_required
def api_folder_size_stats():
    """获取文件夹大小统计信息"""
    try:
        stats = FileUtils.get_folder_size_stats(app.config['UPLOAD_FOLDER'])
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/preview', methods=['POST'])
@login_required
def api_preview():
    """POST接口：获取文件预览地址"""
    try:
        data = request.get_json()
        if not data or 'filepath' not in data:
            return jsonify({
                'success': False,
                'error': '文件路径不能为空'
            }), 400
        
        filepath = data['filepath'].strip()
        if not filepath:
            return jsonify({
                'success': False,
                'error': '文件路径不能为空'
            }), 400
        
        # 构建完整路径
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filepath)
        file_path = os.path.normpath(file_path)
        
        # 安全检查
        if not FileUtils.is_safe_path(app.config['UPLOAD_FOLDER'], file_path):
            return jsonify({
                'success': False,
                'error': '访问路径不安全'
            }), 403
        
        if not os.path.exists(file_path):
            return jsonify({
                'success': False,
                'error': '文件不存在'
            }), 404
        
        # 检查是否为文件夹
        if os.path.isdir(file_path):
            return jsonify({
                'success': False,
                'error': '路径指向文件夹，请选择具体文件'
            }), 400
        
        # 生成安全的预览URL（使用临时token或会话验证）
        # 这里直接返回文件路径，前端可以构建预览URL
        preview_url = f"/download/{filepath}?as_attachment=false"
        
        return jsonify({
            'success': True,
            'preview_url': preview_url,
            'filepath': filepath
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'获取预览地址失败: {str(e)}'
        }), 500


if __name__ == '__main__':
    debug = server_config.get('debug', False)
    
    print(f"=== 文件服务器启动信息 ===")
    print(f"服务器地址: {server_address}")
    print(f"上传目录: {app.config['UPLOAD_FOLDER']}")
    print(f"最大文件大小: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024)} MB")
    print(f"调试模式: {debug}")
    print("=== 默认用户账号 ===")
    users = config.get('users', [])
    for user in users:
        print(f"用户名: {user.get('username')} | 密码: {user.get('password')} | 角色: {user.get('role')}")
    print("========================")
    
    # 显示二维码
    QRCodeUtils.generate_qrcode(server_address)
    
    app.run(host=server_host, port=server_port, debug=debug)
