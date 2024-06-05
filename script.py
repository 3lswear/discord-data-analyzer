import matplotlib.pyplot as plt
# import pandas as pd
import asyncio
from js import document, FileReader
import json
from datetime import datetime
from pyodide.ffi import create_proxy
from io import StringIO

selected_file = None

async def process_file(event):
    global selected_file

    fileList = event.target.files
    selected_file = fileList.item(0)

    print("file inputted!")

async def do_the_thing(event, file):

    print("Crunching the data...")
    the_string: str = await file.text()
    print("loaded all the shit into memory")
    count = 0;
    fake_file = StringIO(the_string)
    print("constructed a fake file")
    # for line in fake_file:
    #     do_something_with(line)

    output = "all's good"
    age_times = []
    age_keys = ["prob_13_17", "prob_18_24", "prob_25_34", "prob_35_over"]
    age_lists = {k:[] for k in age_keys}

    gender_times = []
    gender_keys = ["prob_male", "prob_female", "prob_non_binary_gender_expansive"]
    gender_lists = {k:[] for k in gender_keys}

    print('done setting up')
    # for line in fake_file:
    #     print(line)
    #     count += 1

    # print("count is ", count)

    for line in fake_file:
        # for line in f:
        if ',"predicted_' in line:
            j = json.loads(line)
            if 'predicted_age' in j:
                age_times.append(datetime.fromisoformat(j.get('day_pt').replace(' UTC', '')))
                for key in age_keys:
                    age_lists[key].append(j.get(key))
            if 'predicted_gender' in j:
                gender_times.append(datetime.fromisoformat(j.get('day_pt').replace(' UTC', '')))
                for key in gender_keys:
                    gender_lists[key].append(j.get(key))

    print('done filling lists')
    print(f'age_times len = {len(age_times)}')
    print(f'gender_times len = {len(gender_times)}')

    if (len(age_times)):
        plt.title("Discord predicted age")
        for key in age_keys:
            print(f'plotting {key}')
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
        output = "No data for you :("

    document.getElementById("content").innerHTML = output

def main():

    global selected_file
    # Create a Python proxy for the callback function
    # process_file() is your function to process events from FileReader
    file_event = create_proxy(process_file)

    # Set the listener to the callback
    e = document.getElementById("myfile")
    e.addEventListener("change", file_event, False)

    def run_button(event):
        asyncio.ensure_future(do_the_thing(event, selected_file))


    button_event = create_proxy(run_button)
    button = document.getElementById('runbutton')
    button.addEventListener('click', button_event, False)

main()
