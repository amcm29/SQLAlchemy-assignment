# Import Dependencies
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt
import datedelta

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

# Create engine to connect to database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Create the classes 
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


# 1. import Flask
from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################

# 2. Create an app, being sure to pass __name__
# For details on this, see: http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# 3. Define what to do when a user hits the index route
# These `@app.route` lines are called "decorators" and are used to define 
# the a response for a specific URL route.

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate App!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation    Displays the last year of precipitation data for Hawaii<br/>"
        f"/api/v1.0/stations    Displays a list of the available Hawaiian weather stations from the last year<br/>"
        f"/api/v1.0/tobs    Displays the last year of temperature data for Hawaii<br/>"
        f"/api/v1.0/<start>    Displays the min, max, and avg temperatures of all dates since the selected start date.<br/>"
        f"/api/v1.0/<start>/<end>    Displays a list of the available Hawaiian weather stations from the last year<br/>")
    

# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
   print("Server received request for 'Percipitation' page...")

   date_prcp=session.query(Measurement.date, Measurement.prcp).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

   precip = {date: prcp for date,prcp in date_prcp}

   return jsonify(precip)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'Stations' page...")

    stationlist=session.query(Station.station, Station.name).filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    station_dict={}
    
    return jsonify(stationlist)

# This final if statement simply allows us to run in "Development" mode, which 
# means that we can make changes to our files and then save them to see the results of 
# the change without restarting the server.
# explanation of the line below: https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    app.run(debug=True)
