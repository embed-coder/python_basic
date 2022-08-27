#!/bin/bash

RUN_DIR="/opt/skylab/liftsensorpod/trane_bacnet"

# declare -x BROKER_IP="54.169.190.147"
# declare -x BROKER_PORT="1883"
# declare -x BROKER_PW="SkyLab@I0T!"
# declare -x BROKER_TOPIC="hdb-sensorpod"
# declare -x BROKER_TYPE="1"
# declare -x BROKER_USER="skylab_lmd"
# declare -x DEBIAN_FRONTEND="noninteractive"
# declare -x DEVICE="/dev/ttyUSB0"
# declare -x DEVICE_ID="590006-A-SensorPod"
# declare -x FAST_MEASURE="1"
# declare -x HOME="/root"
# declare -x HOSTNAME="skylab-Dev"
# declare -x INTERVAL="2"
# declare -x SENSOR_ID="lift-laser-sensor-1"

${RUN_DIR}/trane_bacnet &

while sleep 10; do
    ps aux | grep trane_bacnet\/trane_bacnet | grep -q -v grep
    if [ $? -ne 0 ]; then
        echo "Application has already exited -> restart"
        ${RUN_DIR}/trane_bacnet -a -s &
    fi
done
