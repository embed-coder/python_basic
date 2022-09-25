from kafka import KafkaProducer
import time
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
  kafka_message = str.encode('some_message_bytes from John')

  try:
    opts, args = getopt.getopt(argv,"hs:p:t:m:",["server=","port=","topic=","message="])
  # except getopt.GetoptError:
  except getopt.error as err:
    # output error, and return with an error code
    print ("Usage: kafka_consumer_test.py -s <server> -p <port> -t <topic>\n\
    Ex: kafka_consumer_test.py localhost 9092 test \n")
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
    elif opt in ("-m", "--message"):
      kafka_message = str.encode(arg)

  producer = KafkaProducer(bootstrap_servers=[kafka_server+":"+kafka_port])

  # for _ in range(100):
    # producer.send(kafka_topic, b'some_message_bytes from John')
    ## producer.flush()
    # time.sleep(0.01)

  producer.send(kafka_topic, kafka_message)
  producer.flush()

if __name__ == "__main__":
  main(sys.argv[1:])
