# Arthur

1. Metrics (**Input**):
   1. [x] Wether [D]
   2. [x] CPU/memory [D]
   3. [x] CPU temperatrue [A]
   4. [x] Current power concumption [A] (**Note that RPI has no build-in power meter, only it has a voltage comparator circuit**)
   5. [x] Apache2 metrics [D]
      1. acces number
      2. response time
      3. bandwidth
2. Effectors (**Output**):
   1. [x] Adjust cpu clock [A]
   2. [x] Content degration [D]
   3. [x] Watchdog (to reboot) [A]
   4. [ ] Apache content caching [D]
3. Adaptations:
   1. [ ] AI [D]
   2. [ ] Runtime model / Three-layer model [D]
   3. [ ] Integrate the main program [A]
4. Tests :
   1. [ ] get some data to feed the AI function.
5. Design the poster.
   1. [ ] designer the first version.

# Planning the Slides

1. Uncertainties
   1. Changes of Ambient Temperature
   2. Fluctuation of incoming Requests
   3. Different size of the hosted website
2. Models
   1. Managed system: like a boxing fighter
      1. ways to crash down RPI
         1. Heat cpu up to 80 deg
         2. Bring cpu/memory usage to 99%
3. Goals
   1. serve full content + all visitors + no downtime
   2. serve degraded content + all visitors + no downtime
   3. serve degraded content + limited visitors + no downtime
   4. X X X shortest downtime (watchdog reboot cycle time)
4. Feedback loop
5. Metrics and Effectors
   1. Utility functions
6. Implementation Framework and Technologies
7. Adaptation methods
   1. AI
8. Results and analysis
9. Future works.
