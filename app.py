import numpy as np
import flask
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime

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
        f"/api/v1.0/(enter start date YYYY-MM-DD)<br/>"
        f"/api/v1.0/(enter start date YYYY-MM-DD)/ (enter end date YYYY-MM-DD)<br/>"
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

@app.route('/api/v1.0/<start>')
def startdate(start):
    strt = datetime.strptime(start, "%Y-%m-%d").date()
    session = Session(engine)
    mostactivemin = session.query(func. min(measurement.tobs)).\
        filter((measurement.date >= strt)&(measurement.\
            station == 'USC00519281')).all()
    mostactivemax = session.query(func. max(measurement.tobs)).\
        filter((measurement.date >= strt)&(measurement.\
            station == 'USC00519281')).all()
    mostactiveavg = session.query(func. avg(measurement.tobs)).\
        filter((measurement.date >= strt)&(measurement.\
            station == 'USC00519281')).all()
    session.close()
    minmaxavg = mostactivemin, mostactivemax, mostactiveavg
    allstartdate = list(np.ravel(minmaxavg))
    return jsonify(allstartdate)

@app.route('/api/v1.0/<start>/<end>')
def startenddate(start,end):
    strt = datetime.strptime(start, "%Y-%m-%d").date()
    ed = datetime.strptime(end, "%Y-%m-%d").date()
    session = Session(engine)
    mostactivemin = session.query(func. min(measurement.tobs)).\
        filter((measurement.date >= strt)&(measurement.date <= ed)&\
            (measurement.station == 'USC00519281')).all()
    mostactivemax = session.query(func. max(measurement.tobs)).\
        filter((measurement.date >= strt)&(measurement.date <= ed)&\
            (measurement.station == 'USC00519281')).all()
    mostactiveavg = session.query(func. avg(measurement.tobs)).\
        filter((measurement.date >= strt)&(measurement.date <= ed)&\
            (measurement.station == 'USC00519281')).all()
    session.close()
    minmaxavg = mostactivemin, mostactivemax, mostactiveavg
    allstartend = list(np.ravel(minmaxavg))
    return jsonify(allstartend)


if __name__ == '__main__':
    app.run(debug=True)

