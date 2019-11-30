#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
from datetime import datetime
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from sqlalchemy import func, inspect
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import Venue, Show, Artist, app, db

# TODO DONE: connect to a local postgresql database. SEE Models.py

#----------------------------------------------------------------------------#
# Custom Functions.
#----------------------------------------------------------------------------#

def object_as_dict(obj):
  '''Converts SQLALchemy Query Results to Dict
  Input: ORM Object
  Output: Single Object as Dict

  Makes use of the SQLAlchemy inspection system (https://docs.sqlalchemy.org/en/13/core/inspection.html)
  '''
  return {c.key: getattr(obj, c.key)
        for c in inspect(obj).mapper.column_attrs}

def get_dict_list_from_result(result):
    '''Converts SQLALchemy Collections Results to Dict
  Input: sqlalchemy.util._collections.result
  Output: Result as list

  Source: https://stackoverflow.com/questions/48232222/how-to-deal-with-sqlalchemy-util-collections-result
  '''
    list_dict = []
    for i in result:
        i_dict = i._asdict()  
        list_dict.append(i_dict)
        print(i_dict)
    return list_dict

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  # date = dateutil.parser.parse(value)
  # Instead of parsing a string, I directly parse a datetime object, so I changed this function.
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(value, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  # Bonus: List recently listed Artists & Venues
  recent_artists = Artist.query.order_by(Artist.id.desc()).limit(10).all()
  recent_venues = Venue.query.order_by(Venue.id.desc()).limit(10).all()
  return render_template('pages/home.html', recent_artists = recent_artists, recent_venues = recent_venues)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO DONE: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # Step 1: Get a list of dicts that contains City & State names, 
  # i.e. : [{'city': 'Frankfurt', 'state': 'AL'}, {'city': 'Berlin', 'state': 'AL'}]
  groupby_venues_result = (db.session.query(
                Venue.city,
                Venue.state
                )
        .group_by(
                Venue.city,
                Venue.state
                )
  )
  data=get_dict_list_from_result(groupby_venues_result)

  # Step 2: Loop through areas and append Venue data
  for area in data:
    area['venues'] = [object_as_dict(ven) for ven in Venue.query.filter_by(city = area['city']).all()]
    # Step 3: Append num_shows
    for ven in area['venues']:
      ven['num_shows'] = db.session.query(func.count(Show.c.Venue_id)).filter(Show.c.Venue_id == ven['id']).filter(Show.c.start_time > datetime.now()).all()[0][0]
  # NOTE: I added the number of shows to the venues.html template
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  search_term=request.form.get('search_term', '')
  search_venues_count = db.session.query(func.count(Venue.id)).filter(Venue.name.contains(search_term)).all()
  search_venues_result = Venue.query.filter(Venue.name.contains(search_term)).all()

  response={
    "count": search_venues_count[0][0],
    "data": search_venues_result
  }

  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO DONE: replace with real venue data from the venues table, using venue_id
  
  # Step 1: Get single Venue
  single_venue = Venue.query.get(venue_id)

  # Step 2: Get Past Shows
  single_venue.past_shows = (db.session.query(
    Artist.id.label("artist_id"), 
    Artist.name.label("artist_name"), 
    Artist.image_link.label("artist_image_link"), 
    Show)
    .filter(Show.c.Venue_id == venue_id)
    .filter(Show.c.Artist_id == Artist.id)
    .filter(Show.c.start_time <= datetime.now())
    .all())
  
  # Step 3: Get Upcomming Shows
  single_venue.upcoming_shows = (db.session.query(
    Artist.id.label("artist_id"), 
    Artist.name.label("artist_name"), 
    Artist.image_link.label("artist_image_link"), 
    Show)
    .filter(Show.c.Venue_id == venue_id)
    .filter(Show.c.Artist_id == Artist.id)
    .filter(Show.c.start_time > datetime.now())
    .all())

  # Step 4: Get Number of past Shows
  single_venue.past_shows_count = (db.session.query(
    func.count(Show.c.Venue_id))
    .filter(Show.c.Venue_id == venue_id)
    .filter(Show.c.start_time < datetime.now())
    .all())[0][0]

  # Step 5: Get Number of Upcoming Shows
  single_venue.upcoming_shows_count = (db.session.query(
    func.count(Show.c.Venue_id))
    .filter(Show.c.Venue_id == venue_id)
    .filter(Show.c.start_time > datetime.now())
    .all())[0][0]

  return render_template('pages/show_venue.html', venue=single_venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO DONE: insert form data as a new Venue record in the db, instead
  # TODO DONE: modify data to be the data object returned from db insertion
  form = VenueForm(request.form) # Initialize form instance with values from the request
  flashType = 'danger' # Initialize flashType to danger. Either it will be changed to "success" on successfully db insert, or in all other cases it should be equal to "danger"
  if form.validate():
    try:
      newVenue = Venue(
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        address = request.form['address'],
        phone = request.form['phone'],
        genres = request.form.getlist('genres'),
        facebook_link = request.form['facebook_link']
        )
      db.session.add(newVenue)
      db.session.commit()
      # on successful db insert, flash success
      flashType = 'success'
      flash('Venue {} was successfully listed!'.format(newVenue.name))
    except Exception as e: 
      # TODO DONE: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      print(e)
      flash('An error occurred due to database insertion error. Venue {} could not be listed.'.format(request.form['name']))
    finally:
      # Always close session
      db.session.close()
  else:
    flash(form.errors) # Flashes reason, why form is unsuccessful (not really pretty)
    flash('An error occurred due to form validation. Venue {} could not be listed.'.format(request.form['name']))
  return render_template('pages/home.html', flashType = flashType)

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO DONE: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # DONE BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  # NOTE: Javascript to handle Button click + success/error in "main.html"
  try:
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
    # This will alert User that Venue could not be deleted because they are still Shows
    return jsonify({ 'success': False })
  finally:
    db.session.close()
  # This will return the User to the HomePage 
  return jsonify({ 'success': True })

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO DONE: replace with real data returned from querying the database
  artists = Artist.query.all()
  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO DONE: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term=request.form.get('search_term', '')
  search_artist_count = db.session.query(func.count(Artist.id)).filter(Artist.name.contains(search_term)).all()
  search_artist_result = Artist.query.filter(Artist.name.contains(search_term)).all()
  response={
    "count": search_artist_count[0][0],
    "data": search_artist_result
  }
  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # NOTE: Comments are wrong? Should be Artist, not Venues
  # shows the venue page with the given venue_id
  # TODO DONE: replace with real venue data from the venues table, using venue_id
  
  # Step 1: Get single Artist
  single_artist = Artist.query.get(artist_id)

  # Step 2: Get Past Shows
  single_artist.past_shows = (db.session.query(
    Venue.id.label("venue_id"), 
    Venue.name.label("venue_name"), 
    Venue.image_link.label("venue_image_link"), 
    Show)
    .filter(Show.c.Artist_id == artist_id)
    .filter(Show.c.Venue_id == Venue.id)
    .filter(Show.c.start_time <= datetime.now())
    .all())
  
  # Step 3: Get Upcomming Shows
  single_artist.upcoming_shows = (db.session.query(
    Venue.id.label("venue_id"), 
    Venue.name.label("venue_name"), 
    Venue.image_link.label("venue_image_link"), 
    Show)
    .filter(Show.c.Artist_id == artist_id)
    .filter(Show.c.Venue_id == Venue.id)
    .filter(Show.c.start_time > datetime.now())
    .all())

  # Step 4: Get Number of past Shows
  single_artist.past_shows_count = (db.session.query(
    func.count(Show.c.Artist_id))
    .filter(Show.c.Artist_id == artist_id)
    .filter(Show.c.start_time < datetime.now())
    .all())[0][0]
  
  # Step 5: Get Number of Upcoming Shows
  single_artist.upcoming_shows_count = (db.session.query(
    func.count(Show.c.Artist_id))
    .filter(Show.c.Artist_id == artist_id)
    .filter(Show.c.start_time > datetime.now())
    .all())[0][0]

  return render_template('pages/show_artist.html', artist=single_artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)

  # Pre Fill form with data
  form.name.data = artist.name
  form.city.data = artist.city
  form.state.data = artist.state
  form.phone.data = artist.phone
  print(artist.genres)
  form.genres.data = [artist.genres]
  form.facebook_link.data = artist.facebook_link

  # TODO DONE: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO DONE: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  
  artist = Venue.query.get(artist_id)
  artist.name = request.form['name'],
  artist.city = request.form['city'],
  artist.state = request.form['state'],
  artist.phone = request.form['phone'],
  artist.genres = request.form['genres'],
  artist.facebook_link = request.form['facebook_link']
  db.session.add(artist)
  db.session.commit()
  db.session.close()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  # Pre Fill form with data
  form.name.data = venue.name
  form.city.data = venue.city
  form.state.data = venue.state
  form.address.data = venue.address
  form.phone.data = venue.phone
  form.genres.data = venue.genres
  form.facebook_link.data = venue.facebook_link
  # TODO DONE: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO DONE: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  
  venue = Venue.query.get(venue_id)
  venue.name = request.form['name'],
  venue.city = request.form['city'],
  venue.state = request.form['state'],
  venue.address = request.form['address'],
  venue.phone = request.form['phone'],
  venue.genres = request.form.getlist('genres'),
  venue.facebook_link = request.form['facebook_link']
  db.session.add(venue)
  db.session.commit()
  db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  # TODO DONE: insert form data as a new Artist record in the db, instead
  # TODO DONE: modify data to be the data object returned from db insertion
  form = ArtistForm(request.form) # Initialize form instance with values from the request
  flashType = 'danger' # Initialize flashType to danger. Either it will be changed to "success" on successfully db insert, or in all other cases it should be equal to "danger"
  if form.validate():
    try:
      newArtist = Artist(
        name = request.form['name'],
        city = request.form['city'],
        state = request.form['state'],
        phone = request.form['phone'],
        facebook_link = request.form['facebook_link'],
        genres = request.form.getlist('genres')
        )
      db.session.add(newArtist)
      db.session.commit()
      # on successful db insert, flash success
      flashType = 'success'
      flash('Artist {} was successfully listed!'.format(newArtist.name)) 
    except Exception as e: 
      # TODO DONE: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      print(e)
      flash('An error occurred due to database insertion error. Artist {} could not be listed.'.format(request.form['name']))
    finally:
      # Always close session
      db.session.close()
  else:
    flash(form.errors) # Flashes reason, why form is unsuccessful (not really pretty)
    flash('An error occurred due to form validation. Artist {} could not be listed.'.format(request.form['name']))
  # called upon submitting the new artist listing form

  return render_template('pages/home.html', flashType = flashType)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO DONE: replace with real shows data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  shows = (db.session.query(
    Venue.id.label("venue_id"), 
    Venue.name.label("venue_name"),
    Artist.id.label("artist_id"), 
    Artist.name.label("artist_name"), 
    Artist.image_link.label("artist_image_link"), 
    Show)
    .filter(Show.c.Venue_id == Venue.id)
    .filter(Show.c.Artist_id == Artist.id)
    .all())

  return render_template('pages/shows.html', shows=shows)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form

  # NOTE: Not requested, but I think its more intuitiv
  # Depending on Success or Error, the type of flash should have a different layout (i.e. green or red)
  # Since the project is using bootstrap, I make use of https://getbootstrap.com/docs/4.3/components/alerts/
  # Therefor, I also changed the templates/layouts/main.html file, so the type gets passed in as an argument to the render_template function
  # TODO DONE: insert form data as a new Show record in the db, instead

  form = ShowForm(request.form) # Initialize form instance with values from the request
  flashType = 'danger' # Initialize flashType to danger. Either it will be changed to "success" on successfully db insert, or in all other cases it should be equal to "danger"
  if form.validate():
    # NOTE: Form could not be validated due to a missing csrf-token.
    # I solved this issue by putting a "{{ form.csrf_token() }}"
    # under the respective <form> tag in forms/new_show.html
    try:
      newShow = Show.insert().values(
        Venue_id = request.form['venue_id'],
        Artist_id = request.form['artist_id'],
        start_time = request.form['start_time']
      )
      db.session.execute(newShow) 
      db.session.commit()
      # on successful db insert, flash success
      flashType = 'success'
      flash('Show was successfully listed!')
    except Exception as e: 
      # TODO DONE: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Show could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      print(e)
      flash('An error occurred due to database insertion error. Show could not be listed.')
    finally:
      # Always close session
      db.session.close()
  else:
    flash(form.errors) # Flashes reason, why form is unsuccessful (not really pretty)
    flash('An error occurred due to form validation. Show could not be listed.')
  return render_template('pages/home.html', flashType = flashType)

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
    app.run(debug=True) # NOTE I prefer to set debug mode to true within the script

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
