import matplotlib.pyplot as plt
import pandas as pd
import asyncio
from js import document, FileReader
from pyodide import create_proxy

async def process_file(event):
    fileList = event.target.files.to_py()

    for f in fileList:
        data = await f.text()
        document.getElementById("content").innerHTML = data



def main():
    # Create a Python proxy for the callback function
    # process_file() is your function to process events from FileReader
    file_event = create_proxy(process_file)

    # Set the listener to the callback
    e = document.getElementById("myfile")
    e.addEventListener("change", file_event, False)

main()
