import csv
from make_stimuli import stimuli

with open('kevin1_tone_discrimination_results.csv', newline='') as csvfile:
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

frequencies = stimuli['frequency'][0]

scores = {float(frequency): [] for frequency in frequencies[1:]}
for n in range(len(rows)-1):
    frequency = columns['correct_response'][n]
    scores[float(frequency)].append(int(columns['score'][n]))

accuracy = {}
for frequency in scores:
    mean = sum(scores[frequency]) / len(scores[frequency])
    accuracy[frequency] = mean

print(accuracy)