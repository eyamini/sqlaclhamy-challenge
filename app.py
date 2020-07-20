import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        f"Available Routes:"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]"
        
        
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Last Year of Percipitation Data"""
    session = Session(engine)
    """Return a list of all Precipitation Data"""
    results = session.query(measurement.date,measurement.prcp).\
                order_by(measurement.date).all()
    
    session.close()

    precip = list(np.ravel(results))
    
    precip = {precip[i]: precip[i + 1] for i in range(0, len(precip), 2)} 

    return jsonify(precip)
        

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    results = session.query(Station.station).\
                 order_by(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations)
 
        
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(measurement.date,  measurement.tobs).\
                filter(measurement.date >= '2016-08-23').\
                    order_by(measurement.date).all()

    session.close()

    tob = list(np.ravel(results))

    tob = {tob[i]: tob[i + 1] for i in range(0, len(tob), 2)} 

    return jsonify(tob)       

        
@app.route("/api/v1.0/<start_date>")
def data_start_date(start_date):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).all()

    session.close()

    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_db = {}
        start_date_tobs_db["min_temp"] = min
        start_date_tobs_db["avg_temp"] = avg
        start_date_tobs_db["max_temp"] = max
        start_date_tobs.append(start_date_tobs_db)     
        
 return jsonify(start_date_tobs)
        
        
@app.route("/api/v1.0/<start_date>/<end_date>")
def data_start_end_date(start_date, end_date):
    session = Session(engine)

    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    session.close()

    start_end_date_tobs = []
    for min, avg, max in results:
        start_end_date_tobs_db = {}
        start_end_date_tobs_db["min_temp"] = min
        start_end_date_tobs_db["avg_temp"] = avg
        start_end_date_tobs_db["max_temp"] = max
        start_end_date_tobs.append(start_end_date_tobs_db) 
    

    return jsonify(start_end_date_tobs)  
        
        


if __name__ == '__main__':
    app.run(debug=True)
