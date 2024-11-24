# How to set watchdog for Apache2 HTTP server

- For watchdog, there are hardware and software ones.
  - **Hardware**: need a lot of configuration, it also has a daemon. Check this link [raspberry pi watchdog](https://gist.github.com/lbussy/17f57adefbf744a102166d0894b54c6c) for details.
  - **Software**: Just write a python code
- For what kind of stuff to let the dog watch:
  - `apache2.pid`: The existence of the main Apache process
  - `systemctl is-active apache2`: The status of the apache2 service in Systemd

> Note: <br> 1. I decided to use **software** watchdog for this project, becasue it easy to apply to different modules.
> <br>2. I decide to monitor `systemctl is-active apache2
`, cause it is directly related to the Apache HTTP server's healthy.

## 1. Hardware or software watchdog?

## 2. Which to monitor?

**1. Mechanism of monitoring pid**

- When the Apache HTTP server starts, it writes its **Process ID (PID)** to the file `/var/run/apache2/apache2.pid`.
- The file contains the PID of the main Apache process (the parent process of all Apache worker processes).
- Verify whether Apache is running by: firstly **Reading the PID** from the file.then **periodly** **Checking** if the process with that PID exists in the `/proc` filesystem.

**2. Mechanism of using `systemctl is-active apache2`**

- `systemctl` queries the system's **service manager** (Systemd) for the status of the `apache2` service.
- The `is-active` command checks whether the service is currently running or in an active state.
- This involves verifying the service unit's status (not just the process).

- **Example**:
  - Run:`systemctl is-active apache2`
  - Example Output:`active`
  - Possible outputs:
    - `active`: The service is running.
    - `inactive`: The service is stopped.
    - `failed`: The service has crashed or failed to start.
    - `activating`: The service is starting up.

### **Comparison Table**

| Feature            | `apache2.pid` Monitoring                         | `systemctl is-active apache2`                              |
| ------------------ | ------------------------------------------------ | ---------------------------------------------------------- |
| **What It Checks** | The existence of the main Apache process         | The status of the `apache2` service in Systemd             |
| **Scope**          | Limited to the Apache process                    | Service-level monitoring (includes start/stop/fail states) |
| **Reliability**    | Can produce false positives with stale PID files | Relies on Systemd, more reliable for service status        |
| **Granularity**    | PID-specific (direct process monitoring)         | General service-level information                          |
| **Integration**    | Requires manual checks or scripts                | Fully integrated with Systemd commands                     |
| **Use Case**       | Low-level process tracking                       | High-level service health monitoring                       |

For most use cases, **`systemctl is-active apache2`** is more robust and reliable because:

- It integrates with Systemd's service management.
- It accounts for more than just process existence (e.g., failed states).
- It simplifies service control (start, stop, restart).
