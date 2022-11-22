import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import datetime as dt
from datetime import timedelta

# For logging. TQDM is a package that shows a progress bar in the console.
import logging
from tqdm import tqdm

logging.getLogger().setLevel(logging.INFO)
            
updateLogger = logging.getLogger()

class WeatherData:
    
    
    global data
    global yesterday
    global climateStationMetadata
    global lastDateCollected
    
    
    def __init__(self):
        
        logging.info(f"Loading in previous historical data...")
        
        # Load in data that's already been collected.
        self.data = pd.read_csv("data/data-historical-both.csv", low_memory=False)
        
        # Get the list of active stations and store it as a class property.
        self.climateStationMetadata = pd.read_csv("data/stations_cma.csv", encoding="utf-8", index_col="Climate ID")
        
        self.lastDateCollected = pd.to_datetime(self.data["Date/Time"]).max(skipna=True)
        
        # Get today's data and yesterday's date and store them as a class property.
        self.yesterday = (dt.datetime.today() - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # If it's out of date, run the fetch method.
        if self.lastDateCollected < self.yesterday:
            
            self.getNewDataFromECC()
            
        # Otherwise, log and move on.
        else: logging.info(f"Data up to date.")
            
        # Run a function to join CMA data onto each climate station in the dataset.
        self.joinCityData()
        
        return None
       
       
       
        
        
        
    # This function handles the getting of new data from the ECC API.
    def getNewDataFromECC(self):
        
        dates = pd.date_range(self.lastDateCollected + timedelta(days=1), self.yesterday).map(lambda x: x.date)
    
        li = []

        for date in dates:
            updateLogger.info(f"Getting data for stations for {date}.")
            
            # Get a list of unique station IDs to iterate through.
            listOfStationIds = (self.climateStationMetadata
                              .loc[self.climateStationMetadata["Last Year"] == 2022, "Station ID"]
                              .unique()
                              .astype(int)
                              )
            
            for stationId in tqdm(listOfStationIds):
                
                df = pd.read_csv(f'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={str(stationId)}&Year={date.year}&Month={date.month}&Day={date.day}&timeframe=2')
                df = df.loc[(df["Month"] == date.month) & (df["Day"] == date.day),:]
                df = df[[ "Climate ID", "Year", "Month", "Day", "Date/Time", "Max Temp (°C)", "Min Temp (°C)"]]
                li.append(df)
                
        additions = pd.concat(li)

        self.data = (pd.concat([self.data, additions])
                     .drop_duplicates(subset=["Climate ID", "Year", "Month", "Day"])
                     .drop(columns=list(self.data.filter(regex='Unnamed').columns))
                     )
        
        
        try:
            logging.info("Saving new data...")
            self.data.to_csv("data/data-historical-both.csv")
            
        except: logging.error("Error saving new data.")
        
        return self.data
        
        
        
        
    # Joins CMA name metadata onto our main dataset.
    def joinCityData(self):
        
        logging.info(f"Joining CMA data onto weather station data...")

        # Join CMA info onto the dataset in this class instance.
        self.data = (self.data
                     .set_index("Climate ID")
                     .join(self.climateStationMetadata[["CMANAME", "PRUID"]])
                     )
        
        return self.data
        
    
    
    
        
    def values(self, input_data, date, metric):
        
        if "max" in metric.lower():
            values = input_data.max(axis=0)
            dates = input_data.idxmax(axis=0)
            
        elif "min" in metric.lower():
            values = input_data.min(axis=0)
            dates = input_data.idxmin(axis=0)
            
        values.columns = ["Temp"]
        dates.columns = ["Year"]
        
        max = (pd.concat([values, dates], axis=1)
               .reset_index()
               .rename(columns={0: "Temp", 1: "Year"})
               )
        
        max["date"] = pd.to_datetime(max[["Year", "Month", "Day"]])
        max["days_since_record"] = (pd.to_datetime(date) - max["date"]).dt.days
        
        max_values = (max
                      .loc[:, ["CMANAME", "PRUID", "date", "days_since_record", "Temp"]]
                      .sort_values("days_since_record")
                      )
    
        return max_values
    
    
    
    
    
    
    
    
    
    def maxForCity(self, cma, metric, date=None):
        
        if date == None:
            date = self.yesterday.date()
            
        data = self.getDataForCity(cma=cma, metric=metric)
        
        values = self.values(input_data=data, date=date, metric=metric).drop_duplicates("CMANAME")
        
        values.index = range(0, len(values))
        
        return values
    
    
    
    
    
    
    
    def getDataForCity(self, cma, metric):
        
        if "max" in metric.lower():
            agg = "max"
            
        elif "min" in metric.lower():
            agg = "min"
        
        data = (self.data[self.data["CMANAME"] == cma]
                        .pivot_table(columns=["Month", "Day", "CMANAME", "PRUID"], index="Year", values=metric, aggfunc=agg)
                        .dropna(how="all", axis=1)
                        )
        
        return data
    
    
    
    
    
    
    
    
    def rankAllCities(self, metric="Max Temp (°C)", date=None):
        
        save_file_name = f"data/{self.yesterday.date()}-{metric}.json"
        
        if date == None:
            date = self.yesterday
            
        lis_max = []
        
        # Get only those CMAs that have more than 5 stations associated with them.
        countOfStationsPerCity = (self.climateStationMetadata
                    .pivot_table(index="CMANAME", values="CMAUID", aggfunc='count')
                    .sort_values("CMAUID", ascending=True)
                    )
        
        excludeList = (countOfStationsPerCity
                    .loc[countOfStationsPerCity["CMAUID"] <= 5, :]
                    .index
                    .to_list()
                    )
        
        cmaNamesList = self.climateStationMetadata["CMANAME"].dropna().astype(str).unique()
        
        cmaNamesList = [v for v in cmaNamesList if v not in excludeList]
        
        logging.info(f"Ranking {len(cmaNamesList)} cities by days since breaking {metric} record.")

        for cma_id in tqdm(cmaNamesList):
            max = self.maxForCity(cma=cma_id, metric=metric, date=date)
            lis_max.append(max)
            
        df = pd.concat(lis_max).sort_values("days_since_record", ascending=True)
        
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        
        df["Rank"] = df["days_since_record"].rank(method="min").astype(int)
        
        start_years = (self.climateStationMetadata
                    .loc[:, ["CMANAME", "First Year"]]
                    .sort_values(["CMANAME", "First Year"])
                    .drop_duplicates("CMANAME")
                    .set_index("CMANAME")
                    )
        
        records = (df
            .set_index("CMANAME")
            .join(start_years)
            .reset_index()
            )
        
        records.to_json(save_file_name, orient='records')
        
        return records