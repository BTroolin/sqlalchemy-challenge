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

#base.prepare(engine, reflect=True)

#measurement = base.classes.measurement