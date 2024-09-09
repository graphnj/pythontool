import random
import simpy


RANDOM_SEED = 42
NEW_SHIPS = 500  # 总货船数
ARRIVED_INTERVAL = (2, 15)  # 到来时间间隔
UPLOAD_TIME = (7, 20)  # 卸货时长

wait_times = []
upload_times = []


def my_print(*x):
    #pass
    print(*x)


def source(env, number, interval, counter):
    """进程用于生成核酸检测的人"""
    arrived_inter_time = [random.randint(*interval) for i in range(number)]
    arrived_time = [sum(arrived_inter_time[:i+1]) for i in range(len(arrived_inter_time))]
    my_print("到达时间", arrived_time)
    for i in range(number):
        c = ship(env, ' '*i*4 + 'person%02d' % i, counter, arrived_time[i])
        env.process(c)
    yield env.timeout(0)


def ship(env, name, docker, arrived_time):
    yield env.timeout(arrived_time)  # 到达船坞
    my_print(name, '到达时间', env.now)
    with docker.request() as req:  # 寻求进入
        yield req
        my_print(name, '进入时间', env.now)
        unload_time = random.randint(*UPLOAD_TIME)
        wait_time = env.now - arrived_time
        yield env.timeout(unload_time)
        my_print(name, '出港时间', env.now)
        wait_times.append(wait_time/NEW_SHIPS)
        upload_times.append(unload_time/NEW_SHIPS)


ans = []
for i in range(10):
    wait_times.clear()
    upload_times.clear()
    # Setup and start the simulation
    # random.seed(RANDOM_SEED)
    env = simpy.Environment()

    # Start processes and run
    docker = simpy.Resource(env, capacity=1)
    env.process(source(env, NEW_SHIPS, ARRIVED_INTERVAL, docker))
    env.run()

    ans.append(sum(wait_times))
print("每个船的平均等待时间", sum(ans) / len(ans))