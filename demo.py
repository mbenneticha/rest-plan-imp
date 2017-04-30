#!/usr/bin/env python
from google.appengine.ext import ndb
import webapp2
import json

class Boat(ndb.Model):
  id = ndb.StringProperty()  #auto-generated string
  name = ndb.StringProperty(required=True)
  type = ndb.StringProperty()
  length = ndb.IntegerProperty()
  at_sea = ndb.BooleanProperty()

class Slip(ndb.Model):
  id = ndb.StringProperty()  #auto-generated string
  number = ndb.IntegerProperty(required=True)
  current_boat = ndb.StringProperty()
  arrival_date = ndb.StringProperty()

class BoatHandler(webapp2.RequestHandler):
  #add a newly created boat; starts at_sea = True
  def post(self):
	  #parent_key = ndb.Key(Boat, "parent_boat")
	  boat_data = json.loads(self.request.body)
	  new_boat = Boat(name=boat_data['name'], type=boat_data['type'], length=boat_data['length'], at_sea=True)
	  new_boat.put()
	  boat_dict = new_boat.to_dict()
	  boat_dict['id'] = '/boat/' + new_boat.key.urlsafe()
	  self.response.write(json.dumps(boat_dict))
  
  #delete a boat
  def delete(self, id=None):
    try:
      if id:
        b = ndb.Key(urlsafe=id).get()
        #if boat is in slip
        if (b.at_sea = false):
          #get all slips
          slip = allSlips.get()
          #empty slip with boat
          if (slip.current_boat = b.id):
            slip.current_boat = None
            slip.arrival_date = None
            slip.put()
        #delete boat
        b.key.delete()
        self.response.write("<html><body><p>Success: Boat deleted!</p></body></html>")
    except (HTTPError, 404):
      self.response.write("<html><body><p>Bad Request. Ensure ID Values are correct.</p></body></html>")
  
  #modify a boat's properties; excludes at_sea!
  def patch(self, id=None):
    try:
      if id:
        # get request body
        boat_data = json.loads(self.request.body)
        # get boat in question
        b = ndb.Key(urlsafe=id).get()
        # error out if updating wrong data
        if boat_data.get('at_sea') or boat_data.get('at_sea')==False:
          self.response.write("Cannot change at_sea manually!")
        # update correct data
        else:
          if boat_data.get('name'):
            b.name = boat_data['name']
            self.response.write("Updated boat name\n")
          # Update Length and Type here
          b.put()
          boat_dict = b.to_dict()
          self.response.write(boat_dict)
    except (HTTPError, 404):
      self.response.write("<html><body><p>Bad Request. Ensure ID Values are correct.</p></body></html>")
  
  #replace a boat; at_sea value remains the same.
	def put(self, id=None):
	  try:
	    if id:
	      # get request body
	      boat_data = json.loads(self.request.body)
	      # get boat in question
	      b = ndb.Key(urlsafe=id).get()
	      # error out if updating at_sea
	      if boat_data.get('at_sea') or boat_data.get('at_sea')==False:
	        self.response.write("Cannot change at_sea manually!")
	      #or if no name is given
	      elif boat_data.get('name')==NULL:
	        self.response.write("Boat name is REQUIRED!")
	      #update correct data
	      else:
	        #set new name
	        if boat_data.get('name'):
	          b.name = boat_data['name']
	          self.response.write("Updated boat name\n")
	        #set new type if given
	        if boat_data.get('type'):
	          b.type = boat_data['type']
	          self.response.write("Updated boat type\n")
	        else:
	          b.type = null;
	        #set new length if given
	        if boat_data.get('length'):
	          b.length = boat_data['length']
	          self.response.write("Updated boat length\n")
	        else:
	          b.length = null;
	        b.put()
	        boat_dict = b.to_dict()
	        self.response.write(boat_dict)
	  except (HTTPError, 404):
	    self.response.write("<html><body><p>Bad Request. Ensure ID Values are correct.</p></body></html>")
  
  #view a boat
  def get(self, id=None):
    #if the id is given, view that boat (by ID)
    if id:
      b = ndb.Key(urlsafe=id).get()
      b_d = b.to_dict()
    #view all boats
    else:
      self.response.write(json.dumps(b_d))
      allBoats = Boat.query().fetch()
      self.response.write(allBoats)

	#set a boat to "at sea"
	#manage a boat's arrival
	#need slip id, date of arrival, boat id


