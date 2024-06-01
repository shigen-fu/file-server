from flask import render_template, request, redirect, url_for, flash, send_from_directory, current_app, session
import os
import time
from app.utils.utils import login_required, get_file_size, format_file_size


class FileController:
    def __init__(self):
        self.home = login_required(self.home)
        self.upload = login_required(self.upload)
        self.download = login_required(self.download)
        self.preview = login_required(self.preview)
        self.delete_file = login_required(self.delete_file)
        self.share = login_required(self.share)

    def home(self):
        path = request.args.get('path', '')
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], path)
        if not os.path.exists(full_path):
            flash('Path not found', 'danger')
            return redirect(url_for('files.home'))

        files = []
        for entry in os.scandir(full_path):
            files.append({
                'name': entry.name,
                'is_dir': entry.is_dir(),
                'size': format_file_size(entry.stat().st_size),
                'permissions': oct(entry.stat().st_mode)[-3:],
                'mtime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry.stat().st_mtime))
            })

        return render_template('index.html', files=files, path=path)

    def upload(self):
        path = request.args.get('path', '')
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], path)
        if not os.path.exists(full_path):
            flash('Path not found', 'danger')
            return redirect(url_for('files.home'))

        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part', 'danger')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
            if file:
                filename = file.filename
                filepath = os.path.join(full_path, filename)
                file.save(filepath)
                flash('File successfully uploaded', 'success')
                return redirect(url_for('files.home', path=path))
        return render_template('upload.html')

    def download(self, filename):
        path = request.args.get('path', '')
        full_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'], path, filename)
        return send_from_directory(directory=os.path.dirname(full_path), path=os.path.basename(full_path), as_attachment=True)

    def preview(self, filename):
        path = request.args.get('path', '')
        full_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'], path, filename)
        return send_from_directory(directory=os.path.dirname(full_path), path=os.path.basename(full_path))

    def delete_file(self, filename):
        path = request.args.get('path', '')
        full_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'], path, filename)
        if os.path.exists(full_path):
            os.remove(full_path)
            flash('File successfully deleted', 'success')
        else:
            flash('File not found', 'danger')
        return redirect(url_for('files.home', path=path))

    def share(self, filename):
        # 分享功能的实现可以根据具体需求来设计
        pass
