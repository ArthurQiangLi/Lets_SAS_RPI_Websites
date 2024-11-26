// Function to update CPU and memory stats every second
function updateEvery1s() {
  fetch("/update_1s")
    .then((response) => response.json())
    .then((data) => {
      document.querySelector(".box.age").style.backgroundColor = data.color;
      document.getElementById("age").textContent = `${data.age}`;
      document.getElementById("cpu").textContent = `${data.cpu
        .toFixed(1)
        .padStart(4, "0")}%, @${data.arm_clock
        .toString()
        .padStart(4, "0")}Mhz, Total:${data.total_cpu
        .toString()
        .padStart(4, "0")}Mhz`;
      document.getElementById(
        "memory"
      ).textContent = `Memory: ${data.memory.toFixed(1)} %`;
      document.getElementById(
        "cputemperature"
      ).textContent = `${data.cpu_temperature} °C`;
      document.getElementById("watchdog_status").textContent = data.watchdog
        ? "Enabled"
        : "Disabled";
      updateThrottledStatus(data.throttled_status);
    })
    .catch((error) => console.error("Error updating CPU stats:", error));
}

// Function to update the throttled status box
function updateThrottledStatus(data) {
  for (const [key, value] of Object.entries(data)) {
    const element = document.getElementById(key);
    if (element) {
      if (value) {
        element.classList.add("active"); // Add red tick and red text for warnings
      } else {
        element.classList.remove("active"); // Default style for inactive warnings
      }
    }
  }
}

// Function to update the background color every 3 seconds
function updateEvery10s() {
  fetch("/update_10s")
    .then((response) => response.json())
    .then((data) => {
      const apache2ActiveElement = document.getElementById("apache2-active");
      if (data.apache_active) {
        apache2ActiveElement.textContent = "✔";
        apache2ActiveElement.style.color = "#04aa6d"; // Green for activ
      } else {
        apache2ActiveElement.textContent = "✘";
        apache2ActiveElement.style.color = "#ff4d4d"; // Red for inactive
      }
    })
    .catch((error) => console.error("Error updating background color:", error));
}

// Function to update weather data every 30 seconds
function updateEvery30s() {
  fetch("/update_30s")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById(
        "weather"
      ).textContent = `${data.temp} °C, ${data.humidity} % Humidity, ${data.weather}`;
    })
    .catch((error) => console.error("Error updating weather:", error));
}

// Set intervals for updates
setInterval(updateEvery10s, 10000); // Every 3 seconds
setInterval(updateEvery30s, 30000); // Every 30 seconds
setInterval(updateEvery1s, 1000); // Every 1 second

// Function to handle the reboot button click
function setupRebootButton() {
  const rebootButton = document.getElementById("reboot-button");
  rebootButton.addEventListener("click", () => {
    fetch("/reboot", { method: "POST" })
      .then(() => {
        alert("Rebooting the Raspberry Pi...");
      })
      .catch((error) => {
        console.error("Error sending reboot request:", error);
        alert("Failed to reboot the Raspberry Pi. Please try again.");
      });
  });
}

function setupMinClcokButton() {
  const minButton = document.getElementById("min-clock-button");
  minButton.addEventListener("click", () => {
    fetch("/min_clock", { method: "POST" })
      .then(() => {
        alert("Setting min cpu clock...");
      })
      .catch((error) => {
        console.error("Error sending min-clock request:", error);
      });
  });
}
function setupMaxClcokButton() {
  const maxButton = document.getElementById("max-clock-button");
  maxButton.addEventListener("click", () => {
    fetch("/max_clock", { method: "POST" })
      .then(() => {
        alert("Setting max cpu clock...");
      })
      .catch((error) => {
        console.error("Error sending max-clock request:", error);
      });
  });
}

function setupOnDemandButton() {
  const autoButton = document.getElementById("auto-clock-button");
  autoButton.addEventListener("click", () => {
    fetch("/on_demand", { method: "POST" })
      .then(() => {
        alert("Setting auto ondemand cpu clock...");
      })
      .catch((error) => {
        console.error("Error sending on_demand request:", error);
      });
  });
}

function setupWatchdogButton() {
  const watchdogButton = document.getElementById("watchdog-button");
  watchdogButton.addEventListener("click", () => {
    fetch("/watchdog", { method: "POST" })
      .then(() => {
        alert("Switch watchdog...");
      })
      .catch((error) => {
        console.error("Error sending watchdog on/off request:", error);
      });
  });
}

// Set up the reboot button functionality on page load
document.addEventListener("DOMContentLoaded", () => {
  setupRebootButton();
  setupMinClcokButton();
  setupMaxClcokButton();
  setupOnDemandButton();
  setupWatchdogButton();
});
