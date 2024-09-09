
from numpy.random import *
from simpy import *

def rng(dis,param):
    """random number generator"""
    def generate():
        return dis(lam=param,size=1)[0]
    return generate

def erlang(k):
    """由k个指数分布拟合"""
    def exp2erlang(lam,size):
        res=[]
        for n in range(size):
            k_poisson= exponential(lam/k,size=k)
            sum=0
            for x in k_poisson:
                sum = sum + x
            res.append(sum)
        return res
    return exp2erlang


X=rng(erlang(3),5)
X()
#典型银行模型：FIFO
def bankSample(X,Y,Z,A,B,EX):
    """
银行排队服务例子

情景:
  一个柜台对客户进行服务, 服务耗时, 客户等候过长会离开柜台
    %X 表示时间间隔分布
    %Y 表示服务时间的分布
    %Z 表示服务台的个数
    %A 表示系统的容量,此处特殊化为客户的耐心时间分布
    %B 表示顾客数
    %以上参数必须有界，受到计算机精度限制，可以使用大常数近似无穷
    %C 表示服务规则,请修改函数
    %EX 传递了银行储蓄额的分布
  """
    #加入随机种子是为了对比模型的变化
    seed(2)
    def source(env, number, interval,counter):
        """生成客户"""
        for i in range(number):
            c = customer(env, '客户%04d' % i, counter, time_in_bank=Y(),account=EX())
            env.process(c)
            yield env.timeout(interval)
    #成功服务的客户
    SUCC=0
    #成功客户等待时间
    WAIT=0
    #成功客户逗留时间
    STAY=0
    #业务额
    AMT=0
    def customer(env, name, counter, time_in_bank,account):
        nonlocal WAIT
        nonlocal SUCC
        nonlocal STAY
        nonlocal AMT
        """顾客服务与离开仿真"""
        arrive = env.now
        #print('%7.4f  %s: 到达' % (arrive, name))
        with counter.request() as req:
            patience = A()
            # 直到到达或者失去耐心
            results = yield req | env.timeout(patience)
            wait = env.now - arrive

            if req in results:
                # 到达
                WAIT=WAIT+wait
                STAY=STAY+time_in_bank
                AMT= AMT + account
                #print('%7.4f %s:等待%6.3f' % (env.now, name, wait))
                yield env.timeout(time_in_bank)
                SUCC=SUCC+1
                #print('%7.4f %s:服务完成' % (env.now, name))
            else:
                # We reneged
                pass
                #print('%7.4f %s:等待%6.3f后离开' % (env.now, name, wait))
    # 初始化环境
    print('排队问题仿真')
    env = Environment()

    # 开始协程
    counter = Resource(env, capacity=Z)
    env.process(source(env, B, X(), counter))
    env.run()
    print("总服务人数：{0:n}人".format(SUCC))
    print("总营业额：{0:n}元".format(AMT))
    print("总计失去： {0:n}名客户".format(B-SUCC))
    print("损失率为： {0:n}%".format((B-SUCC)/B*100))
    print("平均等待时间：{0:n}".format(WAIT/SUCC) )
    print("平均耗费时间：{0:n}".format(STAY/SUCC) )


#间隔分布
X=rng(erlang(3),3)
#服务时间分布
Y=rng(erlang(3),10)
#耐心时间分布
A=rng(erlang(3),30)
#业务额分布正态
def normaltocurry(s):
    def normalcurry(lam,size):
        return normal(lam,s,size=size)
    return normalcurry
EX=rng(normaltocurry(200),1000)
bankSample(X,Y,1,A,1000,EX)