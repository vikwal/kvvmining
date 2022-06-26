from sqlm import *

rootraw = "../../Database/rawdata.db"
root = "../../Database/database.db"
target = "../../Database/database_streamlit.db"

sqlcmd.data_transfer(rootraw, root, target, "Fahrtanfragen")