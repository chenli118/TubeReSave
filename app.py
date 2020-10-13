# -*- coding: utf-8 -*-

import os
import sys
import tbdown
import click
import datetime
from flask import Flask
from flask import redirect, url_for, abort, render_template, flash,send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret(^@^)string')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', prefix + os.path.join(app.root_path, 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# handlers
@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Note=Tube)


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')


# Forms
class NewTubeForm(FlaskForm):
    body = TextAreaField('LinkHRef', validators=[DataRequired()])
    submit = SubmitField('Save')


class EditTubeForm(FlaskForm):
    body = TextAreaField('LinkHRef', validators=[DataRequired()])
    submit = SubmitField('Update')


class DeleteTubeForm(FlaskForm):
    submit = SubmitField('Delete')


# Models
class Tube(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(240))
    LinkHRef = db.Column(db.String(240))
    CreateON = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    DownStatus =db.Column(db.Integer,default=-1)
    DownMsg = db.Column(db.Text,default=' ')
    # optional
    def __repr__(self):
        return '<Title %r>' % self.Title


@app.route('/')
def index():
    form = DeleteTubeForm()
    tubes = Tube.query.all()
    return render_template('index.html', tubes=tubes, form=form)

@app.route('/<path:path>', methods=['GET'])
def static_proxy(path):    
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)),"videos")
    return send_from_directory(root, path)

@app.route('/new', methods=['GET', 'POST'])
def new_note():
    form = NewTubeForm()
    if form.validate_on_submit():
        LinkHRef = form.body.data
        tube = Tube(LinkHRef=LinkHRef)
        db.session.add(tube)
        db.session.commit()
        flash('Your tube is saved.')
        return redirect(url_for('index'))
    return render_template('new_note.html', form=form)


@app.route('/edit/<int:tube_id>', methods=['GET', 'POST'])
def edit_note(tube_id):
    form = EditTubeForm()
    tube = Tube.query.get(tube_id)
    if form.validate_on_submit():
        tube.LinkHRef = form.body.data
        db.session.commit()
        flash('tube is updated.')
        return redirect(url_for('index'))
    form.body.data = tube.Title  # preset form input's value
    return render_template('edit_note.html', form=form)


@app.route('/delete/<int:tube_id>', methods=['POST'])
def delete_note(tube_id):
    form = DeleteTubeForm()
    if form.validate_on_submit():
        tube = Tube.query.get(tube_id)
        db.session.delete(tube)
        db.session.commit()
        flash('tube is deleted.')
    else:
        abort(400)
    return redirect(url_for('index'))

@db.event.listens_for(Tube, 'before_delete')
def receive_before_delete(mapper, connection, target):
    tbdown.delete(connection,target)

@db.event.listens_for(Tube, 'after_insert')
def after_insert_listener(mapper, connection, target):
    tbdown.down(connection,target)
