import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import pandas as pd
import datetime as dt
from datetime import datetime

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the SurfsUp API for Hawaii<br/>"
        f"Available routes:<br/r>"
        f"Measurements for Precipitation: /api/v1.0/precipitation<br/r>"
        f"List of Stations: /api/v1.0/stations<br/r>"
        f"Prior year temparature observations for highest activity station: /api/v1.0/tobs<br/r>"
        f"Temperature for specific date provided in following format (YYYY-MM-DD) at end of APP: /api/v1.0/start<br/r>"
        f"Temperature for specific dates provided in following format (YYYY-MM-DD)/(YYYY-MM-DD) at end of APP: /api/v1.0/start/end<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create session from python to the DB
    session = Session(engine)
    # Starting from the most recent data point in the database. 
    recent_date = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(recent_date.date, '%Y-%m-%d').date()
    # Calculate the date one year from the last date in data set.
    last_year_date = last_date - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    precip_scores = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year_date).all()
    session.close()
    # Creat a dictionary using date and prcp 
    
    year_rain = []
    for date, prcp in precip_scores:
        raindata = {}
        raindata["date"] = date
        raindata["prcp"] = prcp
        year_rain.append(raindata)
    
    # Return a json representation of dictionary
    return jsonify(year_rain)

@app.route("/api/v1.0/stations")
def stations():
    # Create a session from python to the DB
    session = Session(engine)
    station_query = session.query(Station.name, Station.station, Station.elevation).all()
    session.close()
    #create dictionary of stations
    station_list = []
    for name, station, elevation in station_query:
        row = {}
        row["name"] = name
        row["station"] = station
        row["elevation"] = elevation
        station_list.append(row)
    
    # Return a json list of stations
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session from python to the DB
    session = Session(engine)
    # Starting from the most recent data point in the database. 
    recent_date = session.query(Measurement).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(recent_date.date, '%Y-%m-%d').date()

    # Calculate the date one year from the last date in data set.
    last_year_date = last_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    tobs_total = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_year_date).all()
    
    # Close Session
    session.close()

    # Create a list of dictionaries with the date and temperature with for loop
    all_temp = []
    for date, temp in tobs_total:
        temp_info = {}
        temp_info['Date'] = date
        temp_info['Temperature'] = temp
        all_temp.append(temp_info)

    return jsonify(all_temp)
    
    
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create session from python to the DB
    session = Session(engine)
    # Start date variable
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    # Query to retrieve the  start date information   
    start_measurement = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start_date).all()
    session.close()  
    
    tobs_start = []

    for min,avg,max in start_measurement:

        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_start.append(tobs_dict)
    
    return jsonify(tobs_start)

@app.route('/api/v1.0/<start>/<end>')

def start_end(start,end):

    session = Session(engine)

    queryresult = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()
    
    tobs_start_end = []

    for min,avg,max in queryresult:

        tobs_dict = {}
        tobs_dict["Min"] = min
        tobs_dict["Average"] = avg
        tobs_dict["Max"] = max
        tobs_start_end.append(tobs_dict)

    return jsonify(tobs_start_end)

if __name__ == "__main__":
    app.run(debug=True)