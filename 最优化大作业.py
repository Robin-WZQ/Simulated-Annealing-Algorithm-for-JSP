#-------------------------------
# Simulated Annealing Algorithm for Job Shop Scheduling Problem
# Created by WZQ
# 2021/7/25
#-------------------------------

import random
import math
import time

temperature = 5000
DLATA = 0.99
EPS=10e-4
INLOOP = 3000

def inititial():
    '''
    输入数据，初始化
    cost[i][j]=t:第i个元件在第j个机器上加工的时间为t
    manage[j][k]=i:第j台机器上加工第k个原件为i
    0<=i<=m-1,0<=j<=n-1
    '''
    m,n = map(int,input().split())
    cost = [[] for i in range(m)]
    for i in range(m):
        line = input()
        line = ' '.join(line.split()).split(" ")
        for j in range(round(len(line)/2)):         
            cost[i].append(eval(line[2*j+1]))
    manage = [[i for i in range(m)] for j in range(n)]
    return m,n,cost,manage

def randomExChange(m,n,manage):
    '''
    产生新解，随机交换某两个零件在某个机器上的的加工顺序
    '''
    x = random.randint(0,m-1)
    y = random.randint(0,m-1)
    for j in range(n):
        temp = manage[j][x]
        manage[j][x] = manage[j][y]
        manage[j][y] = temp
    return manage

def output(num,order):
    '''
    输出最优时间，输出最优调度方案
    '''
    print("最优加工时间为：{}".format(num))
    print("顺序为{}".format(order))
    return 0

def evaluate(cost,manage,n,m):
    '''
    评估函数，返回加工时间
    '''
    time= [[0 for i in range(m)] for j in range(n)] #定义时间二维表
    a=0
    for i in range(m):
        a += cost[manage[0][i]][0] #初始化第一行的时间表
        time[0][i]=a
    for j in range(1,n):
        for i in range(m):
            position = manage[j-1].index(manage[j][i])
            if(i==0):
                bigger = time[j-1][position]
            else: 
                bigger = max(time[j-1][position],time[j][i-1])
            time[j][i]=bigger+cost[manage[j][i]][j]
    return time[n-1][m-1]

def main():
    '''
    模拟退火算法主函数
    '''
    Pnum,Mnum,cost,manage = inititial()
    t = evaluate(cost,manage,Mnum,Pnum)
    
    best = t
    T = float(temperature)
    startTime=time.perf_counter()
    
    #外循环迭代，终止于温度小于阈值
    while(T>EPS):
        #内循环
        T = T * DLATA
        for iter in range(INLOOP):
            temporary = manage
            temporary = randomExChange(Pnum,Mnum,temporary)
            new_t = float(evaluate(cost,temporary,Mnum,Pnum))
            if(new_t<t):
                t = new_t
                manage = temporary
                best_manage = manage
                if(t<best):
                    best=t #保存最优解
            else:
                p = math.exp((t-new_t)/T)
                if(random.random()<=p):
                    t = new_t
                    manage = temporary
                else:
                    continue
    output(int(best),best_manage[0])
    endTime=time.perf_counter()
    print("程序运行时长为{}秒".format(round(endTime-startTime,2))) 


if __name__ == '__main__':
    main()
