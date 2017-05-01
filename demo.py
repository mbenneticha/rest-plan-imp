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
    new_boat.id = new_boat.key.urlsafe()
    new_boat.put()
    boat_dict = new_boat.to_dict()
    boat_dict['self'] = '/boat/' + new_boat.id
    self.response.write(json.dumps(boat_dict))

  #delete a boat
  def delete(self, id=None):
    try:
      if id:
        b = ndb.Key(urlsafe=id).get()
        #if boat is in slip
        if (b.at_sea == False):
          #get all slips
          allSlips = Slip.query().fetch()
          slip = allSlips.get()
          #empty slip with boat
          if (slip.current_boat == b.id):
            slip.current_boat = None
            slip.arrival_date = None
            slip.put()
        #delete boat
        b.key.delete()
        self.response.status = '204 Success'
        self.response.write("<html><body><p>Success: Boat deleted!</p></body></html>")
    except ValueError:
      self.response.status = '400 Bad Request'
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
            #self.response.write("Updated boat name\n")
          #set new type if given
          if boat_data.get('type'):
            b.type = boat_data['type']
            #self.response.write("Updated boat type\n")
          #set new length if given
          if boat_data.get('length'):
            b.length = boat_data['length']
            #self.response.write("Updated boat length\n")
          b.put()
          boat_dict = b.to_dict()
          self.response.write(boat_dict)
    except  ValueError:
      self.response.status = '400 Bad Request'
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
        elif boat_data.get('name')==None:
          self.response.write("Boat name is REQUIRED!")
        #update correct data
        else:
          #set new name
          if boat_data.get('name'):
            b.name = boat_data['name']
            #self.response.write("Updated boat name\n")
          #set new type if given
          if boat_data.get('type'):
            b.type = boat_data['type']
            #self.response.write("Updated boat type\n")
          else:
            b.type = None;
          #set new length if given
          if boat_data.get('length'):
            b.length = boat_data['length']
            #self.response.write("Updated boat length\n")
          else:
            b.length = None;
          b.put()
          boat_dict = b.to_dict()
          self.response.write(boat_dict)
    except ValueError:
      self.response.status = '400 Bad Request'
      self.response.write("<html><body><p>Bad Request. Ensure ID Values are correct.</p></body></html>")
  
  #view a boat
  def get(self, id=None):
    #if the id is given, view that boat (by ID)
    if id:
      b = ndb.Key(urlsafe=id).get()
      b_d = b.to_dict()
      self.response.write(json.dumps(b_d))
    #view all boats
    else:
      allBoats = Boat.query().fetch()
      allBoats_dict = []
      for boat in allBoats:
        boat_dict = boat.to_dict()
        boat_dict['self'] = '/boat/' + str(boat.id) 
        allBoats_dict.append(boat_dict)
      self.response.write(allBoats_dict)

  #set a boat to "at sea"
  #manage a boat's arrival
  #need slip id, date of arrival, boat id


