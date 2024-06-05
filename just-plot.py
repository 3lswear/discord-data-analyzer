import matplotlib.pyplot as plt
import json
from pprint import pprint
from datetime import datetime

# f = open('events_small_fixed.json', 'r')
f = open('events.json', 'r')
the_string = f.read()

age_times = []
age_keys = ["prob_13_17", "prob_18_24", "prob_25_34", "prob_35_over"]
age_lists = {k:[] for k in age_keys}

gender_times = []
gender_keys = ["prob_male", "prob_female", "prob_non_binary_gender_expansive"]
gender_lists = {k:[] for k in gender_keys}

for line in iter(the_string.splitlines()):
# for line in f:
    if ',"predicted_' in line:
        j = json.loads(line)
        # print(j)
        # pprint(j)
        if 'predicted_age' in j:
            age_times.append(datetime.fromisoformat(j.get('day_pt').replace(' UTC', '')))
            for key in age_keys:
                age_lists[key].append(j.get(key))
        if 'predicted_gender' in j:
            gender_times.append(datetime.fromisoformat(j.get('day_pt').replace(' UTC', '')))
            for key in gender_keys:
                gender_lists[key].append(j.get(key))


# for key in gender_keys:
#     a = zip(gender_times, gender_lists[key])
#     # print(a)
#     print(*sorted(zip(gender_times, gender_lists[key])))
#     # print(*zip(*sorted(a)))
#     print("---------")

if (len(age_times)):
    plt.title("Discord predicted age")
    for key in age_keys:
        plt.plot(*zip(*sorted(zip(age_times, age_lists[key]))), marker='o')
    plt.legend(["13-17", "18-24", "25-34", "35+"])
    plt.show()

if (len(gender_times)):
    plt.title("Discord predicted gender")
    for key in gender_keys:
        plt.plot(*zip(*sorted(zip(gender_times, gender_lists[key]))), marker='o')
    plt.legend(["male", "female", "non-binary"])
    plt.show()

if len(age_times) == 0 and len(gender_times) == 0:
    print("No data for you :(")






#
# dictionary = json.load(open('file.json', 'r'))
# xAxis = [key for key, value in dictionary.items()]
# yAxis = [value for key, value in dictionary.items()]
# plt.grid(True)
#
# ## LINE GRAPH ##
# plt.plot(xAxis,yAxis, color='maroon', marker='o')
# plt.xlabel('variable')
# plt.ylabel('value')
#
# ## BAR GRAPH ##
# fig = plt.figure()
# plt.bar(xAxis,yAxis, color='maroon')
# plt.xlabel('variable')
# plt.ylabel('value')
#
# plt.show()
