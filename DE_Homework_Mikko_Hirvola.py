#light sqlite for storing data for the homework
import sqlite3

#task 2 testing
import pytest

#purely to clean up after us and remove the temp db
import os

#plotter for task 3 analysis
import matplotlib.pyplot as plot

#datetime to weekday conversion for task 3
import datetime

#dataframes for same reason
import pandas

#task 3 onwards
import numpy

#loading bonus task file
import pickle
import joblib

#Cleaning created files
import os

def prepare():
    try:
        #Creating gym table
        SQL_Connection = sqlite3.connect("./tmpsqlite")
        SQL_Cursor = SQL_Connection.cursor()
        print("Preparing sqlite.")
        SQL_Cursor.execute('''
create table if not exists hietaniemi_data(
timestamp text,
etupenkki integer,
ojentapunnerrus integer,
vinopenkkipunnerrus integer,
hauiskaanto integer,
penkkipunnerrus integer,
yloveto integer,
jalkakyykky integer,
soutulaite integer)
''')
        #read file and insert to db
        print("Inserting gym data to sql.")
        with open("hietaniemi-gym-data.csv", "r") as hietaniemi:
            next(hietaniemi)
            for l in hietaniemi:
                SQL_Cursor.execute('''
insert into hietaniemi_data(timestamp, etupenkki, ojentapunnerrus, vinopenkkipunnerrus, hauiskaanto, penkkipunnerrus, yloveto, jalkakyykky, soutulaite) 
                values ("''' + l[:-1].replace(',','","') + '''")''')
        print("Aggregating data.")
        SQL_Cursor.execute('''
create table if not exists hietaniemi_data_aggregated as 
        select substr(timestamp, 0, 14) as timestamp, sum(etupenkki) as etupenkki, sum(ojentapunnerrus) as ojentapunnerrus, 
sum(vinopenkkipunnerrus) as vinopenkkipunnerrus, sum(hauiskaanto) as hauiskaanto, sum(penkkipunnerrus) as penkkipunnerrus, sum(yloveto) as yloveto, sum(jalkakyykky) as jalkakyykky, 
sum(soutulaite) as soutulaite 
        from hietaniemi_data group by substr(timestamp, 0, 14)''')
        SQL_Cursor.execute('''commit''')

        #Creating weather table
        print("Inserting weather data to sql.")
        SQL_Cursor.execute('''
create table if not exists kaisaniemi_data(
Year integer,
Month integer,
Day integer,
Hour integer,
Timezone text,
Precipitation real,
Snow_depth real,
Temperature real)
''')
        #read file and insert to db
        with open("kaisaniemi-weather-data.csv", "r") as kaisaniemi:
            next(kaisaniemi)
            for l in kaisaniemi:
                SQL_Cursor.execute('''
                insert into kaisaniemi_data(Year, Month, Day, Hour, Timezone, Precipitation, Snow_depth, Temperature)
                values ("''' + l[:-1].replace(',','","') + '''")''')
        SQL_Cursor.execute('''commit''')

    except (sqlite3.Error, IOError) as e:
        print(e)

def task_1():
    #Simply open the db connection and fetch data from the prepared db table
    sql = None
    try:
        SQL_Connection = sqlite3.connect("./tmpsqlite")
        SQL_Cursor = SQL_Connection.cursor()
        print("Data sample:")
        SQL_Cursor.execute('''
select timestamp, etupenkki, ojentapunnerrus, vinopenkkipunnerrus, hauiskaanto, penkkipunnerrus, yloveto, jalkakyykky, soutulaite 
from hietaniemi_data_aggregated
limit 10''')
        for dbrow in SQL_Cursor.fetchall():
            print(dbrow)
    except (sqlite3.Error) as e:
        print(e)

def task_2_a():
    try:
        SQL_Connection = sqlite3.connect("./tmpsqlite")
        SQL_Cursor = SQL_Connection.cursor()
        Rowcount = SQL_Cursor.execute('''select count(*) from hietaniemi_data''')
        return Rowcount.fetchone()[0]
    except (sqlite3.Error) as e:
        print(e)
        return -1

def task_2_b():
    try:
        SQL_Connection = sqlite3.connect("./tmpsqlite")
        SQL_Cursor = SQL_Connection.cursor()
        Rowcount = SQL_Cursor.execute('''select count(*) from hietaniemi_data where timestamp < "2020-04-24 00" or timestamp > "2021-05-11 23"''')
        return Rowcount.fetchone()[0]
    except (sqlite3.Error) as e:
        print(e)
        return -1

