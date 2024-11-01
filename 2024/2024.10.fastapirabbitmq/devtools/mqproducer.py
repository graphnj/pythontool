import json
import uuid

import pika
import time

MQ_USERNAME = 'admin'
MQ_PASSWORD ='123456'
MQ_HOST = '101.43.52.53'
MQ_PORT = 8072
MQ_virtualhost = '/zhizi'
MQ_queue = 'zhizialarm'


#user_info = pika.PlainCredentials('zhizi', 'zhizi567234')#用户名和密码
user_info = pika.PlainCredentials(MQ_USERNAME, MQ_PASSWORD)#用户名和密码
connection = pika.BlockingConnection(pika.ConnectionParameters(MQ_HOST, MQ_PORT, MQ_virtualhost, user_info))#连接服务器上的RabbitMQ服务

# 创建一个channel
channel = connection.channel()

# 如果指定的queue不存在，则会创建一个queue，如果已经存在 则不会做其他动作，生产者和消费者都做这一步的好处是
# 这样生产者和消费者就没有必要的先后启动顺序了
channel.queue_declare(queue='zhizialarm',durable=False)


alarm={
    "requestId":str(uuid.uuid4()),
"taskId":'task123',
"eventId":'20240712101124465',
"eventType":'垃圾满溢',
"eventDesc":'垃圾桶已满',
"eventTime":'1601234567',
"imgUrl":'https://tse1-mm.cn.bing.net/th/id/OIP-C.Vf0PjZtryNgbCMLEPTW0dgHaEK?rs=1&pid=ImgDetMain',
"deviceId":'32010208091000000001',
"channelId":'32010208091000000001'
}




for i in range(0, 10000):
    alarm['requestId']=str(uuid.uuid4())
    tm=time.time()
    alarm['eventId']=f'{int(tm*1000)}'
    alarm['eventTime']=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tm))
    data=json.dumps(alarm).encode('utf-8')
    channel.basic_publish(exchange='',#当前是一个简单模式，所以这里设置为空字符串就可以了
                          routing_key=MQ_queue,# 指定消息要发送到哪个queue
                          body=data# 指定要发送的消息
                          )
    time.sleep(2)

# 关闭连接
# connection.close()
