#!/usr/bin/python3
import sys
from inspect import currentframe, getframeinfo
from datetime import datetime
import time
import os
import json
import redis
# import threading

DATASET = {'AUTO': False, 'VERSION': '0.0.1', 'DEBUG': False, 'VERBOSE': False, 'INTERVAL': 0, 'FILE': '', 'LOGFILE': '', 'DEVICE': '',
           'BROKER_IP': '', 'BROKER_PORT': 1883, 'BROKER_USER': '', 'BROKER_PW': '', 'BROKER_TOPIC': '/SensorPod/sensor1',
           'SENSOR_ID': 'sensor1', 'SENDOUT': False, 'BROKER_TYPE': 1, 'SLAVE_ID': 1, 'BAUDRATE': 9600, 'REDIS_KEY': 'm2c_data'}

# forwarderThread = threading.Thread(target = self.fill_in_sum_data, daemon=True)

OPTDIR = '/opt/skylab/trane_bacnet/'

TAGSFILE = OPTDIR + 'TRANE_SYSTEM_TAG.json'
f = open(TAGSFILE)
TAGS = json.load(f)
f.close()

r = redis.Redis(host='localhost', port=6379, db=0)


def get_env_var():
    DATASET['LOGFILE'] = os.environ.get('LOGFILE', '/var/log/')
    f = open(OPTDIR + 'VERSION')
    DATASET['VERSION'] = f.read()
    f.close()
    DATASET['DEVICE'] = os.environ.get('DEVICE', '/dev/ttyF1')
    DATASET['SLAVE_ID'] = int(os.environ.get('SLAVE_ID', 1))
    DATASET['INTERVAL'] = float(os.environ.get('INTERVAL', 1))
    # BROKER_TYPE: 0: kafka, 1: mqtt
    DATASET['BROKER_TYPE'] = float(os.environ.get('BROKER_TYPE', 1))
    DATASET['BROKER_IP'] = os.environ.get('BROKER_IP', '')
    DATASET['BROKER_PORT'] = int(os.environ.get('BROKER_PORT', 1883))
    DATASET['BROKER_USER'] = os.environ.get('BROKER_USER', '')
    DATASET['BROKER_PW'] = os.environ.get('BROKER_PW', '')
    DATASET['SENSOR_ID'] = os.environ.get('SENSOR_ID', DATASET['SENSOR_ID'])
    f = open('/etc/hostname')
    hostname = f.read().replace('\n', '')
    f.close()
    DATASET['BROKER_TOPIC'] = os.environ.get('BROKER_TOPIC', 'test_topic')
    DATASET['REDIS_KEY'] = os.environ.get('REDIS_KEY', 'm2c_data')

    DATASET['BAUDRATE'] = int(os.environ.get('BAUDRATE', 9600))


def get_thisfilename():
    cf = getframeinfo(currentframe())
    return cf.filename


def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno


def log(*objects, sep=' '):
    if DATASET['DEBUG']:
        print(str(datetime.now()) + ' - ', end='')
        print(get_linenumber() + ' - ', end='')
        print(*objects, sep=sep, file=sys.stdout)

        with open(DATASET['LOGFILE'], 'a') as f:
            print(str(datetime.now()) + ' - ', end='', file=f)
            print(get_linenumber() + ' - ', end='', file=f)
            print(*objects, sep=sep, file=f)
    else:
        print(str(datetime.now()) + ' - ', end='')
        print(*objects, sep=sep, file=sys.stdout)

        with open(DATASET['LOGFILE'], 'a') as f:
            print(str(datetime.now()) + ' - ', end='', file=f)
            print(*objects, sep=sep, file=f)


def help(myname):
    print('Version: ' + DATASET['VERSION'] + ', created by John Nguyen\n' +
          myname + ' is the convenient script to start reading vibration sensor data.\n\
Require pyserial to be installed \'pip install pyserial\'\n\
Require paho-mqtt to be installed \'pip install paho-mqtt\'\n\
\n\
Usage: ' + myname + ' [OPTIONS] [Parameters]')


def show_version():
    print('Version: ' + DATASET['VERSION'] + ', created by John Nguyen\n')


def get_data(open_serial):
    data = {}

    for tag in TAGS['tags']:
        reg_addr = tag['reg_addr']
        log('Register: ' + tag['name'] + ', addr: ' + str(reg_addr))
        try:
            if tag['nb_regs'] == '2':
                reg_data = open_serial.read_float(reg_addr)
            else:
                reg_data = open_serial.read_register(reg_addr)
        except Exception as err:
            log('Error: get_data: {}'.format(err))
            return -1
        data[tag['name']] = reg_data

    if DATASET['DEBUG']:
        log('Data: ' + str(data))

    return data


def main(argv):
    get_env_var()

    myname = get_thisfilename()
    # print('myname:', myname)
    tmparr = myname.split(
        '/')[3].split('.') if (myname.find('/') != -1) else myname.split('.')
    DATASET['LOGFILE'] = DATASET['LOGFILE'] + tmparr[0] + '.log'
    print('Info: LOGFILE:', DATASET['LOGFILE'])

    log('Info: VERSION:', DATASET['VERSION'])

    if len(DATASET['DEVICE']) == 0:
        log('Error: Serial Port must be specified')
        sys.exit(2)

    pid = os.getpid()
    log('Info: PID:', pid)
    log('Info: device: {}, slave id: {}'.format(
        DATASET['DEVICE'], DATASET['SLAVE_ID']))
    log('Info: Baudrate:', DATASET['BAUDRATE'])
    log('Info: MQTT Server ' +
        DATASET['BROKER_IP'] + ':' + str(DATASET['BROKER_PORT']))
    log('Info: BROKER_TOPIC:', DATASET['BROKER_TOPIC'])
    log('Info: REDIS_KEY:', DATASET['REDIS_KEY'])

    time.sleep(0.5)

    bacnet = BAC0.lite(ip=TAGS['BACNET_DEVICE']['devices'][0]['address'])

    while True:
        data = get_data(instrument)
        if data == -1:
            return -1

        msg = {'payload': {'Timestamp': str(datetime.now(
        )), 'SensorID': DATASET['SENSOR_ID'], 'data': data}, 'topic': DATASET['BROKER_TOPIC']}
        log(msg)
        r.rpush(DATASET['REDIS_KEY'], str(msg))

        time.sleep(DATASET['INTERVAL'])

    return 0


if __name__ == '__main__':
    main(sys.argv[1:])