def task_2_c():
    try:
        SQL_Connection = sqlite3.connect("./tmpsqlite")
        SQL_Cursor = SQL_Connection.cursor()
        Rowcount = SQL_Cursor.execute('''select count(*) from hietaniemi_data where etupenkki < 0 or ojentapunnerrus < 0 or vinopenkkipunnerrus < 0 or hauiskaanto < 0 or penkkipunnerrus < 0 or yloveto < 0 or jalkakyykky < 0 or jalkakyykky <0 or soutulaite < 0''')
        return Rowcount.fetchone()[0]
    except (sqlite3.Error) as e:
        print(e)
        return -1


def test_task_2_a():
    assert task_2_a() >= 50000

def test_task_2_b():
    assert task_2_b() == 0

def test_task_2_c():
    assert task_2_c() == 0

def task_3():
    try:
        SQL_Connection = sqlite3.connect("./tmpsqlite")
        SQL_Cursor = SQL_Connection.cursor()

        #What was the most popular device during the tracking period measured by number of minutes used?
        Usage = SQL_Cursor.execute('''select sum(etupenkki) as etupenkki, sum(ojentapunnerrus) as ojentapunnerrus, 
sum(vinopenkkipunnerrus) as vinopenkkipunnerrus, sum(hauiskaanto) as hauiskaanto, sum(penkkipunnerrus) as penkkipunnerrus, sum(yloveto) as yloveto, sum(jalkakyykky) as jalkakyykky, 
sum(soutulaite) as soutulaite from hietaniemi_data_aggregated''')
        First_element = lambda arr : arr[0]
        Columns = list(map(First_element, Usage.description))
        Usage_amounts = list(Usage.fetchone())
        Device = Usage_amounts.index(max(Usage_amounts))
        print("Most popular device was: " + Columns[Device])

        #plot the data out
        plot.clf()
        plot.bar(Columns,Usage_amounts)
#        plot.xlabel("Device")
        plot.ylabel("Minutes")
        plot.savefig("total_minutes.png")

        #Did time of day (hour) impact overall popularity of the outdoor gym?
        Usage = SQL_Cursor.execute('''select substr(timestamp, -2, 2) as hour, sum(etupenkki) + sum(ojentapunnerrus) + sum(vinopenkkipunnerrus) + sum(hauiskaanto) + sum(penkkipunnerrus) + sum(yloveto) + sum(jalkakyykky) + sum(soutulaite) as total_usage 
from hietaniemi_data_aggregated group by substr(timestamp, -2, 2)''')
        Hours = []
        Minutes = []
        for dbrow in Usage.fetchall():
            Hours.append(dbrow[0])
            Minutes.append(dbrow[1])
        print("Most popular hour was " + Hours[Minutes.index(max(Minutes))] + " with " + str(Minutes.index(max(Minutes))))
        print("Least popular hour was " + Hours[Minutes.index(min(Minutes))] + " with " + str(Minutes.index(min(Minutes))))

        #plot the data out
        plot.clf()
        plot.bar(Hours,Minutes)
        plot.xlabel("Hour")
        plot.ylabel("Minutes")
        plot.savefig("per_hour.png")

        #Was the gym more popular overall on weekends (Saturday and Sunday) than on weekdays?
        #Get data to df instead of sqlite for wider functionality
        Usage_df = pandas.read_sql_query('''select substr(timestamp, 0, 11) as day, sum(etupenkki) + sum(ojentapunnerrus) + sum(vinopenkkipunnerrus) + sum(hauiskaanto) + sum(penkkipunnerrus) + sum(yloveto) + sum(jalkakyykky) + sum(soutulaite) as total_usage 
        from hietaniemi_data_aggregated group by substr(timestamp, 0, 11)''', SQL_Connection)
        Weekday_lmd = lambda day : datetime.datetime.strptime(day, "%Y-%m-%d").weekday()
        Usage_df["weekday"] = list(map(Weekday_lmd, Usage_df["day"]))

        #Clean unnecessary stuff and aggregate
        Usage_df = Usage_df.drop(columns=["day"])
        Usage_per_day = Usage_df.groupby(["weekday"]).agg("sum").reset_index().values

        #I couldnt get numpy array to give me correct values so naive solution to not waste time on that
        Dayname_enum = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        max_usage = [-1, -1]
        min_usage = [-1, -1]
        Usage_amounts = []
        for i in Usage_per_day:
            if(i[1] > max_usage[1]):
               max_usage = i
            if((i[1] < min_usage[1]) or (min_usage[1] == -1)):
               min_usage = i
            Usage_amounts.append(i[1])
               
        print("Most popular weekday is " + Dayname_enum[max_usage[0]] + " with " + str(max_usage[1]) + " total minutes")
        print("Least popular weekday is " + Dayname_enum[min_usage[0]] + " with " + str(min_usage[1]) + " total minutes")

        #plot the data out
        plot.clf()
        plot.bar(Dayname_enum,Usage_amounts)
#        plot.xlabel("Day")
        plot.ylabel("Minutes")
        plot.savefig("per_day.png")
        
    except (sqlite3.Error, OSError) as e:
        print(e)
        return -1

