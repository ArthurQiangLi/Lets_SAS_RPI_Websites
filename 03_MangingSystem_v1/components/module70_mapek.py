
def mape_monitoring(dic):
    if(dic == {}):
        return {}
    metric = {"cpu": float(dic['cpu']), # 3.8
              "memory": float(dic['memory']), # 44.7
              "cpu_temp": float(dic['cpu_temperature']),  # 58.5
              "load1": float(dic['apache2metrics_Load1']),
              "busyworkers": float(dic['apache2metrics_BusyWorkers']), #3,
              "response_ms": float(dic['apache2metrics_DurationPerReq'])}# 5}
    return metric


def mape_analyzing(metric):
    if not metric:
        return {}
    state = {"health": 'good',  # = good/medium/critical
             "performance": 'good'}  # = good/bad
    if(metric['cpu_temp'] > 70):
        state['health'] = 'critical'
    elif(metric['cpu'] > 60 or metric['memory']>60 or metric['cpu_temp']>60):
        state['health'] = 'bad'
    else:
        state['health'] = 'good'

    if(metric['load1']>3 or metric['response_ms']>10 or metric['busyworkers']>30):
        state['performance'] = 'bad'
    else:
        state['performance'] = 'good'

    return state


def mape_planning(metric, state, plan):
    if not metric or not state:
        return plan
    # plan = {"no": 1,  # = 1/2/3/4
    #         "clock": 'min'} # = min/max

    # Update the plan based on the state
    if state['health'] in ('good', 'medium'):
        plan['clock'] = 'max'
    if state['health'] == 'critical':
        plan['clock'] = 'min' 

    if state['performance'] == 'bad':
        plan['no'] = min(4, plan['no'] + 1)  # Decrease by 1 but not below 1

    if state['performance'] == 'good':
        plan['no'] = max(1, plan['no'] - 1)  # Increase by 1 but not above 4

    return plan


##
# Testing




dic = {
 'Timestamp': '2024-11-27 15:57:47',
 'cpu': '70',
 'memory': '44.7',
 'cpu_temperature': '78.5',
 'arm_clock': '1400.0',
 'total_cpu': '42.0',
 'throttled_status_under_voltage': 'True',
 'throttled_status_currently_throttled': 'False',
 'throttled_status_freq_capped': 'True',
 'throttled_status_under_voltage_occurred': 'True',
 'throttled_status_throttling_occurred': 'False',
 'throttled_status_freq_capped_occurred': 'True',
 'color': '#325103',
 'age': '6d, 3h, 57m, 46s',
 'watchdog': 'True',
 'apache_active': 'True',
 'temp': '1.19',
 'humidity': '83',
 'weather': 'broken clouds',
 'apache2metrics_TotalAccesses': '14955',
 'apache2metrics_TotalkBytes': '24428',
 'apache2metrics_BusyWorkers': '1',
 'apache2metrics_IdleWorkers': '49',
 'apache2metrics_Processes': '2',
 'apache2metrics_ConnsTotal': '0',
 'apache2metrics_DurationPerReq': '1.84821',
 'apache2metrics_Load1': '2.4',
 'apache2metrics_Load5': '1.7',
 'apache2metrics_ServerUptime': '3d 20h 35m 5s'
}
plan = {"no": 3,  # = 1/2/3/4
        "clock": 'min'} # = min/max

metric = mape_monitoring(dic)
print(metric)
# calculate utilities
state = mape_analyzing(metric)
# planning
plan = mape_planning(metric, state, plan)
# executing

mapek = state | plan  # log data to plot
print(mapek)

