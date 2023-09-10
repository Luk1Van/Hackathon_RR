import torch
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import json
import warnings
warnings.simplefilter("ignore")


def preprocess_stations(stations_data):
    all_stations = list(stations_data.iloc[0].keys())
    
    station_vectors = []
    for key, value in stations_data.items():
        vector = []
        for station, values in value.items():
            vector.extend([int(v) for v in values])
        station_vectors.append(vector)
    
    return np.array(station_vectors), all_stations


def preprocess_timetable_updated(timetable_data, all_stations):
    route_vectors = []
    free_carriage_vectors = []
    timetable_vectors = []
    
    for train_num, train_data in timetable_data.items():
        for key, value in train_data.items():
            route = [int(r) for r in value['route']]
            for i in range(len(route)-1):
                route[i] = route[i+1]
            route_vectors.append(route)

            free_carriage = [int(fc) for fc in value['free_carriage']]
            free_carriage_vectors.append(free_carriage)

            timetable = [int(time.split('-')[0].split(':')[0])*60 + int(time.split('-')[0].split(':')[1]) for time in value['timetable']]
            timetable_vectors.append(timetable)
    
    return np.array(route_vectors), np.array(free_carriage_vectors), np.array(timetable_vectors)


def pad_sequences(sequences, max_length):
    padded_sequences = []
    
    for seq in sequences:
        if len(seq) < max_length:
            padded_seq = list(seq) + [0] * (max_length - len(seq))
        else:
            padded_seq = list(seq)[:max_length]
        padded_sequences.append(padded_seq)
    
    return np.array(padded_sequences)


model = torch.jit.load("model.pt")
model.eval()

data = pd.read_json("dataset.json")

station_vectors, all_stations = preprocess_stations(data["stations"])
route_vectors, free_carriage_vectors, timetable_vectors = preprocess_timetable_updated(data["full_timetable"], all_stations)
max_length_route = max([len(r) for r in route_vectors])
max_length_free_carriage = max([len(fc) for fc in free_carriage_vectors])
max_length_timetable = max([len(t) for t in timetable_vectors])

route_vectors_padded = pad_sequences(route_vectors, max_length_route)
free_carriage_vectors_padded = pad_sequences(free_carriage_vectors, max_length_free_carriage)
timetable_vectors_padded = pad_sequences(timetable_vectors, max_length_timetable)

num_repeats = route_vectors_padded.shape[0] // station_vectors.shape[0]
expanded_station_vectors = np.tile(station_vectors, (num_repeats, 1))

route_vectors_padded = route_vectors_padded[:expanded_station_vectors.shape[0]]
free_carriage_vectors_padded = free_carriage_vectors_padded[:expanded_station_vectors.shape[0]]
timetable_vectors_padded = timetable_vectors_padded[:expanded_station_vectors.shape[0]]

combined_input = np.hstack((expanded_station_vectors, route_vectors_padded, free_carriage_vectors_padded, timetable_vectors_padded))


X_train, X_test, y_train, y_test = train_test_split(combined_input, expanded_station_vectors, test_size=0.2, random_state=42)



with torch.no_grad():
    inputs = torch.tensor(X_test, dtype=torch.float32)
    predicted_vectors = model(inputs).numpy()
    predictions = np.concatenate(predicted_vectors).ravel().astype(int).tolist()

    #print(predictions)


print("Введите номер ситуации:")
situation = int(input())
l, r = 0, 0
schedule = {}
timetable = data["full_timetable"].iloc[situation]
for train in timetable.keys():
	r += len(timetable[train]["route"]) - 1
	if r > len(predictions):
		break
	schedule[train] = {}
	schedule[train]["route"] = timetable[train]["route"]
	schedule[train]["timetable"] = timetable[train]["timetable"]
	schedule[train]["vagons"] = [max(x, 0) for x in predictions[l:r]]
	l = r

	print("\nНомер локомотива:", train)
	print("Маршрут:", *schedule[train]["route"])
	print("Расписание:", *schedule[train]["timetable"])
	print("Количество вагонов для каждой станции:", *schedule[train]["vagons"])

with open("output.json", "w", encoding='utf8') as outfile:
    json.dump(schedule, outfile, ensure_ascii=False)