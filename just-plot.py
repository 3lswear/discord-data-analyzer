import matplotlib
import matplotlib.axes as mpl_axes
import matplotlib.pyplot as plt
import json
from pprint import pprint
from datetime import datetime

# f = open('events_small_fixed.json', 'r')
f = open('events.json', 'r')

VERSION = "0.1"

age_times = []
age_keys = ["prob_13_17", "prob_18_24", "prob_25_34", "prob_35_over"]
age_lists = {k:[] for k in age_keys}

gender_times = []
gender_keys = ["prob_male", "prob_female", "prob_non_binary_gender_expansive"]
gender_lists = {k:[] for k in gender_keys}

# for line in iter(the_string.splitlines()):
user_id = None
for line in f:
    if ',"predicted_' in line:
        j = json.loads(line)
        # print(j)
        # pprint(j)
        if (not user_id) and ('user_id' in j):
            user_id = j.get('user_id')
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
fig, axs = plt.subplots(2)
fig.set_size_inches(18, 15);

age_ax: mpl_axes.Axes = axs[0]
gender_ax: mpl_axes.Axes = axs[1]
age_ax.set_ylim(0.0, 1.0)
gender_ax.set_ylim(0.0, 1.0)

age_ax.set_ylabel("Probability")
age_ax.set_xlabel("Time")
gender_ax.set_ylabel("Probability")
gender_ax.set_xlabel("Time")

age_ax.grid();
gender_ax.grid();

if (len(age_times)):
    fig.suptitle(f"Discord data for user_id {user_id}")
    # plt.title("Discord predicted age")
    age_ax.set_title("Predicted age")
    for key in age_keys:
        print(f'plotting {key}')
        age_ax.plot(*zip(*sorted(zip(age_times, age_lists[key]))), marker='o')
    age_ax.legend(["13-17", "18-24", "25-34", "35+"])
    # plt.grid()

    # plt.tight_layout()
    # plt.show()

if (len(gender_times)):
    gender_ax.set_title("Predicted gender")
    for key in gender_keys:
        gender_ax.plot(*zip(*sorted(zip(gender_times, gender_lists[key]))), marker='o')
    gender_ax.legend(["male", "female", "non-binary"])
    # plt.tight_layout()
fig.text(0, 0, f"created with discord data analyzer v{VERSION} https://metacringe.com/dda", verticalalignment='bottom')

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