def task_4():
    #Weekday as number
    #We pretty much did this in the task 3 already, but lets redo it as a part of the orignal dataset
    Raw_gym_data = pandas.read_csv("hietaniemi-gym-data.csv")
    Weekday_lmd = lambda day : datetime.datetime.strptime(day[0:10], "%Y-%m-%d").weekday()
    Raw_gym_data["weekday"] = list(map(Weekday_lmd, Raw_gym_data["time"]))
    
    #Hour as number
    Hour_lmd = lambda day : int(day[11:13])
    Raw_gym_data["hour"] = list(map(Hour_lmd, Raw_gym_data["time"]))
    
    #Sum of minutes across all gym devices
    Raw_gym_data["total"] = Raw_gym_data["19"] + Raw_gym_data["20"] + Raw_gym_data["21"] + Raw_gym_data["22"] + Raw_gym_data["23"] + Raw_gym_data["24"] + Raw_gym_data["25"] + Raw_gym_data["26"]
    Raw_gym_data.to_csv("hietaniemi-gym-data-enriched.csv")

    print("Results are in hietanieme-gym-enriched.csv")
    
def task_5():
    #open db connection and prepare the db
    sql = None
    try:
        SQL_Connection = sqlite3.connect("./tmpsqlite")
        SQL_Cursor = SQL_Connection.cursor()
        #Starting the analysis
        #Does temperature impact gym popularity?
        #We will ignore data points that do not have matching pair from both sides or where temperature is missing
        SQL_Cursor.execute('''
        select max(Temperature) as Max_Temperature, min(Temperature) as Min_Temperature
        from kaisaniemi_data where Temperature != ""''')
        vals = SQL_Cursor.fetchone()
        #calculate our Temperature range
        map_width = int(vals[0]*10-vals[1]*10+1)
        #prepare zero array for the heatmap based on 24 hours and our temperature range
        heat_base = numpy.zeros((map_width,24))

        SQL_Cursor.execute('''
        select k.Temperature as Temperature, substr(k.Hour,0,3),
        (sum(h.etupenkki) + sum(h.ojentapunnerrus) + sum(h.vinopenkkipunnerrus) + sum(h.hauiskaanto) + sum(h.penkkipunnerrus) + sum(h.yloveto) + sum(h.jalkakyykky) + sum(h.soutulaite))/count(*) as gym_utilisation
from hietaniemi_data_aggregated h
inner join kaisaniemi_data k on (h.timestamp = k.Year || '-' || substr('00' || k.Month, -2, 2) || '-' || substr('00' || k.Day, -2, 2) || ' ' || substr(k.Hour,0,3))
where k.Temperature != ""
        group by substr(k.Hour,0,3), k.Temperature''')
        #conversion to real will give us minimal amount of inaccuracy, but it is not significant as the data has already been anonymized/heavily skewed with less gym utilisation
        for dbrow in SQL_Cursor.fetchall():
            #assign datapoints to heatmap
            heat_base[int((dbrow[0]-vals[1])*10)][int(dbrow[1])] = dbrow[2]
        #plot the data out
        plot.clf()
        plot.imshow(heat_base, cmap='hot', interpolation='nearest')
        plot.xlabel("Time")
        plot.ylabel("Temperature")
        plot.savefig("temperature_effect.png")
        
        #What about precipitation?
        #We will do the exact same task, but with different field
        #We will ignore data points that do not have matching pair from both sides or where precipitation is missing
        SQL_Cursor.execute('''
        select max(Precipitation) as Max_Precipitation, min(Precipitation) as Min_Precipitation
        from kaisaniemi_data where Precipitation != ""''')
        vals = SQL_Cursor.fetchone()
        #calculate our Precipitation range
        map_width = int(vals[0]*10-vals[1]*10+1)
        #prepare zero array for the heatmap based on 24 hours and our temperature range
        heat_base = numpy.zeros((map_width,24))

        SQL_Cursor.execute('''
        select k.Precipitation as Precipitation, substr(k.Hour,0,3),
        (sum(h.etupenkki) + sum(h.ojentapunnerrus) + sum(h.vinopenkkipunnerrus) + sum(h.hauiskaanto) + sum(h.penkkipunnerrus) + sum(h.yloveto) + sum(h.jalkakyykky) + sum(h.soutulaite))/count(*) as gym_utilisation
from hietaniemi_data_aggregated h
inner join kaisaniemi_data k on (h.timestamp = k.Year || '-' || substr('00' || k.Month, -2, 2) || '-' || substr('00' || k.Day, -2, 2) || ' ' || substr(k.Hour,0,3))
where k.Precipitation != ""
        group by substr(k.Hour,0,3), k.Precipitation''')
        #conversion to real will give us minimal amount of inaccuracy, but it is not significant as the data has already been anonymized/heavily skewed with less gym utilisation
        for dbrow in SQL_Cursor.fetchall():
            #assign datapoints to heatmap
            heat_base[int((dbrow[0]-vals[1])*10)][int(dbrow[1])] = dbrow[2]
        #plot the data out
        plot.clf()
        plot.imshow(heat_base, cmap='hot', interpolation='nearest')
        plot.xlabel("Time")
        plot.ylabel("Precipitation")
        plot.savefig("precipitation_effect.png")

        print("Effects of precipitation and temparature to usage can be seen in precipitation_effect.png and temperature_effect.png respectively")

    except (sqlite3.Error, IOError) as e:
        print(e)



