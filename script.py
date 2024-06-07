from js import document, FileReader
from pyodide.ffi import create_proxy
import glob
import json
import asyncio
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("module://matplotlib_pyodide.wasm_backend")
# matplotlib.use("module://matplotlib_pyodide.html5_canvas_backend")

async def do_the_thing(event):

    VERSION = "0.1"

    print("Crunching the data...")
    count = 0;

    age_times = []
    age_keys = ["prob_13_17", "prob_18_24", "prob_25_34", "prob_35_over"]
    age_lists = {k:[] for k in age_keys}
    gender_times = []
    gender_keys = ["prob_male", "prob_female", "prob_non_binary_gender_expansive"]
    gender_lists = {k:[] for k in gender_keys}


    activity_files = glob.glob("/data/events-*-*-of-*.json")
    for activity_file in activity_files:
        print(f"Processing {activity_file}")
        with open(activity_file, 'r') as f:
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

    print(f'age points = {len(age_times)}')
    print(f'gender points = {len(gender_times)}')

    fig, axs = plt.subplots(2)
    # plt.figure(figsize=(6,6), dpi=72)

    if (len(age_times)):
        fig.suptitle("two things")
        # plt.title("Discord predicted age")
        for key in age_keys:
            print(f'plotting {key}')
            axs[0].plot(*zip(*sorted(zip(age_times, age_lists[key]))), marker='o')
        axs[0].legend(["13-17", "18-24", "25-34", "35+"])
        # plt.tight_layout()
        # plt.show()

    if (len(gender_times)):
        # plt.figure(figsize=(6,6), dpi=72)
        # axs[1].title("Discord predicted gender")
        for key in gender_keys:
            axs[1].plot(*zip(*sorted(zip(gender_times, gender_lists[key]))), marker='o')
        axs[1].legend(["male", "female", "non-binary"])
        # plt.tight_layout()
        plt.show()

    if len(age_times) == 0 and len(gender_times) == 0:
        print("No data for you :( (there was no relevant data)")

def main():

    button_event = create_proxy(do_the_thing)
    button = document.getElementById('runbutton')
    button.addEventListener('click', button_event, False)

    print("👋 I am loaded now, push the button!")

main()
