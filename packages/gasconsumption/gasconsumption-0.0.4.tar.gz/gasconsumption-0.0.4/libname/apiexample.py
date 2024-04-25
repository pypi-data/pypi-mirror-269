

#Import Analysis function from fastapiwrapper file
from fastapiwrapper import Analysis

#To access the database, it's necessary to provide both the username and password.
analysis = Analysis(username= "ahmadriad2@gmail.com", password="12345678")

#If you specify the desired curves, you'll view only those. Otherwise, 
# you'll access all the curves allowed for your access.
deftable = analysis.DefTable(curveid=[1,2])
print(deftable)

#When executed, this function retrieves a time-series table. You have the flexibility to specify the curve ID,
# start date, and end date parameters to filter the dataset according to your requirements.
timetable= analysis.TimeSeries(curveid=[1,2],startdate='2023-12-18', enddate='2023-12-20')


