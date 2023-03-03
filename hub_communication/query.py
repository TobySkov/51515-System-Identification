"""
Query data from hub.

Inpirational projects:
https://pybricks.com/projects/tutorials/wireless/hub-to-device/pc-communication/
https://github.com/hbldh/bleak/blob/master/examples/async_callback_with_queue.py
https://stackoverflow.com/questions/65352682/python-asyncio-pythonic-way-of-waiting-until-condition-satisfied
"""

import asyncio
import pandas as pd
from pathlib import Path
from bleak import BleakScanner, BleakClient


async def run_ble_client(address: str, char_uuid: str, queue: list):


    async def callback_handler(_, data):
        """Handling incoming data"""
        print("Data recieved")
        queue.append(data.decode())

    async def check_finished(flag):
        """Checking if all data has been recieved"""
        while True:
            if len(queue) != 0:
                if queue[-1][-4:] == "Done":
                    break
                else:
                    await asyncio.sleep(0.2)
            else:
                await asyncio.sleep(0.2)
        flag.set()

    async with BleakClient(address) as client:
        """Connecting with client and starting notification"""
        print(f"Connected: {client.is_connected}. Start hub program...")
        await client.start_notify(char_uuid, callback_handler)

        flag = asyncio.Event()
        asyncio.create_task(check_finished(flag))
        await flag.wait()

        await client.stop_notify(char_uuid)


def hub_filter(device, ad):
    """Finding hub address"""
    HUB_NAME = "Pybricks Hub"
    return device.name and device.name.lower() == HUB_NAME.lower()


def data_filter(queue: list, path: Path) -> pd.DataFrame:
    """Filtering data recieved from hub"""
    print("Start data filtering...", end="")
    all_data = ''.join(queue)

    assert all_data[:6] == 'Start,'
    assert all_data[-5:] == ';Done'

    header, data = all_data.split("Header-To-Data;")

    columns = header.split(',')
    # Removing "Start-Header;";
    del columns[0]

    lines = data.split(';')
    # Removing "End-Measurements;"
    del lines[-1]

    matrix = []
    for line in lines:
        row = []
        for num in line.split(','):
            row.append(float(num))
        matrix.append(row)

    data_structured = pd.DataFrame.from_records(data=matrix, columns=columns)
    data_structured.to_pickle(path=path)
    print("Done")



async def main():
    address = await BleakScanner.find_device_by_filter(hub_filter)
    char_uuid = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
    queue = []
    await run_ble_client(address, char_uuid, queue)
    data_folder = Path(__file__).parents[1].joinpath('test_results')
    data_filter(
        queue=queue, 
        path=data_folder.joinpath('2023_03_03_Motor_1_Program_1.pkl')
    )


if __name__ == "__main__":
    asyncio.run(main())

