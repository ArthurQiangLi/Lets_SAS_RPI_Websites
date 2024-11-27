# Data flow in app_v1.py

## Updated every 1s

1. extern_get_cpu_memory_usage {"cpu": 22, "memory": 60}
2. extern_get_cpu_temperature1 {"cpu_temperature": 52}
3. extern_get_arm_clock {"arm_clock": 1400}
4. extern_get_pi_throttled_status {"throttled_status":} <br>
   ```{
   "under_voltage": Ture,
   "currently_throttled": Ture,
   "freq_capped": Ture,
   "under_voltage_occurred": Ture,
   "throttling_occurred": Ture,
   "freq_capped_occurred": Ture
   }
   ```
5. extern_get_random_color {"color": 0x1234ab}
6. extern_get_age {"age": '5d, 0h, 52m, 53s'}
7. extern_get_apache_active {"apache_active": True}

## Updated every 10s

## Updated every 30s

1. extern_fetch_weather {"temp":-3, "humidity": 98, "weather":mist}
2. extern_get_apache2metrics
   ```
   {'ServerUptime': '2 days 23 hours 7 minutes 8 seconds',
   'TotalAccesses': 664,
   'TotalkBytes': 3973,
   'BusyWorkers': 1,
   'IdleWorkers': 49,
   'Processes': 2,
   'ConnsTotal': 1,
   DurationPerReq: 2.7,
   Load1: 0.66,
   Load5: 0.64}
   ```

# 2. Effectors

1. extern_set_reboot()
2. extern_set_clock(min, max)
3. extern_enable_watchdog(apache2alive)
4. extern_content_degration(True/False)
