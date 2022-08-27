import imp
import sys
from inspect import currentframe, getframeinfo
from datetime import datetime
import time
import paho.mqtt.client as mqtt
import os
import json
import redis
import re
from zipfile import ZipFile

DATASET = {'AUTO': False, 'VERSION': '0.0.1', 'DEBUG': False, 'VERBOSE': False, 'INTERVAL': 0, 'FILE': '', 'LOGFILE': '', 'DEVICE': '', 'BROKER_IP': '54.169.190.147', 'BROKER_PORT': 1883, 'BROKER_USER': 'skylab_lmd', 'BROKER_PW': 'SkyLab@I0T!', 'BROKER_TOPIC': '/SensorPod/forwarder', 'SENSOR_ID': 'forwarder', 'SENDOUT': False, 'BROKER_TYPE': 1, 'SLAVE_ID': 1, 'BAUDRATE': 9600, 'LOGSIZE': 100000000, 'LOGFILES': 7}

myThread = None

OPTDIR = '/opt/skylab/liftsensorpod/forwarder/'

r = redis.Redis(host='localhost', port=6379, db=0)

def get_env_var():
    DATASET['LOGFILE'] = os.environ.get('LOGFILE', '/var/log/')
    f = open(OPTDIR + 'VERSION')
    DATASET['VERSION'] = f.read()
    f.close()
    DATASET['DEVICE'] = os.environ.get('DEVICE', '/dev/ttyF1')
    DATASET['SLAVE_ID'] = int(os.environ.get('SLAVE_ID', 1))
    DATASET['INTERVAL'] = float(os.environ.get('INTERVAL', 0.1))
    # BROKER_TYPE: 0: kafka, 1: mqtt
    DATASET['BROKER_TYPE'] = float(os.environ.get('BROKER_TYPE', 1))
    DATASET['BROKER_IP'] = os.environ.get('BROKER_IP', '54.169.190.147')
    DATASET['BROKER_PORT'] = int(os.environ.get('BROKER_PORT', 1883))
    DATASET['BROKER_USER'] = os.environ.get('BROKER_USER', 'skylab_lmd')
    DATASET['BROKER_PW'] = os.environ.get('BROKER_PW', 'SkyLab@I0T!')
    DATASET['SENSOR_ID'] = os.environ.get('SENSOR_ID', DATASET['SENSOR_ID'])
    f = open('/etc/hostname')
    hostname = f.read().replace('\n', '')
    f.close()
    DATASET['REDIS_KEY'] = os.environ.get('REDIS_KEY', 'm2c_data')
    DATASET['BAUDRATE'] = int(os.environ.get('BAUDRATE', 9600))

def get_thisfilename():
    cf = getframeinfo(currentframe())
    return cf.filename

def get_linenumber():
    cf = currentframe()
    return cf.f_back.f_lineno

def log(*objects, sep=' '):
    try:
        if os.path.getsize(DATASET['LOGFILE']) > DATASET['LOGSIZE']:
            os.remove(DATASET['LOGFILE'])
            # LOGFILEZIP= DATASET['LOGFILE'] + '-' + re.sub('[:. -]', '', str(datetime.now()))
            # os.rename(DATASET['LOGFILE'], LOGFILEZIP)
            # with ZipFile('spam.zip', 'w') as myzip:
            #     myzip.write(LOGFILEZIP + '.zip')
    except Exception as e:
        print('log: Exception:', e)

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
    print('Version: ' + DATASET['VERSION'] + ', created by John Nguyen\n' + \
myname + ' is the convenient script to start reading vibration sensor data.\n\
Require pyserial to be installed \'pip install pyserial\'\n\
Require paho-mqtt to be installed \'pip install paho-mqtt\'\n\
\n\
Usage: ' + myname + ' [OPTIONS] [Parameters]')

def show_version():
    print('Version: ' + DATASET['VERSION'] + ', created by John Nguyen\n')

def get_data(r_data):
    data = {}

    decoded_data = r_data.decode("utf-8")
    decoded_data = decoded_data.replace("\'", "\"")
    parsed_data = json.loads(decoded_data)
    if DATASET['DEBUG']:
        log('Data: ' + str(parsed_data))
    
    data = parsed_data['payload']
    topic = parsed_data['topic']
    
    return data, topic

MQTTReturnCodes = {0: 'Connection successful', 1: 'Connection refused – incorrect protocol version', 2: 'Connection refused – invalid client identifier', 3: 'Connection refused – server unavailable', 4: 'Connection refused – bad username or password', 5: 'Connection refused – not authorised'}
def mqtt_on_connect(client, userdata, flags, rc):
    if rc == 0:
      log("Mqtt connected ok")
    else:
        log("Mqtt bad connection Returned code: {}, {}".format(rc, MQTTReturnCodes[rc]))
  
def main(argv):
    get_env_var()

    myname = get_thisfilename()
    # print('myname:', myname)
    tmparr = myname.split('/')[3].split('.') if (myname.find('/') != -1) else myname.split('.')
    DATASET['LOGFILE'] = DATASET['LOGFILE'] + tmparr[0] + '.log'
    print('Info: LOGFILE:', DATASET['LOGFILE'])

    log('Info: VERSION:', DATASET['VERSION'])

    if len(DATASET['DEVICE']) == 0:
        log('Error: Serial Port must be specified')
        sys.exit(2)
        
    pid = os.getpid()
    log('Info: PID:', pid)
    log('Info: device: {}, slave id: {}'.format(DATASET['DEVICE'], DATASET['SLAVE_ID']))
    log('Info: Baudrate:', DATASET['BAUDRATE'])
    log('Info: MQTT Server ' + DATASET['BROKER_IP'] + ':' + str(DATASET['BROKER_PORT']))
    log('Info: REDIS_KEY:', DATASET['REDIS_KEY'])
    
    time.sleep(0.5)

    mqttc = mqtt.Client()
    if len(DATASET['BROKER_USER']) != 0:
        mqttc.username_pw_set(DATASET['BROKER_USER'], DATASET['BROKER_PW'])
    log('Info: Connecting to ' + DATASET['BROKER_IP'] + ':' + str(DATASET['BROKER_PORT']))
    mqttc.on_connect=mqtt_on_connect
    log('Info: Connecting to ' + DATASET['BROKER_IP'] + ':' + str(DATASET['BROKER_PORT']))
    mqttc.connect(DATASET['BROKER_IP'], DATASET['BROKER_PORT'])
    mqttc.loop_start()  #Start loop

    while True:
        message = r.lpop(DATASET['REDIS_KEY'])
        if message:
            msg, topic = get_data(message)
            log('topic:', topic)
            log('msg:', msg)
            infot = mqttc.publish(topic, json.dumps(msg), qos=0)
            infot.wait_for_publish()

        time.sleep(DATASET['INTERVAL'])

    return 0

if __name__ == '__main__':
    main(sys.argv[1:])