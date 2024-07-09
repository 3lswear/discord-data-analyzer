from js import document, FileReader
from pyodide.ffi import create_proxy
import glob
import json
import asyncio
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.axes as mpl_axes
matplotlib.use("module://matplotlib_pyodide.wasm_backend")
# matplotlib.use("module://matplotlib_pyodide.html5_canvas_backend")

async def do_the_thing(event) -> None:

    VERSION = "0.1"

    print("Crunching the data...")

    age_times = []
    age_keys = ["prob_13_17", "prob_18_24", "prob_25_34", "prob_35_over"]
    age_lists = {k:[] for k in age_keys}
    gender_times = []
    gender_keys = ["prob_male", "prob_female", "prob_non_binary_gender_expansive"]
    gender_lists = {k:[] for k in gender_keys}


    activity_files = glob.glob("/data/events-*-*-of-*.json")
    user_id = None
    for activity_file in activity_files:
        print(f"Processing {activity_file}")
        with open(activity_file, 'r') as f:
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

    print(f'age points = {len(age_times)}')
    print(f'gender points = {len(gender_times)}')

    fig, axs = plt.subplots(2)
    fig.set_size_inches(15, 15);

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
        # plt.tight_layout()
        # plt.show()

    if (len(gender_times)):
        gender_ax.set_title("Predicted gender")
        for key in gender_keys:
            gender_ax.plot(*zip(*sorted(zip(gender_times, gender_lists[key]))), marker='o')
        gender_ax.legend(["male", "female", "non-binary"])
        # plt.tight_layout()
        fig.text(0, 0, f"created with discord data analyzer v{VERSION} https://dda.metacringe.com/", verticalalignment='bottom')
        plt.show()

    if len(age_times) == 0 and len(gender_times) == 0:
        print("No data for you :(")

def main():

    button_event = create_proxy(do_the_thing)
    button = document.getElementById('runbutton')
    button.addEventListener('click', button_event, False)

    print("👋 I am loaded now, push the button!")

main()
