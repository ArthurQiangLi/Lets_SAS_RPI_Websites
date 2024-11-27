# To monitor apache:

'fetch_apache_metrics' method scrapes the apache metrics

Apache already serves the localhost/server-status so I don't think there was anything extra happening here

## Example data

```
localhost
ServerVersion: Apache/2.4.62 (Raspbian)
ServerMPM: event
Server Built: 2024-10-04T15:21:08
CurrentTime: Tuesday, 26-Nov-2024 18:29:51 CST
RestartTime: Saturday, 23-Nov-2024 19:22:42 CST
ParentServerConfigGeneration: 4
ParentServerMPMGeneration: 3
ServerUptimeSeconds: 256028
ServerUptime: 2 days 23 hours 7 minutes 8 seconds
Load1: 0.39
Load5: 0.48
Load15: 0.50
Total Accesses: 664
Total kBytes: 3973
Total Duration: 1372
CPUUser: 10.35
CPUSystem: 16.46
CPUChildrenUser: .82
CPUChildrenSystem: .67
CPULoad: .0110535
Uptime: 256028
ReqPerSec: .00259347
BytesPerSec: 15.8903
BytesPerReq: 6127.04
DurationPerReq: 2.06627
BusyWorkers: 1
GracefulWorkers: 0
IdleWorkers: 49
Processes: 2
Stopping: 0
ConnsTotal: 1
ConnsAsyncWriting: 0
ConnsAsyncKeepAlive: 1
ConnsAsyncClosing: 0
Scoreboard: _W________________________________________________....................................................................................................
```

## Explained

Here’s a detailed table explaining each item from the Apache status page based on your example:

| **Item**                         | **Description**                                                                                                       |
| -------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **localhost**                    | The hostname or IP address of the server. In this case, the server is running locally on `localhost`.                 |
| **ServerVersion**                | The version of Apache currently running, including any modules or build details. Example: `Apache/2.4.62`.            |
| **ServerMPM**                    | The Multi-Processing Module (MPM) used by Apache. Example: `event`, which handles concurrent connections efficiently. |
| **Server Built**                 | The date and time when the Apache server was built or compiled.                                                       |
| **CurrentTime**                  | The current system time on the server, including the timezone.                                                        |
| **RestartTime**                  | The last time the Apache server was restarted.                                                                        |
| **ParentServerConfigGeneration** | The number of times the server configuration has been changed (triggering restarts).                                  |
| **ParentServerMPMGeneration**    | The generation of the Multi-Processing Module (MPM) currently in use.                                                 |
| **ServerUptimeSeconds**          | Total uptime of the server in seconds since the last restart. Example: `256028` seconds.                              |
| **ServerUptime**                 | Human-readable uptime of the server, expressed as days, hours, minutes, and seconds.                                  |
| **Load1, Load5, Load15**         | System load averages over the past 1, 5, and 15 minutes. Indicates how busy the system is.                            |
| **Total Accesses**               | Total number of HTTP requests served by Apache since the server was started.                                          |
| **Total kBytes**                 | Total amount of data served by the server in kilobytes since it was started.                                          |
| **Total Duration**               | Total time (in milliseconds) spent processing all requests since the server started.                                  |
| **CPUUser**                      | Total CPU time (in seconds) spent in user space by Apache processes.                                                  |
| **CPUSystem**                    | Total CPU time (in seconds) spent in kernel (system) space by Apache processes.                                       |
| **CPUChildrenUser**              | Total CPU time (in seconds) spent in user space by child processes spawned by Apache.                                 |
| **CPUChildrenSystem**            | Total CPU time (in seconds) spent in kernel (system) space by child processes spawned by Apache.                      |
| **CPULoad**                      | Percentage of total CPU used by Apache, calculated over its uptime.                                                   |
| **Uptime**                       | Total uptime of the server in seconds (same as `ServerUptimeSeconds`).                                                |
| **ReqPerSec**                    | Average number of HTTP requests handled per second (`Total Accesses / Uptime`).                                       |
| **BytesPerSec**                  | Average amount of data (in bytes) served per second (`(Total kBytes * 1024) / Uptime`).                               |
| **BytesPerReq**                  | Average amount of data (in bytes) served per request (`BytesPerSec / ReqPerSec`).                                     |
| **DurationPerReq**               | Average time (in milliseconds) to handle a single request (`Total Duration / Total Accesses`).                        |
| **BusyWorkers**                  | The number of Apache worker threads or processes currently handling requests.                                         |
| **GracefulWorkers**              | The number of workers currently in the process of gracefully stopping.                                                |
| **IdleWorkers**                  | The number of idle worker threads or processes ready to handle new requests.                                          |
| **Processes**                    | Total number of Apache processes currently running.                                                                   |
| **Stopping**                     | Number of worker threads or processes that are stopping.                                                              |
| **ConnsTotal**                   | Total number of active connections to the server.                                                                     |
| **ConnsAsyncWriting**            | Number of asynchronous connections currently writing data.                                                            |
| **ConnsAsyncKeepAlive**          | Number of asynchronous connections currently in a keep-alive state.                                                   |
| **ConnsAsyncClosing**            | Number of asynchronous connections currently closing.                                                                 |
| **Scoreboard**                   | A visual representation of the status of each worker thread/process. Characters indicate:                             |
|                                  | `_`: Idle (waiting for a request).                                                                                    |
|                                  | `W`: Sending a response.                                                                                              |
|                                  | `R`: Reading a request.                                                                                               |
|                                  | `K`: Keep-alive (waiting for another request on the same connection).                                                 |
|                                  | `C`: Closing a connection.                                                                                            |
|                                  | `.`, `S`, `L`, etc.: Other states such as logging, starting, gracefully finishing, or cleanup.                        |

---
