
# mysql 配置
MYSQL_CONFIG = {
    "host": '10.32.132.80',
    "port": 3306,
    "user": 'root',
    "password": '123456',
    "db": 'smart_assistant_1.4.0'
}

# rabbitmq 配置
# RABBITMQ_CONFIG = {
#     "host": '119.3.180.172',
#     "port": 11180,
#     "user": 'dyb',
#     "password": '123456',
#     "queue": 'zhizialarm'
# }
RABBITMQ_CONFIG = {
    "host": '101.43.52.53',
    "port": 8072,
    "user": 'admin',
    "password": '123456',
    "queue": 'zhizialarm',
    "virtualhost": '/%2Fzhizi'
}


# API 是否开启跨域，默认为False，如果需要开启，请设置为True
# is open cross domain
OPEN_CROSS_DOMAIN = True

LOG_PATH = "./log/"