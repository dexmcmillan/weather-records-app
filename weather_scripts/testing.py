import pandas as pd

data = pd.read_csv("./data/raw_data2.csv")
data = data.drop(columns=list(data.filter(regex='Unnamed')))

print(data)

climateStationMetadata = pd.read_csv("./data/stations_cma.csv").set_index("Climate ID")

# An empty list for storing new data.
li = []

# Get a list of unique station IDs to iterate through.
listOfStationIds = (climateStationMetadata
                    .loc[climateStationMetadata["Last Year"] == 2022, "Station ID"]
                    .unique()
                    .astype(int)
                    )

for stationId in listOfStationIds[0:10]:
    
    df = pd.read_csv(f'https://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID={str(stationId)}&Year=2022&Month=11&Day=21&timeframe=2')
    df = df.loc[(df["Month"] == 11) & (df["Day"] == 21),:]
    df = df[[ "Climate ID", "Year", "Month", "Day", "Date/Time", "Max Temp (°C)", "Min Temp (°C)"]]
    li.append(df)
    
new_data = pd.concat(li)
new_data.index = new_data.index.astype(str)
new_data = new_data.join(climateStationMetadata)
new_data = new_data.pivot_table(columns="Year", values="Max Temp (°C)", index=["CMANAME", "Month", "Day"], aggfunc='max').reset_index().melt(id_vars=["CMANAME", "Month", "Day"]).dropna()

print(new_data)

print(new_data.columns, data.columns)

data = pd.concat([data, new_data], axis=0).drop_duplicates()

print(data.reset_index()[data.reset_index()["CMANAME"] == "Duncan"])

save_file_name = f"data/series/test-max.json"

dataforCitiesWithEnoughData = data.pivot_table(columns="Year", values="value", index=["CMANAME", "Month", "Day"], aggfunc='max')

print(dataforCitiesWithEnoughData)

more_testing = pd.DataFrame({"Year": dataforCitiesWithEnoughData.idxmax(axis=1), "Temp": dataforCitiesWithEnoughData.max(axis=1)}).reset_index()
more_testing["Date"] = pd.to_datetime(more_testing["Year"].astype(str) + "-" + more_testing["Month"].astype(str) + "-" + more_testing["Day"].astype(str))
more_testing = more_testing.drop(columns=["Month", "Day", "Year"])
more_testing["days_since_record"] = (pd.datetime.today() - more_testing["Date"]).dt.days - 1

daysSinceMaximumRecord = []

for city in more_testing["CMANAME"].unique():
    
    d = more_testing[more_testing["CMANAME"] == city]

    d = d[d["days_since_record"] == d["days_since_record"].min()]
    daysSinceMaximumRecord.append(d)
    
daysSinceMaximumRecord = pd.concat(daysSinceMaximumRecord).sort_values("days_since_record")
daysSinceMaximumRecord["Date"] = daysSinceMaximumRecord["Date"].dt.strftime("%Y-%m-%d")

daysSinceMaximumRecord.to_json(save_file_name, orient='records')