from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_app.models.user import User
from flask_app.models.guest import Guest
import copy
@app.route('/guests/<int:id>')
def view_guest(id):
    if 'user' not in session:
        return redirect('/')
    guest = Guest.get_guest_by_id({'id': id})
    return render_template('view_guest.html', guest = guest.__dict__)


@app.route('/edit/guest/<int:id>', methods = ['GET', 'POST'])
def update_guest(id):
    if 'user' not in session:
        return redirect ('/')
    
    if request.method == "POST":
        if not Guest.validate_guest(request.form):
            return redirect(url_for("add_guest"))
        Guest.edit_guest(request.form | {})
    else:
        guest = Guest.get_guest_by_id({"id": id})
        if not guest:
            flash("guest does not exist")
            return redirect('/dashboard')
        if guest.user_id != session['user']['id']:
            flash("That isn't your guest")
            return redirect('/dashboard')
        return render_template("create_edit_guest.html", guest=guest.__dict__)
    return redirect('/dashboard')

@app.route('/dashboard')
def main_dash():
    if 'user' not in session:
        return redirect('/')
    user = User.get_user_by_id(session['user']['id'])
    return render_template('home.html', user = session['user'], guests=[r.__dict__ for r in Guest.get_guests()])



@app.route('/delete/guest/', methods=['POST'])
def delete_guest():
    if 'user' not in session:
        return redirect ('/')
    guest = Guest.get_guest_by_id(request.form['id'])
    if guest.user_id != session['user']['id']:
        flash("That isn't your guest")
        return redirect('/dashboard')
    Guest.delete_guest(request.form)
    return redirect('/dashboard')



@app.route('/create/guest', methods = ["POST", "GET"])
def add_guest():
    if 'user' not in session:
        return redirect ('/')
    if request.method == "POST":
        if not Guest.validate_guest(request.form):
            return redirect(url_for("add_guest"))
        data = request.form | { 'user_id': session['user']['id'] }
        Guest.create_guest(data)
    else:
        return render_template("create_edit_guest.html")
    return redirect('/dashboard')






        



