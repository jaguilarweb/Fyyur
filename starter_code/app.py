#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from models import *
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')

db.init_app(app)

migrate = Migrate(app, db)

  # TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

# Models was separeted in models.py

  # TODO: implement any missing fields, as a database migration using Flask-Migrate
  # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():

    try:
      artists=Artist.query.order_by(Artist.id_artist.desc()).limit(10).all()   
      venues=Venue.query.order_by(Venue.id_venue.desc()).limit(10).all() 
    except Exception as e:
      print(e)
    pass
    
    return render_template('pages/home.html', artists=artists, venues=venues)
    

#  ----------------------------------------------------------------
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
    area=Venue.query.distinct('city')
    venue=Venue.query.distinct('name')
    return render_template('pages/venues.html', areas=area, venues=venue)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term', '')
    venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()
    cities = Venue.query.filter(Venue.city.ilike('%' + search_term + '%')).all()
    states = Venue.query.filter(Venue.state.ilike('%' + search_term + '%')).all()    
    data = []
    city = []
    state = []
    count = 0
    for venue in venues:
        search = Venue.query.filter(Venue.id_venue == venue.id_venue)
        data.append({
          "id": venue.id_venue,
          "name": venue.name,
          "city": venue.city,
          "state": venue.state
        })
        if search.count() > 0:
          count += 1

    for venue in cities:
        search = Venue.query.filter(Venue.city == venue.city)
        data.append({
          "id": venue.id_venue,
          "name": venue.name,
          "city": venue.city,
          "state": venue.state
        })
        if search.count() > 0:
          count += 1

    for venue in states:
        search = Venue.query.filter(Venue.state == venue.state)
        data.append({
          "id": venue.id_venue,
          "name": venue.name,
          "city": venue.city,
          "state": venue.state
        })
        if search.count() > 0:
          count += 1
    response={
          "count": count,
          "data": data
        }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
    venue=Venue.query.filter_by(id_venue=venue_id).first()

  # Using JOIN Queries
    past_shows = db.session.query(Show.venue_id, Show.start_time, Artist.id_artist, Artist.name, Artist.image_link).join(Venue).join(Artist).filter(Show.start_time < datetime.now()).filter(Show.venue_id == venue_id).all()
    upcoming_shows = db.session.query(Show.venue_id, Show.start_time, Artist.id_artist, Artist.name, Artist.image_link).join(Venue).join(Artist).filter(Show.start_time >= datetime.now()).filter(Show.venue_id == venue_id).all()
    artists_past = []
    artists_upcoming = []

    for show in past_shows:        
        artists_past.append({
          "venue_id": show.venue_id,
          "start_time": str(show.start_time),
          "id": show.id_artist,
          "name": show.name,
          "image_link": show.image_link,
        })
      
    for show in upcoming_shows:
        artists_upcoming.append({
          "venue_id": show.venue_id,
          "start_time": str(show.start_time),
          "name": show.name,
          "id": show.id_artist,
          "name": show.name,
          "image_link": show.image_link,
        })

    data={
      "artists_past": artists_past,
      "artists_upcoming": artists_upcoming,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows),
    }
   
    return render_template('pages/show_venue.html', venue=venue, data=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
    error= False
    try:
      name = request.form.get('name')
      city = request.form.get('city')
      address = request.form.get('address')
      state = request.form.get('state')
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      site_link = request.form.get('site_link')
      facebook_link = request.form.get('facebook_link')
      image_link = request.form.get('image_link')
      seeking_talent = request.form.get('seeking_talent ')
      seeking_description = request.form.get('seeking_description')
      venue = Venue(name=name, city=city, address=address, state=state, phone=phone, genres=genres, site_link=site_link, facebook_link=facebook_link, image_link=image_link, seeking_talent=seeking_talent, seeking_description=seeking_description)
      db.session.add(venue)
      db.session.commit()
    except:
      error = True      
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      flash('An error occurred.'+ request.form['name'] +' Venue could not be insert.')     
    else:
      flash('Venue ' + request.form['name'] + ' was successfully listed!')

    return render_template('pages/home.html')    

  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  #flash('Venue ' + request.form['name'] + ' was successfully listed!')

  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/


#  Update
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue=Venue.query.filter_by(id_venue=venue_id).first()
  # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
    error= False
    try:               
      venue = Venue.query.get(venue_id)     
      venue.name = request.form.get('name')
      venue.city = request.form.get('city')   
      venue.state = request.form.get('state')   
      venue.addrres = request.form.get('address')  
      venue.phone = request.form.get('phone')
      venue.genres = request.form.getlist('genres')
      venue.site_link = request.form.get('site_link')
      venue.facebook_link = request.form.get('facebook_link')
      venue.seeking_venue = True
      venue.seeking_description = 'Estamos buscando'     
      venue.image_link = 'https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'   
      db.session.commit()
    except:
      error=True
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      flash('An error occurred. Venue could not be updated.') 
    else:
      flash('Venue ' + request.form['name'] + ' was successfully updated!')

    return redirect(url_for('show_venue', venue_id=venue_id))

# Delete Venue
#  -------------------------------------------------------------
@app.route('/venues/<int:venue_id>', methods=['POST'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    error= False
    try:
      venue = Venue.query.get(venue_id)
      db.session.delete(venue)
      db.session.commit()
    except:
      error=True
      db.session.rollback()
    finally:
      db.session.close()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    if error:
      flash('An error occurred. Venue could not be delete.') 
    else:
       flash('Venue was successfully deleted!')
    return redirect(url_for('index'))

#  ----------------------------------------------------------------
#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
    data=Artist.query.all()
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()
    cities = Artist.query.filter(Artist.city.ilike('%' + search_term + '%')).all()
    states = Artist.query.filter(Artist.state.ilike('%' + search_term + '%')).all()    
    data = []
    city = []
    state = []
    count = 0

    for artist in artists:
        search = Artist.query.filter(Artist.id_artist == artist.id_artist)
        data.append({
        "id": artist.id_artist,
        "name": artist.name,
        "city": artist.city,
        "state": artist.state
        })
        if search.count() > 0:
          count += 1
    
    for artist in cities:
        search = Artist.query.filter(Artist.city == artist.city)
        data.append({
          "id": artist.id_artist,
          "name": artist.name,
          "city": artist.city,
          "state": artist.state
        })
        if search.count() > 0:
          count += 1

    for artist in states:
        search = Artist.query.filter(Artist.state == artist.state)
        data.append({
          "id": artist.id_artist,
          "name": artist.name,
          "city": artist.city,
          "state": artist.state
        })
        if search.count() > 0:
          count += 1
  
    response={
        "count": count,
        "data": data
    }

    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
    artist=Artist.query.filter_by(id_artist=artist_id).first()

    past_shows = db.session.query(Show.artist_id, Show.start_time, Venue.id_venue, Venue.name, Venue.image_link).join(Artist).join(Venue).filter(Show.start_time < datetime.now()).filter(Show.artist_id == artist_id).all()
    upcoming_shows = db.session.query(Show.artist_id, Show.start_time, Venue.id_venue, Venue.name, Venue.image_link).join(Artist).join(Venue).filter(Show.start_time >= datetime.now()).filter(Show.artist_id == artist_id).all()
    venues_past = []
    venues_upcoming = []

    for show in past_shows:
      
        venues_past.append({
          "artist_id": show.artist_id,
          "start_time": str(show.start_time),
          "id": show.id_venue,
          "name": show.name,
          "image_link": show.image_link,
        })
    
    for show in upcoming_shows:  
        venues_upcoming.append({
          "artist_id": show.artist_id,
          "start_time": str(show.start_time),
          "id": show.id_venue,
          "name": show.name,
          "image_link": show.image_link,
        })

    data={
      "venues_past": venues_past,
      "venues_upcoming": venues_upcoming,
      "past_shows_count": len(past_shows),
      "upcoming_shows_count": len(upcoming_shows)
    }

    return render_template('pages/show_artist.html', artist=artist, data=data)


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    error= False
    try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      site_link = 'www.yoursite.com'
      facebook_link = request.form.get('facebook_link')
      seeking_venue = True
      seeking_description = 'Estamos buscando'     
      image_link = 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
      artist= Artist(name=name, city=city, state=state, phone=phone, genres=genres, site_link=site_link, facebook_link=facebook_link, seeking_venue=seeking_venue, seeking_description=seeking_description, image_link=image_link)
      db.session.add(artist)
      db.session.commit()
    except:
      error=True
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      flash('An error occurred. Artist could not be insert.') 
    else:
       flash('Artist ' + request.form['name'] + ' was successfully listed!')
    
    return render_template('pages/home.html')

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
 
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist=Artist.query.filter_by(id_artist=artist_id).first()
  # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    error= False
    try:               
      artist = Artist.query.get(artist_id)     
      artist.name = request.form.get('name')
      artist.city = request.form.get('city')   
      artist.state = request.form.get('state')  
      artist.phone = request.form.get('phone')
      artist.genres = request.form.getlist('genres')
      artist.site_link = 'www.yoursite.com'
      artist.facebook_link = request.form.get('facebook_link')
      artist.seeking_venue = True
      artist.seeking_description = 'Estamos buscando'     
      artist.image_link = 'https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'   
      db.session.commit()
    except:
      error=True
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      flash('An error occurred. Artist could not be updated.') 
    else:
       flash('Artist ' + request.form['name'] + ' was successfully updated!')
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/artist/<int:artist_id>', methods=['POST'])
def delete_artist(artist_id):
    error= False
    try:
      artist = Artist.query.get(artist_id)
      db.session.delete(artist)
      db.session.commit()
    except:
      error=True
      db.session.rollback()
    finally:
      db.session.close()
  # clicking that button delete it from the db then redirect the user to the homepage
    if error:
      flash('An error occurred. Artist could not be delete.') 
    else:
       flash('Artist was successfully deleted!')
    return redirect(url_for('index'))

#  ----------------------------------------------------------------
#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.all()
    try:    
      data = []  
      for show in shows:
          data.append({
                "venue_id": show.venue_id,
                "venue_name": Venue.query.filter_by(id_venue=show.venue_id).first().name,
                "artist_id": show.artist_id,
                "artist_name": Artist.query.filter_by(id_artist=show.artist_id).first().name,
                "artist_image_link": Artist.query.filter_by(id_artist=show.artist_id).first().image_link,
                "start_time": str(show.start_time)
          })
    except Exception as e:
        print(e)
        pass
    return render_template('pages/shows.html', shows=data)

#  Create Show
#  --------------------------------------------------------------
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
    error= False
    try:
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get('start_time')    
      show= Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      db.session.add(show)
      db.session.commit()
    except:
      error=True
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      flash('An error occurred. Show could not be registed.')
    else:
      flash('Show was successfully listed!')   
    return render_template('pages/home.html')
  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/  

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
