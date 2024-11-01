import time

import pika
from configs.server_config import RABBITMQ_CONFIG
from urllib import parse
import json

from contextlib import contextmanager
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from configs.server_config import MYSQL_CONFIG

from server.utils.logUtils import log


HOST = MYSQL_CONFIG['host']
PORT = MYSQL_CONFIG['port']
USERNAME = MYSQL_CONFIG['user']
PASSWORD = parse.quote_plus(MYSQL_CONFIG['password'])
DB = MYSQL_CONFIG['db']

DB_URI = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'

engine = create_engine(DB_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

MQ_HOST = RABBITMQ_CONFIG['host']
MQ_PORT = RABBITMQ_CONFIG['port']
MQ_USERNAME = RABBITMQ_CONFIG['user']
MQ_PASSWORD = RABBITMQ_CONFIG['password']
MQ_queue = RABBITMQ_CONFIG['queue']
MQ_virtualhost=RABBITMQ_CONFIG['virtualhost']


user_info = pika.PlainCredentials(MQ_USERNAME, MQ_PASSWORD)

ConnectFail = True


@contextmanager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



from aio_pika import connect, connect_robust, IncomingMessage


# zhujinhua 20241024  注
# 一定注意
# virtualhost  如果为/xxx  则需要用/%2Fxxx
# rabbitmq 的限制
async def async_consume_messages():
    connurl=f"amqp://{MQ_USERNAME}:{MQ_PASSWORD}@{MQ_HOST}:{MQ_PORT}{MQ_virtualhost}"
    log.info(f'connecting rabbitmq:{connurl}')
    connection = await connect_robust(connurl)
    channel = await connection.channel()
    queue = await channel.declare_queue(MQ_queue)#,durable=True)

    async def process_message(message: IncomingMessage):
        async with message.process():
            msgstr = message.body.decode()
            jsonmsg=json.loads(msgstr)
            log.info(f"Rabbitmq async Received: {jsonmsg}")
            # 调用 alarm_notice 函数
            # with get_db() as db:
            #     try:
            #         msg = json.loads(msgstr)
            #         response = alarm_notice(AlarmParam(**msg), db)
            #         log.info(f'savedb:{response}')
            #     except:
            #         log.error("预警入库过程有误")

    await queue.consume(process_message)













def sync_consume_messages():


    global ConnectFail

    while ConnectFail:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host = MQ_HOST, port = MQ_PORT, virtual_host=MQ_virtualhost, credentials=user_info))
            #if connection
            a=1
            ConnectFail = False
        except Exception as e:
            log.error(f'connect rabbitmq {MQ_HOST}:{MQ_PORT} fail')
            time.sleep(10)

    channel = connection.channel()
    channel.queue_declare(queue=MQ_queue,durable=True)

    def callback(ch, method, properties, body):
        channel.basic_ack(method.delivery_tag)
        message = json.loads(body)
        print(f"mq Received message: {message}")

        # 调用 alarm_notice 函数
        with get_db() as db:
            try:
                print(message)
                #response = alarm_notice(AlarmParam(**message), db)
            except:
                print("预警入库过程有误")

    channel.basic_consume(queue=MQ_queue, on_message_callback=callback)
    log.info("start process rabbitmq msg... ")
    channel.start_consuming()



# 单独启动时
if __name__ == "__main__":
    sync_consume_messages()