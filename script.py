# import matplotlib.pyplot as plt
# import pandas as pd
import asyncio
from js import document, FileReader
from pyodide.ffi import create_proxy

selected_file = None

async def process_file(event):
    global selected_file

    fileList = event.target.files.to_py()
    for f in fileList:
        selected_file = f

    # for f in fileList:
    #     data = await f.text()
    #     count = 0;
    #     for line in data:
    #         count = count + 1
    #
        # document.getElementById("output").innerHTML = "\nfile inputted\n"
    print("file inputted!")

async def do_the_thing(event, file):

    data: str = await file.text()
    count = 0;
    for thing in data:
        count += 1

    document.getElementById("content").innerHTML = str(count)

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
