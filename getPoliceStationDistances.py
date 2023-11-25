from tqdm import tqdm
import pandas as pd
import json

crimes = pd.read_csv('data\cartodb-query.csv')
data = crimes[["dispatch_date", "dispatch_time","location_block", "text_general_code", "point_x", "point_y"]]

police_stations = pd.read_csv('data\Police Station w coordinates.csv').reindex(columns=["OBJECTID", "DISTRICT_NUMBER",
                                                                                        "LOCATION", "TELEPHONE_NUMBER",
                                                                                       "RULEID", "Longitude", "Latitude"])
# Calculating the Manhattan distance
def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

distances =[]
# Calculating distance to nearest police station for each crime
for index, row in tqdm(data.iterrows(), total=data.shape[0], desc="Processing", ascii=False):
    crime_x = row['point_x']
    crime_y = row['point_y']
    min_distance = float('inf')
    for _, station in police_stations.iterrows():
        station_x = station['Longitude']
        station_y = station['Latitude']
        distance = manhattan_distance(crime_x, crime_y, station_x, station_y)
        min_distance = min(min_distance, distance)
    distances.append(min_distance)
with open('data\min_distances.json', 'w') as f:
    json.dump({"min_distances":distances}, f)
