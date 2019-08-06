###################################################################################################
# import dependencies 
import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Hawaii.sqlite")
# reflect the database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
#session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Climate App<br/>"
        f"<br/>"
        f"<br/>"

        f"Available Routes:<br/>"
        f"<br/>"

        f"/api/v1.0/precipitation<br/>"
        f"- JSON list of last year's precipitation data<br/>"
        f"<br/>"

        f"/api/v1.0/stations<br/>"
        f"- JSON list of station data<br/>"
        f"<br/>"

        f"/api/v1.0/tobs<br/>"
        f"- JSON list of temperature observation data from the stations<br/>"
        f"<br/>"

        f"/api/v1.0/start<br/>"
        f"- JSON list of the minimum, average and maximum temperature when given the start date only (YYYY-MM-DD), for dates greater than and equal to the start date<br/>"
        f"<br/>"

        f"/api/v1.0/start/end<br/>"
        f"- JSON list of the minimum, average and maximum temperature when given the start and end dates (YYYY-MM-DD) for dates between the start and end date inclusive:<br/>"
        f"<br/>"

    )
#########################################################################################
#################################################
# * `/api/v1.0/precipitation`
#   * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value
#   * Return the JSON representation of your dictionary
#################################################
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    prcp = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date).\
        order_by(Measurement.date).all()


# Create a list of dicts with `date` and `prcp` as the keys and values
    prcp_totals = []
    for result in prcp:
        row = {}
        row["date"] = prcp[0]
        row["prcp"] = prcp[1]
        prcp_totals.append(row)

    return jsonify(prcp_totals)

#########################################################################################
#################################################
# * `/api/v1.0/stations`
#   * Return a JSON list of stations from the dataset
#################################################
@app.route("/api/v1.0/stations")
def stations():
    #create the session (link) from Python to the DB:
    session = Session(engine)

    stations_query = session.query(Station.name, Station.station)
    stations = pd.read_sql(stations_query.statement, stations_query.session.bind)

    return jsonify(stations.to_dict())    

#########################################################################################
#################################################
# * `/api/v1.0/tobs`
#   * query for the dates and temperature observations from a year from the last data point
#   * Return a JSON list of Temperature Observations (tobs) for the previous year
#################################################
@app.route("/api/v1.0/tobs")
def tobs():
    
    #create the session (link) from Python to the DB:
    session = Session(engine)

#    * Query for the dates and temperature observations from the last year.
#           * Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
#           * Return the json representation of your dictionary.
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperatures = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date > one_year_ago).\
        order_by(Measurement.date).all()

# Create a list of dicts with `date` and `tobs` as the keys and values
    temperatures_total = []
    for result in temperatures:
        row = {}
        row["date"] = temperatures[0]
        row["tobs"] = temperatures[1]
        temperatures_total.append(row)

    return jsonify(temperatures_total)
#########################################################################################
#################################################
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
#   * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date
#################################################
@app.route("/api/v1.0/<start>")
def trip1(start):
    #create the session (link) from Python to the DB:
    session = Session(engine)

    temp = [func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)]
    trip_data = session.query(*temp).filter(Measurement.date >= start)
    session.query(*temp).filter(Measurement.date >= start, Measurement.date)

    start_end_input = []
    for tmin, tavg, tmax in trip_data:
        input_dict = {}
        input_dict["min"] = tmin
        input_dict["avg"] = tavg
        input_dict["max"] = tmax
        start_end_input.append(input_dict)

    print(start_end_input)
    return jsonify(start_end_input)

#########################################################################################
#################################################
#   * Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range
#   * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive
#################################################
@app.route("/api/v1.0/<start>/<end>")
def trip2(start,end):
    #create the session (link) from Python to the DB:
    session = Session(engine)

    
    temp = [func.min(Measurement.tobs),
            func.max(Measurement.tobs),
            func.avg(Measurement.tobs)]
    trip_data = session.query(*temp).filter(Measurement.date <= end)
    session.query(*temp).filter(Measurement.date >= start, Measurement.date <= end)

    start_end_input = []
    for tmin, tavg, tmax in trip_data:
        input_dict = {}
        input_dict["min"] = tmin
        input_dict["avg"] = tavg
        input_dict["max"] = tmax
        start_end_input.append(input_dict)

    print(start_end_input)
    return jsonify(start_end_input)

#########################################################################################

if __name__ == "__main__":
    app.run(debug=True)

###################################################################################################