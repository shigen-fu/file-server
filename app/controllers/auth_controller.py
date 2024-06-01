from flask import flash, redirect, render_template, request, session, url_for

from app.utils.utils import verify_user


class AuthController:
    def login(self):
        if 'username' in session:
            return redirect(url_for('files.home'))
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if verify_user(username, password):
                session['username'] = username
                return redirect(url_for('files.home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html')

    def logout(self):
        session.pop('username', None)
        flash('You have been logged out', 'success')
        return redirect(url_for('auth.login'))
