#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
import sys
from models import *

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

#class Venue(db.Model):
 #   __tablename__ = 'Venue'
#
 #   id = db.Column(db.Integer, primary_key=True)
  #  name = db.Column(db.String(), nullable=False)
  #  city = db.Column(db.String(120), nullable=False)
  #  state = db.Column(db.String(120), nullable=False)
  #  address = db.Column(db.String(120), nullable=False)
  #  phone = db.Column(db.String(120))
  #  image_link = db.Column(db.String(500))
  #  facebook_link = db.Column(db.String(120))
  #  genres = db.Column(db.String(), nullable=False)
  #  website = db.Column(db.String())
  #  seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
  #  seeking_description = db.Column(db.String())
  #  show = db.relationship('Show', backref='venues', lazy=True)
    
   # def __repr__(self):
   #     return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.address}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

#class Artist(db.Model):
 #   __tablename__ = 'Artist'

  #  id = db.Column(db.Integer, primary_key=True)
   # name = db.Column(db.String(), nullable=False)
   # city = db.Column(db.String(120), nullable=False)
   # state = db.Column(db.String(120), nullable=False)
   # phone = db.Column(db.String(120))
   # genres = db.Column(db.String(120), nullable=False)
   # image_link = db.Column(db.String(500))
   # facebook_link = db.Column(db.String(120))
   # website = db.Column(db.String())
   # seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
   # seeking_description = db.Column(db.String())
   # show = db.relationship('Show', backref='artists', lazy=True)
    
    
    #def __repr__(self):
    #    return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone}>'
 
#db.create_all()

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#class Show(db.Model):
 #   __tablename__ = "Show"
    
  #  id = db.Column(db.Integer, primary_key=True)
  #  artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
  #  venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
  #  start_time = db.Column(db.DateTime)
    
  #  def __repr__(self):
  #      return f'<Show {self.id} {self.artist_id} {self.venue_id}>'
    
