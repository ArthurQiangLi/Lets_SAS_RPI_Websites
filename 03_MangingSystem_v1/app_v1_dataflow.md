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

## Updated every 10s

1.extern_get_apache_active {"apache_active": True}

## Updated every 30s

1. extern_fetch_weather {"temp":-3, "humidity": 98, "weather":mist}

# 2. Effectors

1. extern_set_reboot()
