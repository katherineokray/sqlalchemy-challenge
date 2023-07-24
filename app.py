# Import the dependencies.

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


######################################################################################
# Database Setup
######################################################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
base = automap_base()

# reflect the tables
base.prepare(autoload_with=engine)

# Save references to each table
station = base.classes.station
measurement = base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

######################################################################################
# # Flask Setup
######################################################################################

app = Flask(__name__)

######################################################################################
# Flask Routes
######################################################################################

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )
######################################################################################
#Station
@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)

######################################################################################
#Precipitation station
    precipitation_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date > "2016-08-22").\
        order_by(measurement.date.desc()).all()

    session.close()
    
    precipitation_list = []
    for date, prcp in precipitation_data:
        precipitation_dict = {}
        precipitation_dict['date'] = prcp
        precipitation_list.append(precipitation_dict)
        
        return jsonify(precipitation_list)

######################################################################################
#Station List
@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    total_active_stations = session.query(measurement.station).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()

    session.close()
    
    station_list = list(np.ravel(active_stations))
    return jsonify(station_list)

######################################################################################
#Tobs

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    most_active_12_months = session.query(measurement.date, measurement.tobs).\
        filter(measurement.date > "2016-08-22").\
        filter(measurement.station == "USC00519281").all()

    session.close()

    tobs_list = []
    for date, tobs in active_12_months:
        tobs_dict = {}
        tobs_dict[date] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

######################################################################################
#min, max, and average temps for the most active station (USC00519281) (3 points)

@app.route("/api/v1.0/<start>")
def start_date(start):
    
    session = Session(engine)
    
    start_results = session.query(
        func.min(measurement.tobs),
        func.avg(measurement.tobs),
        func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()

    
    session.close() 

    start_list = []
    for date, min, avg, max in start_results:
        start_dict = {}
        start_dict["min"] = min
        start_dict["average"] = avg
        start_dict["max"] = max
        start_list.append(start_dict)
    return jsonify(start_list)

######################################################################################

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
   
    session = Session(engine)
    start = '2014-08-23'
    end = '2017-08-23'

    start_end_functions = session.query(
        func.min(measurement.tobs), 
        func.avg(measurement.tobs), 
        func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        filter(measurement.date <= end).all()
        
    session.close()
    
    start_end_list = []
    for min, avg, max in start_end_list:
        start_end_dict = {}
        start_end_dict["min_temp"] = min
        start_end_dict["avg_temp"] = avg
        start_end_dict["max_temp"] = max
        start_end_list.append(start_end_dict) 
    
    return jsonify(start_end_list)


if __name__ == '__main__':
    app.run(debug=True)