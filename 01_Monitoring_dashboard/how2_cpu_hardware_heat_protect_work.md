# Automatic CPU freq capping is a hardware function, the OS only monitors it.

## 1. Details of the Throttling Mechanism

#### Hardware-Level Functionality

- The Raspberry Pi's **SoC (System on Chip)**, such as the Broadcom BCM2837 (used in the Pi 3B+), has built-in thermal management to prevent damage due to overheating.
- If the chip's temperature exceeds a certain threshold (usually **~80°C**), the hardware triggers **thermal throttling**, reducing the CPU and GPU clock speeds to lower the temperature.
- The voltage regulator in the Pi also plays a role, reducing power delivery to components when the system enters throttling mode.

#### Operating System monitoring

While the hardware initiates the throttling process, the **operating system** monitors and logs these events. For example:

- The Linux kernel interacts with the SoC via drivers to detect and report throttling.
- Tools like `vcgencmd` and logs (e.g., `dmesg`) provide visibility into when and why throttling occurs.

#### Temperature Thresholds on the Raspberry Pi

| **Threshold**   | **Action**                                                     |
| --------------- | -------------------------------------------------------------- |
| 80°C            | Throttling begins (lower CPU and GPU clocks).                  |
| 85°C (critical) | Severe throttling and performance capping to protect hardware. |

---

## 2. How This Works

- **Hardware**:
  The thermal sensors in the SoC continuously monitor the chip's temperature.
  - If the temperature reaches the threshold, the hardware automatically adjusts the clock speeds and voltage.
- **OS**:
  The OS (Linux, in this case) works with the firmware to manage these changes:

  - Logs the event.
  - Updates the reported clock frequency and voltage.
  - Can override or adjust thresholds for more aggressive throttling (with advanced configurations).

- **What Happens When You Manually Set Frequencies?**
  - Even if you manually set the CPU clock to a high frequency using commands or scripts, the **hardware's thermal throttling mechanism** will override these settings if the system overheats.
  - The throttling is enforced by the hardware to prevent damage, so it cannot be disabled through software.

## 3. Access it with command line and python code

### **Checking Throttling Status**

check [read_power and clock](./how_get_power_and_clock.md) and [read cpu temperature](./how_read_cpu_temperature.md) to see details. Basically, the RPI's os offers command line :

1. **Check Throttling Events:**
   `vcgencmd get_throttled`,
   Example Output:
   `throttled=0x50000`

   - Interpret the Output: `0x50000` indicates that:
     - **Bit 16**: Under-voltage occurred since boot.
     - **Bit 18**: ARM frequency capping occurred since boot.

2. **Check the Current Temperature:**
   `vcgencmd measure_temp`

---
