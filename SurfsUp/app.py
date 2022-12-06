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
        f"/api/v1.0/precipitation<br/r>"
        f"/api/v1.0/stations<br/r>"
        f"/api/v1.0/tobs<br/r>"
        f"/api/v1.0/<start><br>"
		f"/api/v1.0<start>/<end><br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    # Create session from python to the DB
    session = Session(engine)
    # Starting from the most recent data point in the database. 
    recentdate = session.query(Measurement).order_by(Measurement.date.desc()).first()
    lastdate = dt.datetime.strptime(recentdate.date, '%Y-%m-%d').date()
    # Calculate the date one year from the last date in data set.
    lastyeardate = lastdate - dt.timedelta(days=365)
    # Perform a query to retrieve the data and precipitation scores
    precip_scores = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= lastyeardate).all()
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
    session = Session(engine)
    stationquery = session.query(Station.name, Station.station, Station.elevation).all()
    session.close()
    #create dictionary of stations
    station_list = []
    for result in stationquery:
        row = {}
        row["name"] = result[0]
        row["station"] = result[1]
        row["elevation"] = result[2]
        station_list.append(row)
    
    # Return a json list of stations
    return jsonify(station_list)
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    recentdate = session.query(Measurement).order_by(Measurement.date.desc()).first()
    lastdate = dt.datetime.strptime(recentdate.date, '%Y-%m-%d').date()
    lastyeardate = lastdate - dt.timedelta(days=365)
    tempobserved = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date >= lastyeardate).order_by(Measurement.date.desc()).all()
    session.close()
    
    #tobs_list = list(np.ravel(tempobserved))
    #creast dictionary of tobs
    tobstotal = []
    for date, temp in tempobserved:
        row = {}
        row["Date"] = date
        row["Temperature"] = temp
        tobstotal.append(row)
        
    # Return json representative of tobs dictionary
    return jsonify (tobstotal)

if __name__ == "__main__":
    app.run(debug=True)