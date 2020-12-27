from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#----------------------------------------------------------------------------#
# Config.
#----------------------------------------------------------------------------#

db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Show(db.Model):
    __tablename__ = 'show'    
    artist_id= db.Column(db.Integer, db.ForeignKey('artist.id_artist'), primary_key=True) 
    venue_id = db.Column( db.Integer, db.ForeignKey('venue.id_venue'), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, primary_key=True)
    venue_child = db.relationship("Venue", back_populates="artists") 
    artist_parent = db.relationship("Artist", back_populates="venues") 


class Venue(db.Model):
    __tablename__ = 'venue'    
    id_venue = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    site_link = db.Column(db.String(120), nullable=True, default='www.yoursite.com')
    facebook_link = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True, default='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60')
    seeking_talent = db.Column(db.Boolean, nullable=True, default=True)
    seeking_description = db.Column(db.String(120), nullable=True, default='We are on the lookout for a local artist to play every two weeks. Please call us.')
    artists = db.relationship("Show", back_populates="venue_child")
  # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artist'
    id_artist = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    site_link = db.Column(db.String(120), nullable=True, default='www.yoursite.com')
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_venue = db.Column(db.Boolean, nullable=True, default=False)
    seeking_description = db.Column(db.String(120), nullable=True, default='Looking for shows to perform.')
    image_link = db.Column(db.String(500), nullable=True, default='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80')   
    venues = db.relationship("Show", back_populates="artist_parent")
  # TODO: implement any missing fields, as a database migration using Flask-Migrate

  # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
