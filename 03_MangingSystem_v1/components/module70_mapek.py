
def mape_monitoring(flat_d1s, flat_d30s):
    metric = {"cpu": 0,
              "memory": 10,
              "cpu_temp": 50,
              "load1": 3,
              "busyworkers": 3,
              "response_ms": 5}
    return metric


def mape_analyzing(metric):
    state = {"health": 'good',  # = good/medium/critical
             "performance": 'good'}  # = good/bad
    
    return state


def mape_planning(metric, state, plan):
    plan = {"no": 1,  # = 1/2/3/4
            "clock": 'min'} # = min/max

    # Update the plan based on the state
    if state['health'] in ('good', 'medium'):
        plan['clock'] = 'max'
    if state['health'] == 'critical':
        plan['clock'] = 'min' 

    if state['performance'] == 'bad':
        plan['no'] = max(1, plan['no'] - 1)  # Decrease by 1 but not below 1

    if state['performance'] == 'good':
        plan['no'] = min(4, plan['no'] + 1)  # Increase by 1 but not above 4

