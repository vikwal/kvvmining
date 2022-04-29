from sqlm import *
from datetime import datetime, timedelta

rootraw = "../../Database/rawdata.db"
root = "../../Database/database.db"

sqlcmd.data_transfer(rootraw, root, "Fahrtanfragen")