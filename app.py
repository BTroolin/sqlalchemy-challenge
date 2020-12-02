#dependencies

import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# set up database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#reflect db to find structure
base = automap_base()
base.prepare(engine, reflect=True)

base.classes.keys()

measurement = base.classes.measurement
station = base.classes.station

## Flask Setup ##

app = Flask(__name__)

# Add Flask Routes

@app.route("/")
def welcome():
    return(
        f"<h1>API Routes for Hawaii Climate Data:</h1><br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"List of Stations: /api/v1.0/stations<br/>"
        f"Temperature: /api/v1.0/tobs<br/>"
        f"Temperature from start date: /api/v1.0/<start><br/>"
        f"Temperature from start to end dates: /api/v1.0/<start>/<end><br/>"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    selection = [measurement.date,measurement.prcp]
    query = session.query(*selection).all()
    
    # Close session in case of high server traffic
    session.close()
    # Return the JSON representation of your dictionary.
    precipitation = []
    for date, prcp in query:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precipitation.append(precip_dict)

    return jsonify(precipitation)

if __name__ == '__main__':
    app.run(debug=True)



@app.route("/api/v1.0/stations")
def stations(): 
    session = Session(engine)
    selection = [station.station,station.name,station.latitude,station.longitude,station.elevation]
    query = session.query(*selection).all()
    session.close()

    #return stations as json
    stations = []
    for station,name,lat,lon,el in query:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Lat"] = lat
        station_dict["Lon"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(measurement.date, measurement.tobs, measurement.prcp).\
                filter(measurement.date >= '2016-08-23').\
                filter(measurement.station=='USC00519281').\
                order_by(measurement.date).all()
    
    session.close()

    temp_dates = []

    for date, tobs in results:
        date_dict = {}
        date_dict[date] = date
        date_dict[tobs] = tobs

        temp_dates.append(date_dict)

    return jsonify(temp_dates)

@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).all()
    session.close()

    # create dictionary and append data
    start = []
    for min, avg, max in results:
        start_dict = {}
        start_dict["Mimimum Temp"] = min
        start_dict["Average Temp"] = avg
        start_dict["Maximum Temp"] = max
        start.append(start_dict)
    return jsonify(start)

#@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start_date, end_date):
    session = Session(engine)

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    start_end = []

    for min, avg, max in results:
        start_end_dict = {}
        start_end_dict["Mimimum Temp"] = min
        start_end_dict["Average Temp"] = avg
        start_end_dict["Maximum Temp"] = max
        start_end.append(start_end_dict)

    return jsonify(start_end)

if __name__=='__main__':
    app.run(debug=True)