class SlipHandler(webapp2.RequestHandler):
  
  #add a newly created slip; current_boat = None (start as empty); arrival_date = None
  def post(self):
    #parent_key = ndb.Key(Slip, "parent_slip")
    slip_data = json.loads(self.request.body)
    new_slip = Slip(number=slip_data['number'], current_boat = None, arrival_date = None)
    new_slip.put()
    new_slip.id = new_slip.key.urlsafe()
    new_slip.put()
    slip_dict = new_slip.to_dict()
    slip_dict['self'] = '/slip/' + new_slip.id
    self.response.write(json.dumps(slip_dict))
 
  #delete a slip; sets the current_boat->id to "at_sea"
  def delete(self, id=None):
    try:
      if id:
        s = ndb.Key(urlsafe=id).get()
        #if slip is occupied
        if (s.current_boat != None):
          #set current_boat->id->at_sea=TRUE
          b = s.current_boat
          b.at_sea = TRUE;
          b.put()
        #delete the slip
        s.key.delete()
        self.response.status = '204 Success'
        self.response.write("<html><body><p>Success: Slip deleted!</p></body></html>")
    except ValueError:
      self.response.status = '400 Bad Request'
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
        #if current_boat != None, arrival_date CANNOT be None
        if (slip_data.get('current_boat')!=None and slip_data.get('arrival_date')==None):
          self.response.write("ERROR: Must include arrival_date if current_boat is not None.")
        # update correct data
        else:
          if slip_data.get('number'):
            s.number = slip_data['number']
            #s.put()
            #self.response.write("Updated slip number\n")
          # Update current_boat and arrival_date here
          if slip_data.get('current_boat'):
            s.current_boat = slip_data['current_boat']
            s.arrival_date = slip_data['arrival_date']
            b = ndb.Key(urlsafe=s.current_boat).get()
            b.at_sea = False;
            b.put()
            #s.put()
            #slip_dict = s.to_dict()
            #slip_dict['Current Boat'] = '/slip/' + s.current_boat
          s.put()
          slip_dict = s.to_dict()
          slip_dict['Current Boat'] = '/slip/' + s.current_boat
          self.response.write(slip_dict)
    except ValueError:
      self.response.status = '400 Bad Request'
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
        #if current_boat != None, arrival_date CANNOT be None
        if (slip_data.get('current_boat')!=None and slip_data.get('arrival_date')==None):
          self.response.write("ERROR: Must include arrival_date if current_boat is not NONE.")
        #or if no number is given
        elif slip_data.get('number')==None:
          self.response.write("Slip number is REQUIRED!")
        #update correct data
        else:
          #set new number
          if slip_data.get('number'):
            s.number = slip_data['number']
            s.put()
            if s.current_boat != None:
              b = ndb.Key(urlsafe=s.current_boat).get()
              b.at_sea = True
              b.put()
              s.current_boat = None
              s.arrival_date = None
              s.put()
            #self.response.write("Replaced slip number\n")
        #set new current_boat if given
        if slip_data.get('current_boat'):
          s.current_boat = slip_data['current_boat']
          s.arrival_date = slip_data['arrival_date']
          self.response.write("Replaced slip current_boat\n")
          self.response.write("Replaced slip arrival_date\n")
        s.put()
        slip_dict = s.to_dict()
        slip_dict['Current Boat'] = '/slip/' + s.current_boat
        self.response.write(slip_dict)
    except ValueError:
      self.response.status = '400 Bad Request'
      self.response.write("<html><body><p>Bad Request. Ensure Values are correct.</p></body></html>")
  
  #view a slip by id; include url to current_boa
  def get(self, id=None):
    #if the id is given, view that slip (by ID)
    if id:
      s = ndb.Key(urlsafe=id).get()
      s_d = s.to_dict()
      self.response.write(json.dumps(s_d))
    #view all slips
    else:
      allSlips = Slip.query().fetch()
      allSlips_dict = []
      for slip in allSlips:
        slip_dict = slip.to_dict()
        slip_dict['self'] = '/slip/' + str(slip.id) 
        allSlips_dict.append(slip_dict)
      self.response.write(allSlips_dict)

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
        if (slip_data.get('current_boat')!=None):
          b = s.current_boat
          b.at_sea = True;
          b.put()
          
          #free the slip
          s.current_boat = None
          s.arrival_date = None
          s.put()
          slip_dict = s.to_dict()
          self.response.write("Boat set at_sea = TRUE\n")
          self.response.write("Slip is now empty.\n")
          self.response.write(slip_dict)
        else:
          self.response.status = '403 Forbidden'
          self.response.write("ERROR: Slip is ALREADY empty.\n")
    except ValueError:
      self.response.status = '400 Bad Request'
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
        if (slip_data.get('current_boat')==None or slip_data.get('arrival_date')==None):
          self.response.write("ERROR: Must include arrival_date AND current_boat.")
        #check if slip has a boat already
        elif (s.current_boat!=None):
          self.response.write("ERROR: This slip is already occupied.\n")
        #update correct data
        else:
          #place the boat into the slip
          if (slip_data.get('current_boat')!= None):
            s.current_boat = slip_data.get('current_boat')
            s.arrival_date = slip_data.get('arrival_date')
            s.put()
          #update boat to at_sea=False
          if (slip_data.get('current_boat')!=None):
            b = s.current_boat
            b.at_sea = False;
            b.put()
          
          boat_dict = b.to_dict()
          slip_dict = s.to_dict()
          self.response.write("Boat set at_sea = FALSE\n")
          self.response.write("Slip is now occupied.\n")
          self.response.write(slip_dict)
          self.response.write(boat_dict)
    except ValueError:
      self.response.status = '400 Bad Request'
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
