import numpy as np
import queue_sim

def heuristic_single_step_lookahead_search(time_horizon,arrivals,serving_time,sla_rt,max_servers,time_delta):
    max_c=-1
    max_reward=-10000
    st=serving_time
    min_st=st
    min_rt=-1
    min_ql=-1

    for c in range(1, max_servers + 1):
        queue=np.array([[0,0],[0,0]])
        servers=np.zeros(c,dtype=int)
        avg_response_time, queue_length = queue_sim.mmc(arrivals,queue,st,time_horizon, servers, time_delta)
        sla_gain = 0
        e_consumption = 0.5 * c / max_servers

        if avg_response_time <= sla_rt:
            sla_gain = 1
        else:
            sla_gain = -1
            st = round(st * (1 - c / max_servers))
            

        reward = sla_gain - e_consumption
        #print(f'Reward for {c} is: {reward}')
        #print(f'Serving time is: {st}')

        if reward > max_reward:
            max_c = c
            max_reward = reward
            min_rt = avg_response_time
            min_ql = queue_length
            min_st = st

        #print(f'Best reward is: {max_reward}')
        #print(f'Best c is: {max_c}')

    best_c = max_c
    best_reward = max_reward
    best_st = min_st
    best_rt = min_rt
    best_ql = min_ql

    return best_c, best_reward, best_st, best_rt, best_ql

def test_controllers(c,scl,th,st):
    time_horizon=th
    #print('')
    arrivals=np.rint(np.random.exponential(scale=scl,size=time_horizon))
    print(f"\n\n Arrivals created : {arrivals}\n\n")
    #queue=np.array([[0,0],[0,0]])
    serving_time=1
    print(f"\n\n Serving time created : {serving_time}\n\n")
    max_servers=np.random.randint(1,c)
    print(f"\n\n Max Servers created : {max_servers}\n\n")
    time_delta=np.random.randint(scl,scl+10)
    print(f"\n\n Time delta is : {time_delta}\n\n")
    sla_rt=np.random.randint(time_delta*serving_time,time_delta*serving_time*1.5)
    print(f"\n\n SLA Response Time is : {sla_rt}\n\n")
    best_c,best_reward,best_st,best_rt,best_ql=heuristic_single_step_lookahead_search(time_horizon=time_horizon,arrivals=arrivals,serving_time=serving_time,sla_rt=sla_rt,max_servers=max_servers,time_delta=time_delta)
    print(f'\n\nBest Response Time is : {best_rt}\n\n Best Queue Lenght is : {best_ql}\n\n Best Serving Time : {best_st}\n\n Best Reward : {best_reward}\n\n Best Number of Servers : {best_c}')

def main():
    c=16
    scl=10
    th=10
    st=1
    test_controllers(c,scl,th,st)

if __name__ == '__main__':
    main()