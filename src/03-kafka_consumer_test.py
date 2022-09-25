from kafka import KafkaConsumer
import sys, getopt

def main(argv):
  kafka_server = "52.237.74.42"
  #kafka_server = "172.17.10.244"
  kafka_port = "9092"
  #kafka_topic = "fd_img_19r2"
  #kafka_topic = "fe_vec_19r2"
  # kafka_topic = "test_topic"
  # kafka_topic = "origin_mpjeg_topic"
  # kafka_topic = "custom_mpjeg_topic"
  kafka_topic = "test"

  try:
    opts, args = getopt.getopt(argv,"hs:p:t:",["server=","port=","topic="])
  # except getopt.GetoptError:
  except getopt.error as err:
    # output error, and return with an error code
    print (str(err))
    print ("Usage: kafka_consumer_test.py -s <server> -p <port> -t <topic>\n\
    Ex: kafka_consumer_test.py -s localhost -p 9092 -t test \n")
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print ("Usage: kafka_consumer_test.py -s <server> -p <port> -t <topic>\n\
      Ex: kafka_consumer_test.py localhost 9092 test \n")
      sys.exit()
    elif opt in ("-s", "--server"):
      kafka_server = arg
    elif opt in ("-p", "--port"):
      kafka_port = arg
    elif opt in ("-t", "--topic"):
      kafka_topic = arg

  consumer = KafkaConsumer(kafka_topic, bootstrap_servers=[kafka_server+":"+kafka_port], auto_commit_interval_ms=1000, auto_offset_reset='earliest', consumer_timeout_ms=20000)
  for msg in consumer:
    print (msg)

if __name__ == "__main__":
  main(sys.argv[1:])
