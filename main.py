import sys

from matplotlib.figure import Figure
if sys.platform == 'emscripten':
    from js import document, FileReader
    from pyodide.ffi import create_proxy
import glob
import json
import asyncio
from typing import Final
from datetime import datetime, timedelta
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.axes as mpl_axes
if sys.platform == 'emscripten':
    matplotlib.use("module://matplotlib_pyodide.wasm_backend")
# matplotlib.use("module://matplotlib_pyodide.html5_canvas_backend")
def annotate_maximums(axis: mpl_axes.Axes,
                      dates: list[datetime],
                      values: list[float],
                      key: str) -> None:
    local_max = max(values)
    bbox = dict(boxstyle="round", fc="0.95")
    arrowprops = dict(arrowstyle="->")
    offset = 36
    x = dates[values.index(local_max)]
    y = local_max
    axis.annotate(f'{key.removeprefix('prob_')} max = ({x.strftime("%Y-%m-%d")},{local_max:.2f})',
                  xy=(x, y),
                  xytext=(
                      0.5 * offset,
                      offset if y < 0.8 else -offset),
                  textcoords='offset points',
                  bbox=bbox, arrowprops=arrowprops)

async def do_plot(event) -> None:

    VERSION = "0.2"

    print("Crunching the data...")

    age_dates: list[datetime] = []
    age_keys: Final[list[str]] = ["prob_13_17", "prob_18_24", "prob_25_34", "prob_35_over"]
    age_lists: dict[str, list[float]] = {k:[] for k in age_keys}
    gender_dates: list[datetime] = []
    gender_keys: Final[list[str]] = ["prob_male", "prob_female", "prob_non_binary_gender_expansive"]
    gender_lists: dict[str, list[float]] = {k:[] for k in gender_keys}


    activity_files = glob.glob("/data/events-*-*-of-*.json")
    user_id = None
    for activity_file in activity_files:
        print(f"Processing {activity_file}")
        with open(activity_file, 'r') as f:
            for line in f:
                if ',"predicted_' in line:
                    j = json.loads(line)
                    if (not user_id) and ('user_id' in j):
                        user_id = j.get('user_id')
                    if 'predicted_age' in j:
                        age_dates.append(datetime.fromisoformat(j.get('day_pt').replace(' UTC', '')))
                        for key in age_keys:
                            age_lists[key].append(j.get(key))
                    if 'predicted_gender' in j:
                        gender_dates.append(datetime.fromisoformat(j.get('day_pt').replace(' UTC', '')))
                        for key in gender_keys:
                            gender_lists[key].append(j.get(key))

    print(f'age points = {len(age_dates)}')
    print(f'gender points = {len(gender_dates)}')

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

    common_dates = list(set(gender_dates) | set(age_dates))
    xmin = min(age_dates[0], gender_dates[0])
    xmax = max(age_dates[-1], gender_dates[-1])
    for ax in axs:
        ax.set_xlim(xmin - timedelta(days=30), xmax + timedelta(days=30))



    if (len(age_dates)):
        fig.suptitle(f"Discord data for user_id {user_id}")
        age_ax.set_title("Predicted age")
        for key in age_keys:
            print(f'plotting {key}')
            annotate_maximums(age_ax, age_dates, age_lists[key], key)
            age_ax.plot(*zip(*sorted(zip(age_dates, age_lists[key]))), marker='o')
        age_ax.legend(["13-17", "18-24", "25-34", "35+"])

    if (len(gender_dates)):
        gender_ax.set_title("Predicted gender")
        for key in gender_keys:
            annotate_maximums(gender_ax, gender_dates, gender_lists[key], key)
            gender_ax.plot(*zip(*sorted(zip(gender_dates, gender_lists[key]))), marker='o')
        gender_ax.legend(["male", "female", "non-binary"])
        fig.text(0, 0, f"created with discord data analyzer v{VERSION} https://dda.metacringe.com/", verticalalignment='bottom')


    if len(age_dates) == 0 and len(gender_dates) == 0:
        print("No data for you :(")
    else:
        # plt.tight_layout()
        plt.show()

def main():

    button_event = create_proxy(do_plot)
    button = document.getElementById('runbutton')
    button.addEventListener('click', button_event, False)

    print("👋 I am loaded now, push the button!")

if sys.platform == 'emscripten':
    main()
