import json

import pika
import time

MQ_USERNAME = 'admin'
MQ_PASSWORD ='123456'
MQ_HOST = '101.43.52.53'
MQ_PORT = 8072
MQ_virtualhost = '/'
MQ_queue = 'zhizialarm'


#user_info = pika.PlainCredentials('zhizi', 'zhizi567234')#用户名和密码
user_info = pika.PlainCredentials(MQ_USERNAME, MQ_PASSWORD)#用户名和密码
connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_HOST, MQ_PORT, MQ_virtualhost, user_info))#连接服务器上的RabbitMQ服务

# 创建一个channel
channel = connection.channel()

# 如果指定的queue不存在，则会创建一个queue，如果已经存在 则不会做其他动作，生产者和消费者都做这一步的好处是
# 这样生产者和消费者就没有必要的先后启动顺序了
channel.queue_declare(queue='zhizialarm',durable=True)


# 回调函数
def callback(ch, method, properties, body):
    d=json.loads(body)
    print('消费者收到:{}'.format(d))


channel.basic_consume(queue='zhizialarm',  # 接收指定queue的消息
                      auto_ack=True,  # 指定为True，表示消息接收到后自动给消息发送方回复确认，已收到消息
                      on_message_callback=callback  # 设置收到消息的回调函数
                      )

print('Waiting for messages. To exit press CTRL+C')

# 一直处于等待接收消息的状态，如果没收到消息就一直处于阻塞状态，收到消息就调用上面的回调函数
channel.start_consuming()

