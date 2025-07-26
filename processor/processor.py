import pika
import json
import os
import re
import time

# --- Mock Error Pattern Detection ---
# In a real system, these would be loaded from a config file or DB
ERROR_PATTERNS = {
    "connection_error": re.compile(r".*(connection refused|timeout|failed to connect).*", re.IGNORECASE),
    "auth_failure": re.compile(r".*(authentication failed|access denied|unauthorized).*", re.IGNORECASE),
    "null_pointer": re.compile(r".*NullPointerException.*", re.IGNORECASE),
}

def get_error_pattern(log_message):
    """Checks a log message against predefined regex patterns."""
    for pattern_id, regex in ERROR_PATTERNS.items():
        if regex.search(log_message):
            return pattern_id
    return None

def process_metrics_message(body):
    """Processes a metrics message."""
    data = json.loads(body)
    print(f"✅ [Metrics] Received from Node '{data['node_id']}': CPU {data['cpu_usage']:.2f}%, RAM {data['ram_usage']:.2f}%")
    # In a real system, you would push this data to Prometheus or a TSDB.
    # e.g., prometheus_client.push_to_gateway(...)

def process_logs_message(body):
    """Processes a log message, enriching it with error patterns."""
    data = json.loads(body)
    message = data.get("message", "")
    pattern_id = get_error_pattern(message)
    
    if pattern_id:
        data['error_pattern_id'] = pattern_id
        print(f"🚨 [Logs] Detected error '{pattern_id}' from Node '{data['node_id']}': {message[:80]}...")
    else:
        print(f"ℹ️  [Logs] Received log from Node '{data['node_id']}': {message[:80]}...")
        
    # In a real system, you would send this enriched `data` to Elasticsearch.
    # e.g., es_client.index(index="logs", document=data)

def main():
    rabbitMQ_url = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
    
    # It's better to retry connection than fail immediately
    connection = None
    while not connection:
        try:
            connection = pika.BlockingConnection(pika.URLParameters(rabbitMQ_url))
            print("✅ Processor connected to RabbitMQ.")
        except pika.exceptions.AMQPConnectionError:
            print("❌ RabbitMQ not available, retrying in 5 seconds...")
            time.sleep(5)

    channel = connection.channel()
    channel.queue_declare(queue='metrics_queue', durable=True)
    # You would also declare a 'logs_queue' here
    
    def callback(ch, method, properties, body):
        # Here you would check the routing key or message type to decide which processor to use
        process_metrics_message(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue='metrics_queue', on_message_callback=callback)
    
    print('⏳ Processor is waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    main()