#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
    data = []
    outputs = Venue.query.distinct(Venue.city, Venue.state).all()
    for output in outputs:
        unique_city_state = {
            "city": output.city,
            "state": output.state
            }
        venues = Venue.query.filter_by(city=output.city, state=output.state).all()
        
        distinct_venues = []
        for venue in venues:
            distinct_venues.append({
                "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": len(list(filter(lambda x: x.start_time > datetime.now(), venue.show)))
            })
        
        unique_city_state["venues"] = distinct_venues
        data.append(unique_city_state)
        
    return render_template('pages/venues.html', areas=data);
  #data=[{
   # "city": "San Francisco",
    #"state": "CA",
    #"venues": [{
     # "id": 1,
      #"name": "The Musical Hop",
      #"num_upcoming_shows": 0,
   # }, {
    #  "id": 3,
     # "name": "Park Square Live Music & Coffee",
      #"num_upcoming_shows": 1,
   # }]
  #}, {
   # "city": "New York",
    #"state": "NY",
    #"venues": [{
     # "id": 2,
      #"name": "The Dueling Pianos Bar",
     # "num_upcoming_shows": 0,
    #}]
  #}]
  

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get("search_term", "")
  response = {}
  venues = Venue.query.filter(Venue.name.ilike(f"%{search_term}%")).all()
  response["count"] = len(venues)
  response["data"] = []
  
  for venue in venues:
      venue_distinct = {
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": len(list(filter(lambda x: x.start_time > datetime.now(), venue.show)))        
      }
      response["data"].append(venue_distinct)
      
  return render_template('pages/search_venues.html', results=response, search_term=search_term)    
 # response={
  #  "count": 1,
   # "data": [{
    #  "id": 2,
    #  "name": "The Dueling Pianos Bar",
    #  "num_upcoming_shows": 0,
   # }]
 # }
  

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  data = Venue.query.get(venue_id)
  setattr(data, "genres", data.genres.split(",")) # converts genres converted to string on collection back to array
  
  # past Shows
  
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.venues==data).filter(Show.start_time < datetime.now()).all()
  past_shows = []
  #past_shows = list(filter(lambda show: show.start_time < datetime.now(), data.show))
  #sub_shows = []
  for show in past_shows_query:
      sub = {}
      sub["artist_name"] = show.artists.name
      sub["artist_id"] = show.artists.id
      sub["artist_image_link"] = show.artists.image_link
      sub["start_time"] = show.start_time.strftime("%m/%d/%y, %H:%M:%S")
      past_shows.append(sub)
      
  setattr(data, "past_shows", past_shows)
  setattr(data, "past_shows_count", len(past_shows_query))
  
  # upcoming shows
  
  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.venues==data).filter(Show.start_time > datetime.now()).all()
  #upcoming_shows = list(filter(lambda show: show.start_time > datetime.now(), data.show))
  upcoming_shows = []
  for show in upcoming_shows_query: 
      sub = {}
      sub["artist_name"] = show.artists.name
      sub["artist_id"] = show.artists.id
      sub["artist_image_link"] = show.artists.image_link
      sub["start_time"] = show.start_time.strftime("%m/%d/%y, %H:%M:%S")
      upcoming_shows.append(sub)
      
  setattr(data, "upcoming_shows", upcoming_shows)
  setattr(data, "upcoming_shows_count", len(upcoming_shows_query))
  
  return render_template('pages/show_venue.html', venue=data)
  
  #data1={
   # "id": 1,
    #"name": "The Musical Hop",
   # "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
   # "address": "1015 Folsom Street",
   # "city": "San Francisco",
   # "state": "CA",
   # "phone": "123-123-1234",
   # "website": "https://www.themusicalhop.com",
   # "facebook_link": "https://www.facebook.com/TheMusicalHop",
   # "seeking_talent": True,
   # "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
   # "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
   # "past_shows": [{
   #   "artist_id": 4,
    #  "artist_name": "Guns N Petals",
    #  "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    #  "start_time": "2019-05-21T21:30:00.000Z"
   # }],
   # "upcoming_shows": [],
   # "past_shows_count": 1,
   # "upcoming_shows_count": 0,
 # }
  #data2={
   # "id": 2,
   # "name": "The Dueling Pianos Bar",
   # "genres": ["Classical", "R&B", "Hip-Hop"],
   # "address": "335 Delancey Street",
   # "city": "New York",
   # "state": "NY",
   # "phone": "914-003-1132",
   # "website": "https://www.theduelingpianos.com",
   # "facebook_link": "https://www.facebook.com/theduelingpianos",
   # "seeking_talent": False,
   # "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
   # "past_shows": [],
   # "upcoming_shows": [],
   # "past_shows_count": 0,
   # "upcoming_shows_count": 0,
 # }
 # data3={
  #  "id": 3,
  #  "name": "Park Square Live Music & Coffee",
  #  "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #  "address": "34 Whiskey Moore Ave",
  #  "city": "San Francisco",
  #  "state": "CA",
  #  "phone": "415-000-1234",
  #  "website": "https://www.parksquarelivemusicandcoffee.com",
  #  "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #  "seeking_talent": False,
  #  "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #  "past_shows": [{
  #    "artist_id": 5,
  #    "artist_name": "Matt Quevedo",
  #    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #    "start_time": "2019-06-15T23:00:00.000Z"
  #  }],
  #  "upcoming_shows": [{
  #    "artist_id": 6,
  #    "artist_name": "The Wild Sax Band",
  #    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #    "start_time": "2035-04-01T20:00:00.000Z"
  #  }, {
  #    "artist_id": 6,
  #    "artist_name": "The Wild Sax Band",
  #    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #    "start_time": "2035-04-08T20:00:00.000Z"
  #  }, {
  #    "artist_id": 6,
  #    "artist_name": "The Wild Sax Band",
  #    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #    "start_time": "2035-04-15T20:00:00.000Z"
  #  }],
  #  "past_shows_count": 1,
  #  "upcoming_shows_count": 1,
  #}
  #data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
   form = VenueForm()
   return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    form = VenueForm(request.form)
    print(form)
    try:
        add_venue = Venue(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            address=form.address.data,
            phone=form.phone.data, 
            facebook_link=form.facebook_link.data,
            image_link=form.image_link.data,
            genres=",".join(form.genres.data), # collects array of genres as strings seperated by comma
            website=form.website_link.data,
            seeking_talent=True if 'seeking_talent' in request.form else False,
            seeking_description=form.seeking_description.data
        )
        db.session.add(add_venue)
        db.session.commit()
  # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash('An error occured. Venue' + ' could not be listed.')
    finally:
        db.session.close()
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
        flash("Venue " + venue.name + " has been deleted successfully!")
    except:
        db.session.rollback()
        print(sys.exc_info())
        flash("Venue was not deleted Successfully.")
    finally:
        db.session.close()
        
    return redirect(url_for("index"))
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
       data = db.session.query(Artist.id, Artist.name).all()   
       return render_template('pages/artists.html', artists=data)
 # data=[{
 #   "id": 4,
 #   "name": "Guns N Petals",
 # }, {
 #   "id": 5,
 #   "name": "Matt Quevedo",
 # }, {
 #   "id": 6,
 #   "name": "The Wild Sax Band",
 # }]
  

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
      search_term = request.form.get('search_term', '')
      artists = Artist.query.filter(
          Artist.name.ilike(f"%{search_term}%")).all()
      response = {
          "count": len(artists),
          "data": []
          }
      
      for artist in artists:
          sub_data = {}
          sub_data["name"] = artist.name
          sub_data["id"] = artist.id
          
          upcoming_shows = 0
          for show in artist.show:
              if show.start_time > datetime.now():
                  upcoming_shows = upcoming_shows + 1
          sub_data["upcoming_shows"] = upcoming_shows
          
          response["data"].append(sub_data)
      return render_template('pages/search_artists.html', results=response, search_term=search_term)
  
  #response={
   # "count": 1,
    #"data": [{
     # "id": 4,
      #"name": "Guns N Petals",
      #"num_upcoming_shows": 0,
    #}]
  #}
  

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  
  data = Artist.query.get(artist_id)
  setattr(data, "genres", data.genres.split(",")) # converts genre string to array
  
  # Past Shows
  
  past_shows = list(filter(lambda show: show.start_time < datetime.now(), data.show))
  sub_shows = []
  for show in past_shows:
      sub = {}
      sub["venue_name"] = show.venues.name
      sub["venue_id"] = show.venues.id
      sub["venue_image_link"] = show.venues.image_link
      sub["start_time"] = show.start_time.strftime("%m%d%y, %H:%M:%S")
      
      sub_shows.append(sub)
     
  setattr(data, "past_shows", sub_shows)
  setattr(data, "past_shows_count", len(past_shows))
  
  # Upcoming shows
  
  upcoming_shows = list(filter(lambda show: show.start_time > datetime.now(), data.show))
  sub_shows = []
  for show in upcoming_shows:
      sub = {}
      sub["venue_name"] = show.venues.name
      sub["venue_id"] = show.venues.id
      sub["venue_image_link"] = show.venues.image_link
      sub["start_time"] = show.start_time.strftime("%m/%d/%y, %H:%M:%S")
      
      sub_shows.append(sub)
      
  setattr(data, "upcoming_shows", sub_shows)
  setattr(data, "upcoming_shows_count", len(upcoming_shows))
  
  return render_template('pages/show_artist.html', artist=data)

 # data1={
  #  "id": 4,
   # "name": "Guns N Petals",
   # "genres": ["Rock n Roll"],
    #"city": "San Francisco",
    #"state": "CA",
   # "phone": "326-123-5000",
   # "website": "https://www.gunsnpetalsband.com",
   # "facebook_link": "https://www.facebook.com/GunsNPetals",
   # "seeking_venue": True,
   # "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
   # "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
   # "past_shows": [{
   #   "venue_id": 1,
   #   "venue_name": "The Musical Hop",
   #   "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    #  "start_time": "2019-05-21T21:30:00.000Z"
   # }],
   # "upcoming_shows": [],
   # "past_shows_count": 1,
   # "upcoming_shows_count": 0,
 # }
 # data2={
 #   "id": 5,
  #  "name": "Matt Quevedo",
   # "genres": ["Jazz"],
    #"city": "New York",
    #"state": "NY",
    #"phone": "300-400-5000",
   # "facebook_link": "https://www.facebook.com/mattquevedo923251523",
   # "seeking_venue": False,
   # "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
   # "past_shows": [{
   #   "venue_id": 3,
   #   "venue_name": "Park Square Live Music & Coffee",
   #   "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
   #   "start_time": "2019-06-15T23:00:00.000Z"
   # }],
   # "upcoming_shows": [],
   # "past_shows_count": 1,
   # "upcoming_shows_count": 0,
  #}
  #data3={
  #  "id": 6,
  #  "name": "The Wild Sax Band",
  #  "genres": ["Jazz", "Classical"],
  #  "city": "San Francisco",
  #  "state": "CA",
  #  "phone": "432-325-5432",
  #  "seeking_venue": False,
  #  "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #  "past_shows": [],
  #  "upcoming_shows": [{
  #    "venue_id": 3,
  #    "venue_name": "Park Square Live Music & Coffee",
  #    "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #    "start_time": "2035-04-01T20:00:00.000Z"
  #  }, {
  #    "venue_id": 3,
  #    "venue_name": "Park Square Live Music & Coffee",
  #    "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #    "start_time": "2035-04-08T20:00:00.000Z"
  #  }, {
  #    "venue_id": 3,
  #    "venue_name": "Park Square Live Music & Coffee",
  #    "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #    "start_time": "2035-04-15T20:00:00.000Z"
  #  }],
  #  "past_shows_count": 0,
  #  "upcoming_shows_count": 3,
  #}
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  form.genres.data = artist.genres.split(",") # converts genres string to array
  
  return render_template('forms/edit_artist.html', form=form, artist=artist)
  
 # artist={
 #   "id": 4,
 #   "name": "Guns N Petals",
 #   "genres": ["Rock n Roll"],
 #   "city": "San Francisco",
 #   "state": "CA",
 #   "phone": "326-123-5000",
 #   "website": "https://www.gunsnpetalsband.com",
 #   "facebook_link": "https://www.facebook.com/GunsNPetals",
 #   "seeking_venue": True,
 #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
 #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
 # }
  # TODO: populate form with fields from artist with ID <artist_id>
  

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    form = ArtistForm(request.form)
    
    try: 
       artist = Artist.query.get(artist_id)
       artist.name = form.name.data
       artist.city = form.city.data
       artist.state = form.state.data
       artist.phone = form.phone.data
       artist.genres = ",".join(form.genres.data) # converts genre arrays to string
       artist.facebook_link= form.facebook_link.data
       artist.image_link = form.image_link.data
       artist.seeking_venue = form.seeking_venue.data
       artist.seeking_description = form.seeking_description.data
       artist.website = form.website_link.data
            
       db.session.add(artist)
       db.session.commit()
       flash("Artist " + artist.name + " was successfully edited")
    except:
       db.session.rollback()
       print(sys.exc_info())
       flash("Artist was not edited successfully")
    finally:
        db.session.close()
        
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
  
    venue = Venue.query.get(venue_id)
    form.genres.data = venue.genres.split(",") # convert genre string back to array 
    
    return render_template('forms/edit_venue.html', form=form, venue=venue)
 # venue={
 #   "id": 1,
 #   "name": "The Musical Hop",
 #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
 #   "address": "1015 Folsom Street",
 #   "city": "San Francisco",
 #   "state": "CA",
 #   "phone": "123-123-1234",
 #   "website": "https://www.themusicalhop.com",
 #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
 #   "seeking_talent": True,
 #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
 #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
 # }
  # TODO: populate form with values from venue with ID <venue_id>

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes 
    form = VenueForm(request.form)  
    
    try:
        venue = Venue.query.get(venue_id)
        venue.name = form.name.data
        venue.city=form.city.data
        venue.state=form.state.data
        venue.address=form.address.data
        venue.phone=form.phone.data
        venue.genres=",".join(form.genres.data) # converts genre array to strings seperated by comma
        venue.facebook_link=form.facebook_link.data
        venue.image_link=form.image_link.data
        venue.seeking_talent=form.seeking_talent.data
        venue.seeking_description=form.seeking_description.data
        venue.website=form.website_link.data

        db.session.add(venue)
        db.session.commit()
        flash("Venue " + form.name.data + " edited successfully")
            
    except Exception:
        db.session.rollback()
        print(sys.exc_info())
        flash("Venue was not edited successfully.")
            
    finally:
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
    form = ArtistForm(request.form)
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
    try:
        add_artist = Artist(
            name=form.name.data,
            city=form.city.data,
            state=form.state.data,
            phone=form.phone.data,
            genres=",".join(form.genres.data), # convert genres array to string separated by commas
            image_link=form.image_link.data,
            facebook_link=form.facebook_link.data,
            website=form.website_link.data,
            seeking_venue=form.seeking_venue.data,
            seeking_description=form.seeking_description.data,
        )
        db.session.add(add_artist)
        db.session.commit()      
  # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    except:
        db.session.rollback()
        flash("Artist was not successfully listed.")
    finally:
        db.session.close()
        
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  
  data = []
  
  shows = Show.query.all()
  for show in shows:
      sub = {}
      sub["venue_id"] = show.venues.id
      sub["venue_name"] = show.venues.name
      sub["artist_id"] = show.artists.id
      sub["artist_name"] = show.artists.name
      sub["artist_image_link"] = show.artists.image_link
      sub["start_time"] = show.start_time.strftime("%m/%d/%y, %H:%M:%S")
      
      data.append(sub)
  return render_template('pages/shows.html', shows=data)
 # data=[{
 #   "venue_id": 1,
 #   "venue_name": "The Musical Hop",
 #   "artist_id": 4,
 #   "artist_name": "Guns N Petals",
 #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
 #   "start_time": "2019-05-21T21:30:00.000Z"
 # }, {
 #   "venue_id": 3,
 #   "venue_name": "Park Square Live Music & Coffee",
 #   "artist_id": 5,
 #   "artist_name": "Matt Quevedo",
 #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
 #   "start_time": "2019-06-15T23:00:00.000Z"
 # }, {
 #   "venue_id": 3,
 #   "venue_name": "Park Square Live Music & Coffee",
 #   "artist_id": 6,
 #   "artist_name": "The Wild Sax Band",
 #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
 #   "start_time": "2035-04-01T20:00:00.000Z"
 # }, {
 #   "venue_id": 3,
 #   "venue_name": "Park Square Live Music & Coffee",
 #   "artist_id": 6,
 #   "artist_name": "The Wild Sax Band",
 #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
 #   "start_time": "2035-04-08T20:00:00.000Z"
 # }, {
 #   "venue_id": 3,
 #   "venue_name": "Park Square Live Music & Coffee",
 #   "artist_id": 6,
 #   "artist_name": "The Wild Sax Band",
 #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
 #
 #  "start_time": "2035-04-15T20:00:00.000Z"
 # }]
  

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
    form = ShowForm(request.form)
    
    try:
        add_show = Show(
            artist_id=form.artist_id.data,
            venue_id=form.venue_id.data,
            start_time=form.start_time.data
        )
        db.session.add(add_show)
        db.session.commit()
        flash('Show was successfully listed!')
    except Exception:
        db.session.rollback()
        print(sys.exc_info())
        flash('Show was not successfully listed.')
    finally:
        db.session.close()
        
    return render_template('pages/home.html')
  # on successful db insert, flash success
  #flash('Show was successfully listed!')
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
