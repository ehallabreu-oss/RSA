import csv
from make_stimuli import stimuli

with open('kevin_full_discrimination_results.csv', newline='') as csvfile:
    kevin = csv.reader(csvfile, delimiter=',')
    rows = []
    for row in kevin:
        rows.append(row)

column_names = []
for element in rows[0]:
    column_names.append(element)

columns = {}
for name in column_names:
    columns[name] = []

for row in rows[1:]:
    for n in range(len(column_names)):
        columns[column_names[n]].append(row[n])

scores = {}
for stimulus_type in stimuli:
    scores[stimulus_type] = {}
    values = stimuli[stimulus_type][0]
    for value in values[1:]:
        scores[stimulus_type][float(value)] = []

for n in range(len(rows)-1):
    stimulus_type = columns['block'][n]
    value = columns['correct_response'][n]
    scores[stimulus_type][float(value)].append(int(columns['score'][n]))

accuracy = {}

for stimulus_key in scores:
    accuracy[stimulus_key] = {}
    for value in scores[stimulus_key]:
        mean = sum(scores[stimulus_key][value]) / len(scores[stimulus_key][value])
        accuracy[stimulus_key][value] = mean

print(accuracy)   