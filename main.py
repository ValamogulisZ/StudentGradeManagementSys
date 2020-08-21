from flask import Flask, render_template, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, BooleanField, DateTimeField,
                     RadioField, SelectField, TextField, TextAreaField)
from wtforms.validators import DataRequired
# import for flask

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'anothersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# initialize flask

db = SQLAlchemy(app)


class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    grade = db.Column(db.Integer)

    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __repr__(self):
        return f"Student {self.name} (ID:{self.id}) got {self.grade} on midterm exam;"


# db.create_all()
all_student = Student.query.all()
print(all_student)
# import for sqlite


class addForm(FlaskForm):
    name = StringField('Input the name of student:', validators=[DataRequired()])
    grade = StringField('Input the midterm grade of student:', validators=[DataRequired()])
    submit1 = SubmitField('Add')


class delForm(FlaskForm):
    stu_id = StringField('Input the id of student you want to delete:', validators=[DataRequired()])
    submit2 = SubmitField('Delete')


class vieForm(FlaskForm):
    view_way = StringField('input "1" for check all, input "2" for check passed student', validators=[DataRequired()])
    submit3 = SubmitField('View')


### bonus point ###
class chaForm(FlaskForm):
    change_stu_id = StringField('Input the id of student you want to change:', validators=[DataRequired()])
    new_grade = IntegerField('Input the midterm grade of student:', validators=[DataRequired()])
    submit4 = SubmitField('Change')


@app.route('/', methods=['GET', 'POST'])
def index():
    # global choice_flag
    add_form = addForm()
    del_form = delForm()
    vie_form = vieForm()
    cha_form = chaForm()

    print("Index called")
    if add_form.validate_on_submit():
        session['name'] = add_form.name.data
        session['grade'] = add_form.grade.data
        # get form information

        db_name = session['name']
        db_grade = int(session['grade'])  # should follow the format of table
        print(db_name, db_grade)
        new_item = Student(db_name, db_grade)
        db.session.add(new_item)
        db.session.commit()
        print(all_student)
        # add to database
        session['show_items'] = str(Student.query.all())
        return redirect(url_for('results'))

    if del_form.validate_on_submit():
        print("deleting item")
        session['stu_id'] = del_form.stu_id.data
        del_id = session['stu_id']
        del_item = Student.query.get(del_id)
        db.session.delete(del_item)
        db.session.commit()
        # delete items in database
        session['show_items'] = str(Student.query.all())
        return redirect(url_for('results'))

    if vie_form.validate_on_submit():
        print("Inside View")
        session['view_way'] = vie_form.view_way.data
        print(session['view_way'])
        if int(session['view_way']) == 1:
            session['show_items'] = str(Student.query.all())
        elif int(session['view_way']) == 2:
            pass_student = Student.query.filter(Student.grade >= 85)
            print(pass_student.all())
            session['show_items'] = str(pass_student.all())
        return redirect(url_for('results'))

    ### bonus points ###
    if cha_form.validate_on_submit():
        print("changing item")
        session['change_stu_id'] = cha_form.change_stu_id.data
        session['new_grade'] = cha_form.new_grade.data
        # get form information

        db_id = int(session['change_stu_id'])
        db_grade = int(session['new_grade'])  # should follow the format of table
        print(db_id, db_grade)
        change_student = Student.query.get(db_id)
        change_student.grade = db_grade
        db.session.add(change_student)
        db.session.commit()
        # update to database

        session['show_items'] = str(Student.query.all())
        return redirect(url_for('results'))

    return render_template('index.html', add_form=add_form, del_form=del_form, vie_form=vie_form, cha_form=cha_form)


@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=True)

