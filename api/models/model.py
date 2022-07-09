#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from sqlalchemy import (Column, String, DateTime, ForeignKey)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from flask import jsonify
import uuid

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
database_path = os.environ.get('DATABASE_URL')
db = SQLAlchemy()

# setup_db(app) binds a flask application and a SQLAlchemy service


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Parent Model.
#----------------------------------------------------------------------------#

class Parent(db.Model):
    __tablename__ = 'parents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_id = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc).astimezone(), nullable=False)
    parents_children = db.relationship('Child', back_populates='parent_children', cascade="all, delete, delete-orphan", lazy='dynamic')

    def __init__(self, card_id, first_name, last_name, image_url):
        self.card_id = card_id
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url

    #----------------------------------------------------------------------------#
    # CRUD FUNCTIONS
    #----------------------------------------------------------------------------#

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'card_id': self.card_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'image_url': self.image_url,
            'created_at': self.created_at
        }

#----------------------------------------------------------------------------#
# Child Model.
#----------------------------------------------------------------------------#

class Child(db.Model):
    __tablename__ = 'children'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('parents.id'), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc).astimezone(), nullable=False)
    parent_children = relationship('Parent', back_populates='parents_children')
    def __init__(self, parent_id, first_name, last_name, image_url, created_at):
        self.parent_id = parent_id
        self.first_name = first_name
        self.last_name = last_name
        self.image_url = image_url
        self.created_at = created_at

    #----------------------------------------------------------------------------#
    # CRUD FUNCTIONS
    #----------------------------------------------------------------------------#

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return jsonify({
            'id': self.id,
            'parent_id': self.parent_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'image_url': self.image_url,
            'created_at': self.created_at
        })