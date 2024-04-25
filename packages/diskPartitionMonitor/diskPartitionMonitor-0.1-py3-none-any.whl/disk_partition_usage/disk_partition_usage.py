import os
import json
import csv
import sys
import shutil
import datetime
import socket
import time
import logging

def get_disk_info(path=None):

    if os.name == "posix":
        partitions = ["/", "/boot", "/tmp", "/var", "/home", "/data","/app","/run","dev/","/opt","/depot","/sys","/crash"]
    else:
        partitions = ["{}:\\".format(letter) for letter in 'CDEFGHIJKLMNOPQRSTUVWXYZ' if os.path.exists("{}:\\".format(letter))]
 
    disk_info = []
    for partition in partitions:
        partition_info = {}
        partition_info['device'] = partition
        partition_info['mountpoint'] = partition
        if os.path.exists(partition):
            try:
                usage = shutil.disk_usage(partition)
                if usage.total > 0:
                    partition_info['total_space'] = usage.total
                    partition_info['used_space'] = {'bytes': usage.used, 'percentage': float(f"{(usage.used/usage.total)*100:.2f}")}
                    partition_info['free_space'] = usage.free
                    disk_info.append(partition_info)
            except PermissionError:
                continue

    if path != None:
        if os.path.exists(path):
            try:
                custom_usage = shutil.disk_usage(path)
                if custom_usage.total > 0:
                    custom_info = {
                        'mountpoint': "{1}",
                        'total_space': custom_usage.total,
                        'used_space': {'bytes': custom_usage.used, 'percentage': float(f"{(custom_usage.used/custom_usage.total)*100:.2f}")},
                        'free_space': custom_usage.free
                    }
                    disk_info.append(custom_info)
            except PermissionError:
                print(f"Permission error accessing {{path}}")

     
    total_space = sum(partition.get('total_space') for partition in disk_info)
    total_used = sum(partition['used_space'].get('bytes') for partition in disk_info)
    total_free = sum(partition.get('free_space') for partition in disk_info)

    return {
        'hostname':  socket.gethostname(),
        'os_type': "Linux" if os.name == "posix" else "Windows",
        'disk_total_space': total_space,
        'disk_used_space': {"bytes": total_used, "percentage": float(f"{(total_used/total_space)*100:.2f}")},
        'disk_free_space': total_free,
        'partitions': disk_info
    }


def readable_size(data):
    for partition, info in data['partitions'].items():
        info['total_space'] = str(round(info['total_space'] / (1024**3), 2)) + ' GB'
        info['used_space'] = str(round(info['used_space']['bytes'] / (1024**3), 2)) + ' GB'
        info['free_space'] = str(round(info['free_space'] / (1024**3), 2)) + ' GB'

    # Convert total disk space to gigabytes with two decimal points and add 'GB' suffix
    data['disk_total_space'] = str(round(data['disk_total_space'] / (1024**3), 2)) + ' GB'
    data['disk_used_space'] = str(round(data['disk_used_space']['bytes'] / (1024**3), 2)) + ' GB'
    data['disk_free_space'] = str(round(data['disk_free_space'] / (1024**3), 2)) + ' GB'
    return json.dumps(data, indent=4)


def write_log(data, path, readable):
    try:
        merged_data = {}  # Initialize a dictionary to store merged data
        merged_data['@timestamp'] = datetime.datetime.now().isoformat()
        merged_data['hostname'] = data['hostname']
        merged_data['os_type'] = data.get('os_type', '') 
        merged_data['disk_total_space'] = data['disk_total_space'] 
        merged_data['disk_free_space'] = data['disk_free_space']
        merged_data['disk_used_space'] = data['disk_used_space']
        partitions = {}
        for partition in data['partitions']:
            mountpoint = partition['mountpoint']
            partition_data = {
                'mountpoint': partition['mountpoint'],
                'total_space': partition['total_space'], 
                'used_space': partition['used_space'],  
                'free_space': partition['free_space'] 
            }
            partitions[mountpoint] = partition_data
        merged_data['partitions'] = partitions

        print(merged_data)
        with open("{}disk_usage.log".format(path), 'a') as f:
            f.write(json.dumps(merged_data) + '\n')
        # write_json(merged_data, path, readable)
    except Exception as e:
        print(f"Error occurred while formatting log data: {e}")

def write_json(data, path, readable):
    if readable == 'True':
        json_output = readable_size(data)
    else:
        json_output = json.dumps(data, indent=4)
    print(json_output)

    with open('{}{}_disk_usage.json'.format(path, data['hostname']), 'w') as json_file:
        json_file.write(json_output)