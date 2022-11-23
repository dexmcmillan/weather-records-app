# This is the primary module that loads and processes the weather data.
# Some one-time number crunching is done in other files, mostly found in the 'methodology' folder.

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import datetime as dt
from datetime import timedelta

# For logging. TQDM is a package that shows a progress bar in the console.
import logging
from tqdm import tqdm

logging.getLogger().setLevel(logging.INFO)



class WeatherData:
    
    # The big dataset, contains one entry for each weather station.
    global data
    
    # A datetime representation of yesterday, which is used throughout this module.
    global yesterday
    
    # A list of stations from ECC.
    global climateStationMetadata
    
    # The last date of collected data, which is used in this module.
    global lastDateCollected
    
    # Stores the metric (either max temp or min temp) that is input into the class constructor.
    global metric
    
    
    def __init__(self, metric="max"):
        
        # Set the input parameter as a class property.
        self.metric = metric
        
        logging.info(f"Loading in previous weather data...")
        
        # Load in data that's already been collected.
        if metric == "max": self.data = pd.read_csv("data/raw_data-max.csv", low_memory=False)
        elif metric == "min": self.data = pd.read_csv("data/raw_data-min.csv", low_memory=False)
        
        # Here, we drop any extraneous columns that may have been created by accident by setting/resetting columns on previous saves.
        self.data = (self.data
                     .drop(columns=list(self.data.filter(regex='Unnamed')))
                     .drop(columns=list(self.data.filter(regex='level')))
                     .drop(columns=list(self.data.filter(regex='index')))
                     )
        
        # Get the list of active stations and store it as a class property.
        self.climateStationMetadata = pd.read_csv("data/stations_cma.csv", encoding="utf-8", index_col="Climate ID")
        
        # We set the Climate ID type to string, because otherwise we may get joining errors if we try to join to the same data as integers.
        self.climateStationMetadata.index = self.climateStationMetadata.index.astype(str)
        
        # Get today's data and yesterday's date and store them as a class property.
        self.yesterday = (dt.datetime.today().date() - timedelta(days=1))
        
        # Create a date column from Year, Month, and Day columns, then find the most recent date to determine if we need to fetch more data from ECC.
        self.data["date"] = pd.to_datetime(self.data["Year"].astype(str) + "-" + self.data["Month"].astype(str) + "-" + self.data["Day"].astype(str))
        self.lastDateCollected = self.data["date"].max().date()
        
        # If it's out of date, run the fetch method.
        if self.lastDateCollected < self.yesterday:
            logging.info("Out of date!")
            self.getNewDataFromECC()
            
        # Otherwise, log and move on.
        else: logging.info(f"Data up to date.")
        
        return None
       
       
       
        
        
        
    # This function handles the getting of new data from the ECC API.
    def getNewDataFromECC(self):
        
        # Get a list of dates that's missing from the dataset.
        dates = pd.date_range(self.lastDateCollected + timedelta(days=1), self.yesterday).map(lambda x: x.date)

        # An empty list for storing new data.
        li = []

        for date in dates:
            logging.info(f"Getting data for stations for {date}.")
            
            # Get a list of unique station IDs to iterate through.
            listOfStationIds = (self.climateStationMetadata
                              .loc[self.climateStationMetadata["Last Year"] == 2022, "Station ID"]
                              .unique()
                              .astype(int)
                              )
            
            # Loop through every station and get data using ECC's historical weather data API.
            for stationId in tqdm(listOfStationIds):
                
                df = pd.read_csv(f'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={str(stationId)}&Year={date.year}&Month={date.month}&Day={date.day}&timeframe=2')
                
                # This url actually returns a full month's worth of data, so we filter for the day we want only.
                df = df.loc[(df["Month"] == date.month) & (df["Day"] == date.day),:]
                
                # Cut out any columns we don't need.
                df = df[["Climate ID", "Year", "Month", "Day", "Date/Time", "Max Temp (°C)", "Min Temp (°C)"]]
                
                # Add it to a list for concatenation once the loop is complete.
                li.append(df)
        
        # We'll join station data onto this, and station data ID is the Climate ID columns.
        new_data = pd.concat(li).set_index("Climate ID")
        
        # Make sure the index (Climate ID) is a string.
        new_data.index = new_data.index.astype(str)
        
        # Next, we join station/CMA location data onto our new data.
        # For more info on how each station was located in city boundaries, see methodology/spatial_join.ipynb.
        
        # The value we pivot on will depend on our input metric, so we set that depending on that parameter.
        if self.metric == "max": value = "Max Temp (°C)"
        elif self.metric == "min": value = "Min Temp (°C)"
        
        # Now we join station data, then pivot to get max values for each day, then melt back into a format we want to save in (and that we can use to join onto our historical data)
        updatedDataForThisMetric = (new_data
                                    .join(self.climateStationMetadata, rsuffix="_")
                                    .pivot_table(columns="Year", values=value, index=["CMANAME", "Month", "Day"], aggfunc=self.metric)
                                    .reset_index()
                                    .melt(id_vars=["CMANAME", "Month", "Day"])
                                    .dropna()
                                    )
    
        # Now we concat the new data onto the old stuff, and drop any duplicates we might have.
        updatedDataForThisMetric = pd.concat([self.data, updatedDataForThisMetric], axis=0).drop_duplicates()
    
        # Now we save our data.
        # We also drop any extra columns that might have been created by index manipulation (setting/resetting.)
        try:
            logging.info(f"Saving new data for {self.metric} values...")
            (updatedDataForThisMetric
            .drop(columns=list(updatedDataForThisMetric.filter(regex='level')))
            .drop(columns=list(updatedDataForThisMetric.filter(regex='index')))
            .drop(columns=list(updatedDataForThisMetric.filter(regex='Unnamed')))
            .drop(columns=["date"])
            .drop_duplicates(subset=["CMANAME", "Month", "Day", "Year"])
            .to_csv(f"data/raw_data-{self.metric}.csv")
            )
            
        except: logging.error("Error saving new data.")
            
        self.data = pd.read_csv(f"data/raw_data-{self.metric}.csv", low_memory=False)
        
        return self.data
    
    
    
    
    
    
    
    
    # Once we have our data together, we'll need to process it to find how long ago records were broken.
    # The raw data we have is simply max/min temperatures for each city.
    def findDaysSinceRecordForAllCities(self):
        
        logging.info(f"Processing raw data to find {self.metric} values...")
        
        # We'll save our final output here.
        save_file_name = f"data/series/{self.yesterday}-{self.metric}.json"
        
        # Some cities simply don't have enough data for us to be including them.
        # Either there are not enough stations in the city boundaries, or the stations in the city have not collected data very far back.
        # Here, we filter for only the cities we want to include.
        cmasWithEnoughData = ['Saint John',
            'Saguenay',
            'Saint-Hyacinthe',
            'Saint-Georges',
            'Abbotsford - Mission',
            'Rivière-du-Loup',
            'Regina',
            'Québec',
            'Quesnel',
            'Prince Rupert',
            'Prince George',
            'Prince Albert',
            'Powell River',
            'Port Alberni',
            'Peterborough',
            'Petawawa',
            'Penticton',
            'Rouyn-Noranda',
            'Salmon Arm',
            'Shawinigan',
            'Saskatoon',
            'Woodstock',
            'Wood Buffalo',
            'Winnipeg',
            'Winkler',
            'Windsor',
            'Williams Lake',
            'Whitehorse',
            'Weyburn',
            'Victoriaville',
            'Victoria',
            'Vernon',
            'Vancouver',
            "Val-d'Or",
            'Truro',
            'Trois-Rivières',
            'Trail',
            'Toronto',
            'Sault Ste. Marie',
            'Sept-Îles',
            'Parksville',
            'Sherbrooke',
            'Sorel-Tracy',
            'Squamish',
            'Sarnia',
            'St. Catharines - Niagara',
            'Summerside',
            'Swift Current',
            'Terrace',
            'Thetford Mines',
            'Thunder Bay',
            'Timmins',
            "St. John's",
            'Owen Sound',
            'North Battleford',
            "Ottawa - Gatineau (Ontario part / partie de l'Ontario)",
            'Essa',
            'Edmundston',
            'Edmonton',
            'Duncan',
            'Drummondville',
            'Dawson Creek',
            'Cranbrook',
            'Courtenay',
            'Cornwall',
            'Corner Brook',
            'Collingwood',
            'Cobourg',
            'Chilliwack',
            'Chatham-Kent',
            'Charlottetown',
            'Centre Wellington',
            'Cape Breton',
            'Campbell River',
            'Calgary',
            'Brooks',
            'Brockville',
            'Brantford',
            'Brandon',
            'Belleville - Quinte West',
            'Bathurst',
            'Barrie',
            'Baie-Comeau',
            'Amos',
            'Alma',
            'Estevan',
            'Fort St. John',
            'Fredericton',
            'Gander',
            'Oshawa',
            'Orillia',
            'Okotoks',
            'North Bay',
            'Yellowknife',
            'Norfolk',
            'Nelson',
            'Nanaimo',
            'Moose Jaw',
            'Montréal',
            'Moncton',
            'Miramichi',
            'Medicine Hat',
            'London',
            'Ottawa - Gatineau (partie du Québec / Quebec part)',
            "Lloydminster (Alberta part / partie de l'Alberta)",
            'Ladysmith',
            'Lachute',
            'Kitchener - Cambridge - Waterloo',
            'Kingston',
            'Kentville',
            'Kenora',
            'Kelowna',
            'Kamloops',
            'Hamilton',
            'Halifax',
            'Guelph',
            'Greater Sudbury / Grand Sudbury',
            'Grande Prairie',
            'Granby',
            'Lethbridge',
            'Yorkton'
        ]
        
        dataforCitiesWithEnoughData = (self.data
                                       .loc[self.data["CMANAME"].isin(cmasWithEnoughData), :]
                                       .pivot_table(columns="Year", values="value", index=["CMANAME", "Month", "Day"], aggfunc='max')
                                       )
        
        # Here, we create a new dataframe depending on what metric we're after.
        # The new dataframe has two columns - one to return the year of date with the least number of days since a record, the other with the temp on that date.
        if self.metric == "max":
            cityMaxValues = pd.DataFrame({"Year": dataforCitiesWithEnoughData.idxmax(axis=1), "Temp": dataforCitiesWithEnoughData.max(axis=1)}).reset_index()
        elif self.metric == "min":
            cityMaxValues = pd.DataFrame({"Year": dataforCitiesWithEnoughData.idxmin(axis=1), "Temp": dataforCitiesWithEnoughData.min(axis=1)}).reset_index()
        
        # Create a date column for our data, then scrap the Month, Day, Year columns.
        cityMaxValues["date"] = pd.to_datetime(cityMaxValues["Year"].astype(str) + "-" + cityMaxValues["Month"].astype(str) + "-" + cityMaxValues["Day"].astype(str))
        cityMaxValues = cityMaxValues.drop(columns=["Month", "Day", "Year"])
        
        # Create a new column to calculate the number of days since a record was broken in each city.
        cityMaxValues["days_since_record"] = (pd.datetime.today() - cityMaxValues["date"]).dt.days - 1

        # An empty list that will be added to and concatenated into a dataframe.
        daysSinceMaximumRecord = []

        # Iterate through each city and get the smallest value in the days_since_record column.
        # The minimum of this column will by default always be the only value we need from this data.
        for city in cityMaxValues["CMANAME"].unique():
            
            # Filter for city data only.
            d = cityMaxValues[cityMaxValues["CMANAME"] == city]

            # Get the record with the lowest value.
            d = d[d["days_since_record"] == d["days_since_record"].min()]
            
            # Append to the list that will ultimately become a dataframe after the loop finishes.
            daysSinceMaximumRecord.append(d)
            
        # Create the dataframe via pd.concat, then sort in ascending order by days_since_record.
        daysSinceMaximumRecord = pd.concat(daysSinceMaximumRecord).sort_values("days_since_record")
        
        # Convert the date column into a string for nicer reading by the front end.
        daysSinceMaximumRecord["date"] = daysSinceMaximumRecord["date"].dt.strftime("%Y-%m-%d")
        
        # Get a dataframe with province info for each city, so we can join it on before export.
        provinceInfo = self.climateStationMetadata.drop_duplicates(subset="CMANAME").set_index("CMANAME")[["PRUID"]]
        
        daysSinceMaximumRecord["CMANAME"] = (daysSinceMaximumRecord["CMANAME"]
                                             .str.replace("Greater Sudbury / Grand Sudbury", "Sudbury", regex=False)
                                             .str.replace(" \(.*\)", "", regex=True)
                                             .str.replace("Î", "I", regex=True)
                                             .str.replace("é|è", "e", regex=True)
                                             )
        
        # Join province info onto our data.
        daysSinceMaximumRecord = (daysSinceMaximumRecord
                                  .set_index("CMANAME")
                                  .join(provinceInfo, how="left")
                                  .reset_index()
                                  .sort_values("days_since_record")
                                  )
        
        # Export to json. This file will be the one used in the front end display.
        daysSinceMaximumRecord.to_json(save_file_name, orient='records')
        
        return daysSinceMaximumRecord