#!/usr/bin/python3
import BAC0
import time
import pandas as pd
from BAC0.core.proprietary_objects.jci import tec_short_point_list

"""
This sample creates an Excel file containing one sheet per controller found on the network
Each sheet contyains all the points known by BAC0. Some proprietary point could not display here.
"""

EXCEL_FILE_NAME = "all_controllers_and_points.xlsx"


def create_data(discovered_devices, network):
    devices = {}
    dataframes = {}
    for each in discovered_devices:
        name, vendor, address, device_id = each

        # try excep eventually as we may have some issues with werid devices
        if "TEC3000" in name:
            custom_obj_list = tec_short_point_list()
        else:
            custom_obj_list = None
        devices[name] = BAC0.device(
            address, device_id, network, poll=0, object_list=custom_obj_list
        )

        # While we are here, make a dataframe with device
        dataframes[name] = make_dataframe(devices[name])
    return (devices, dataframes)


def make_dataframe(dev):
    lst = {}
    for each in dev.points:
        lst[each.properties.name] = {
            "value": each.lastValue,
            "units or states": each.properties.units_state,
            "description": each.properties.description,
            "object": "{}:{}".format(each.properties.type, each.properties.address),
        }
    df = pd.DataFrame.from_dict(lst, orient="index")
    return df


def make_excel(dfs):
    with pd.ExcelWriter(EXCEL_FILE_NAME) as writer:
        for k, v in dfs.items():
            v.to_excel(writer, sheet_name=k)


def main():
    # bacnet = BAC0.connect(ip="192.168.1.10")
    
    # mac, device_id = bacnet.whois()[0]
    # print("mac: " + mac + ", device_id: " + device_id)
    # print("bacnet.devices: " + bacnet.devices)

    # objectList = bacnet.read(f'{mac} device {device_id} objectList')
    # print("objectList: " + objectList)
    # print("TRANE-Quick-Test: " + bacnet.read())

    bacnet = BAC0.lite()
    # [('192.168.1.20', 200), ('192.168.1.85', 120), ('192.168.1.20', 200), ('192.168.1.80', 80), ('192.168.1.88', 602), ('192.168.1.83', 125), ('192.168.1.10', 1), ('192.168.1.20', 200), ('192.168.1.20', 200), ('192.168.1.20', 200)]

    discovered_devices = bacnet.devices
    # [('SC-CHILLER-IOT', 'Trane', '192.168.1.20', 200), ('RP_UNO', 'BroadWin Technology, Inc.', '192.168.1.85', 120), ('BAC2004-ARM', 'Shanghai Sunfull Automation Co., LTD.', '192.168.1.88', 602), ('BCU-1', 'Trane', '192.168.1.10', 1)]

    name, vendor, address, device_id = discovered_devices[3]

    device = BAC0.device(address, device_id, bacnet, poll=0, object_list=None)

    device.points
    # Output all the datapoint inlcuding datapoint's name, and present data


if __name__ == "__main__":
    main()