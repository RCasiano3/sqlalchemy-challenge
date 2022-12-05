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

# Create session from python to the DB
session = Session(engine)

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
    yearprcp = list.np(ravel(precip_scores))
    
    year_rain = []
    for date, prcp in yearprcp:
        raindata = {}
        raindata["date"] = date
        raindata["prcp"] = prcp
        year_rain.append(raindata)
    
    # Return a json representation of dictionary
    return jsonify(year_rain)

@app.route("/api/v1.0/stations")
def stations():
    
@app.route("/api/v1.0/tobs")
def tobs():


if __name__ == "__main__":
    app.run(debug=True)