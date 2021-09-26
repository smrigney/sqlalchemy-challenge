import numpy as np
import flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
station = Base.classes.station
measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    session = Session(engine)
    prcp_results = session.query(measurement.date,measurement.prcp).all()
    session.close()
    
    allprecipitation = []
    for date, prcp in prcp_results:
        prcp_dict = {}
        prcp_dict['precipitation'] = prcp
        prcp_dict['date'] = date
        allprecipitation.append(prcp_dict)
    return jsonify(allprecipitation)

@app.route('/api/v1.0/stations')
def stations():
    session = Session(engine)
    station_results = session.query(measurement.station).all()
    session.close()
    allstations = list(np.ravel(station_results))
    return jsonify(allstations)

@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    tobs_results = session.query(measurement.date,measurement.tobs).filter(measurement.station == 'USC00519281').filter(measurement.date>'2016-08-23').\
group_by(measurement.date).order_by(measurement.date.desc()).all()
    session.close()
    alltobs = list(np.ravel(tobs_results))
    return jsonify(alltobs)

if __name__ == '__main__':
    app.run(debug=True)