class SlipHandler(webapp2.RequestHandler):
  
  #add a newly created slip; current_boat = NULL (start as empty); arrival_date = NULL
  def post(self):
    #parent_key = ndb.Key(Slip, "parent_slip")
    slip_data = json.loads(self.request.body)
    new_slip = Boat(number=slip_data['number'], current_boat = NULL, arrival_date = NULL)
    new_slip.put()
    slip_dict = new_slip.to_dict()
    slip_dict['id'] = '/slip/' + new_slip.key.urlsafe()
    self.response.write(json.dumps(slip_dict))
  
  #delete a slip; sets the current_boat->id to "at_sea"
  def delete(self, id=None):
    try:
      if id:
        s = ndb.Key(urlsafe=id).get()
        #if slip is occupied
        if (s.current_boat != NULL):
          #set current_boat->id->at_sea=TRUE
          b = s.current_boat
          b.at_sea = TRUE;
          b.put()
        #delete the slip
        s.key.delete()
        self.response.write("<html><body><p>Success: Slip deleted!</p></body></html>")
    except (HTTPError, 404):
      self.response.write("<html><body><p>Bad Request. Ensure ID Values are correct.</p></body></html>")
  
  #modify/add something new to a slip's existing properties
  def patch(self, id=None):
    try:
      if id:
        # get request body
        slip_data = json.loads(self.request.body)
        # get slip in question
        s = ndb.Key(urlsafe=id).get()
        # error out if updating wrong data
        #if current_boat != NULL, arrival_date CANNOT be NULL
        if (slip_data.get('current_boat')!=NULL && slip_data.get('arrival_date')==NULL):
          self.response.write("ERROR: Must include arrival_date if current_boat is not NULL.")
        # update correct data
        else:
          if slip_data.get('number'):
            s.number = slip_data['number']
            self.response.write("Updated slip number\n")
          # Update current_boat and arrival_date here
          if slip_data.get('current_boat'):
            s.current_boat = slip_data['current_boat']
            s.arrival_date = slip_data['arrival_date']
          s.put()
          slip_dict = s.to_dict()
          self.response.write(slip_dict)
    except (HTTPError, 404):
      self.response.write("<html><body><p>Bad Request. Ensure Values are correct.</p></body></html>")
  
  #replace a slip's existing properties
  def put(self, id=None):
    try:
      if id:
        # get request body
        slip_data = json.loads(self.request.body)
        # get slip in question
        s = ndb.Key(urlsafe=id).get()
        # error out if updating wrong data
        #if current_boat != NULL, arrival_date CANNOT be NULL
        if (slip_data.get('current_boat')!=NULL && slip_data.get('arrival_date')==NULL):
          self.response.write("ERROR: Must include arrival_date if current_boat is not NULL.")
        #or if no number is given
        elif slip_data.get('number')==NULL:
          self.response.write("Slip number is REQUIRED!")
        #update correct data
        else:
          #set new number
          if slip_data.get('number'):
            s.name = slip_data['number']
            self.response.write("Replaced slip number\n")
        #set new current_boat if given
        if slip_data.get('current_boat'):
          s.current_boat = slip_data['current_boat']
          s.arrival_date = slip_data['arrival_date']
          self.response.write("Replaced slip current_boat\n")
          self.response.write("Replaced slip arrival_date\n")
        else:
          s.current_boat = null;
          s.arrival_date = null;
        s.put()
        slip_dict = s.to_dict()
        self.response.write(slip_dict)
    except (HTTPError, 404):
      self.response.write("<html><body><p>Bad Request. Ensure Values are correct.</p></body></html>")
  
  #view a slip by id; include url to current_boa
  def get(self, id=None):
    #if the id is given, view that slip (by ID)
    if id:
      s = ndb.Key(urlsafe=id).get()
      s_d = s.to_dict()
    #view all slips
    else:
      self.response.write(json.dumps(s_d))
      allSlips = Slip.query().fetch()
      self.response.write(allSlips)

class LaunchHandler(webapp2.RequestHandler):
  
  #set a boat to "at sea"; this empties slip
  def patch(self, id=None):
    try:
      if id:
        # get request body
        slip_data = json.loads(self.request.body)
        # get slip in question
        s = ndb.Key(urlsafe=id).get()
        # error out if updating wrong data
        #update correct data
        #check that slip has a boat
        if (slip_data.get('current_boat')!=NULL):
          b = s.current_boat
          b.at_sea = true;
          b.put()
          
          #free the slip
          s.current_boat = NULL
          s.arrival_date = NULL
          s.put()
          slip_dict = s.to_dict()
          self.response.write("Boat set at_sea = TRUE\n")
          self.response.write("Slip is now empty.\n")
          self.response.write(slip_dict)
        else:
          self.response.write("ERROR: Slip is ALREADY empty.\n")
    except (HTTPError, 404):
      self.response.write("<html><body><p>Bad Request. Ensure Values are correct.</p></body></html>")
  
  #manage a boat's arrival; sets a slip to full
  #need slip id, date of arrival, boat id
  def put(self, id=None):
    try:
      if id:
        # get request body
        slip_data = json.loads(self.request.body)
        # get slip in question
        s = ndb.Key(urlsafe=id).get()
        # error out if updating wrong data
        #if no boat or no arrival_date passed in, error out
        if (slip_data.get('current_boat')==NULL or slip_data.get('arrival_date')==NULL):
          self.response.write("ERROR: Must include arrival_date AND current_boat.")
        #check if slip has a boat already
        elif (s.current_boat!=NULL):
          self.response.write("ERROR: This slip is already occupied.\n")
        #update correct data
        else:
          #place the boat into the slip
          if (slip_data.get('current_boat')!= NULL):
            s.current_boat = slip_data.get('current_boat')
            s.arrival_date = slip_data.get('arrival_date')
            s.put()
          #update boat to at_sea=False
          if (slip_data.get('current_boat')!=NULL):
            b = s.current_boat
            b.at_sea = false;
            b.put()
          
          boat_dict = b.to_dict()
          slip_dict = s.to_dict()
          self.response.write("Boat set at_sea = FALSE\n")
          self.response.write("Slip is now occupied.\n")
          self.response.write(slip_dict)
          self.response.write(boat_dict)
    except (HTTPError, 404):
      self.response.write("<html><body><p>Bad Request. Ensure Values are correct.</p></body></html>")


class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write("hello Mariam")


allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/boat', BoatHandler),
    ('/boat/(.*)', BoatHandler),
    ('/slip', SlipHandler),
    ('/slip/(.*)', SlipHandler),
    ('/slip/(.*)/boat', LaunchHandler),
], debug=True)
