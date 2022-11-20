from weather import WeatherData
import pandas as pd
import datetime as dt
import logging
from datetime import timedelta


climateStationList = pd.read_csv("./data/stations_cma.csv")
yesterday = (dt.datetime.today() - timedelta(days=1)).date()

weather = WeatherData()

def getTestData(upToDate = True):
    
    
    data = pd.read_csv("./data/data-historical-both.csv")
    
    if not upToDate:

        yesterday = dt.datetime.today() - dt.timedelta(days=2)

        data = data.loc[data["Date/Time"] == yesterday.date, :]

        return data
    
    else:
        return data

# Check our exported dataset columns to ensure they're properly ordered, with the right index.
def test_datasetColumns():
    columns = ", ".join(getTestData().columns.to_list())
    logging.info(columns)
    assert columns == "Climate ID, Date/Time, Year, Month, Day, Max Temp (°C), Min Temp (°C)"
    
    
def test_checkForNoSmallCities():
    
    # Load in the max and min data exports from running our script.
    maxTempData = pd.read_json('./data/Max Temp (°C).json')
    minTempData = pd.read_json('./data/Min Temp (°C).json')
    
    print(maxTempData)
    
    # Get the number of stations in each CMA or CA.
    counts = (climateStationList
                    .pivot_table(index="CMANAME", values="CMAUID", aggfunc='count')
                    .sort_values("CMAUID", ascending=True)
                    )
    
    # Make a list of those CMAs or CAs that have fewer than or equal to 5 stations.
    excludeList = (counts
                .loc[counts["CMAUID"] <= 5, :]
                .index
                .to_list()
                )
    
    # Check that none of those CMAs are in the final list.
    maxTempCities = maxTempData[maxTempData["CMANAME"].isin(excludeList)]
    minTempCities = minTempData[minTempData["CMANAME"].isin(excludeList)]
    
    assert len(maxTempCities) == 0 and len(minTempCities) == 0
    
    
def test_getCityData():
    cityData = weather.getDataForCity(cma="Victoria", metric="Max Temp (°C)")
    
    logging.info(cityData)

    assert len(cityData) > 0
    
def test_getCityMax():
    cityMaxData = weather.maxForCity(cma="Victoria", metric="Max Temp (°C)")
    
    logging.info(cityMaxData)

    assert len(cityMaxData) > 0
    
    
def test_noMissingDates():
    
    data = getTestData()
    
    logging.info(yesterday)
    
    dates = ", ".join(data["Date/Time"].astype(str).unique()[-11:])
    logging.info(dates)
    
    dateRange = ", ".join(pd.date_range(yesterday - timedelta(10), yesterday).map(lambda x: str(x.date())))
    logging.info(dateRange)
    
    assert dates == dateRange