def task_bonus():
    #this could be done easier by using the products of previous tasks, but as some of them have done with different approaches,
    #we will redo task 4 columns to only weather data

    #load the dataset
    Weather_data = pandas.read_csv("kaisaniemi-weather-data.csv")
    
    #add the missing columns
    Hour_lmd = lambda hour : int(hour[0:2])
    Weather_data["hour"] = list(map(Hour_lmd, Weather_data["Hour"]))
    Weekday_lmd = lambda year,month,day : datetime.datetime.strptime(str(year)+str(month).zfill(2)+str(day).zfill(2), "%Y%m%d").weekday()
    Weather_data["weekday"] = list(map(Weekday_lmd, Weather_data["Year"], Weather_data["Month"], Weather_data["Day"]))

    #drop the unnecessary columns and reorder the rest
    Weather_data = Weather_data.drop(columns=["Year", "Month", "Day", "Timezone", "Hour"])
    Weather_data = Weather_data.reindex(columns = ["weekday","hour","Precipitation (mm)","Snow depth (cm)","Temperature (degC)"])

    #drop rows with broken data
    Weather_data = Weather_data.dropna()
    
    #loading the model
    Model_file = open("model.pkl", "rb")
    Model = joblib.load(Model_file)

    #running the model with our dataset
    Weather_data["prediction"] = Model.predict(Weather_data)

    #create similar graphs as in task 5
    #----
    #get size of the heatmap
    Valmax = Weather_data["Temperature (degC)"].max()
    Valmin = Weather_data["Temperature (degC)"].min()
    #calculate our Temperature range
    map_width = int(Valmax*10-Valmin*10+1)
    #prepare zero array for the heatmap based on 24 hours and our temperature range
    heat_base = numpy.zeros((map_width,24))

    
    #at this point I'm starting to run out of time, so we do the conversion via naive looping way
    Result_data = Weather_data.to_numpy()
    for i in Result_data:
        heat_base[int((i[4]-Valmin)*10)][int(i[1])] = i[5]
    plot.clf()
    plot.imshow(heat_base, cmap='hot', interpolation='nearest')
    plot.xlabel("Time")
    plot.ylabel("Temperature")
    plot.savefig("temperature_effect_forecast.png")
    
    #----
    #get size of the heatmap
    Valmax = Weather_data["Precipitation (mm)"].max()
    Valmin = Weather_data["Precipitation (mm)"].min()
    #calculate our Precipitation range
    map_width = int(Valmax*10-Valmin*10+1)
    #prepare zero array for the heatmap based on 24 hours and our temperature range
    heat_base = numpy.zeros((map_width,24))

    
    #at this point I'm starting to run out of time, so we do the conversion via naive looping way
    Result_data = Weather_data.to_numpy()
    for i in Result_data:
        heat_base[int((i[2]-Valmin)*10)][int(i[1])] = i[5]
    plot.clf()
    plot.imshow(heat_base, cmap='hot', interpolation='nearest')
    plot.xlabel("Time")
    plot.ylabel("Precipitation")
    plot.savefig("precipitation_effect_forecast.png")

    print("Forecasted effects of precipitation and temparature to usage can be seen in precipitation_effect_forecast.png and temperature_effect_forecast.png respectively")

def clean():
    if (os.path.exists("./tmpsqlite")):
        os.remove("./tmpsqlite")
    if (os.path.exists("./hietaniemi-gym-data-enriched.csv")):
        os.remove("./hietaniemi-gym-data-enriched.csv")
    if (os.path.exists("./per_day.png")):
        os.remove("./per_day.png")
    if (os.path.exists("./per_hour.png")):
        os.remove("./per_hour.png")
    if (os.path.exists("./precipitation_effect.png")):
        os.remove("./precipitation_effect.png")
    if (os.path.exists("./precipitation_effect_forecast.png")):
        os.remove("./precipitation_effect_forecast.png")
    if (os.path.exists("./total_minutes.png")):
        os.remove("./total_minutes.png")
    if (os.path.exists("./temperature_effect.png")):
        os.remove("./temperature_effect.png")
    if (os.path.exists("./temperature_effect_forecast.png")):
        os.remove("./temperature_effect_forecast.png")




