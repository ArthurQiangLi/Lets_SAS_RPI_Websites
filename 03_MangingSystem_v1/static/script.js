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
      updateWatchdogStatus(data);
      updateThrottledStatus(data.throttled_status);
      update_apache_active(data);
    })
    .catch((error) => console.error("Error updating CPU stats:", error));
}
// Function to update watchdog status
function updateWatchdogStatus(data) {
  const ele = document.getElementById("watchdog_status");
  if (data.watchdog) {
    ele.textContent = "Enabled ✔";
    ele.style.color = "#04aa6d"; // Green for activ
  } else {
    ele.textContent = "Disabled ✘";
    ele.style.color = "#ff4d4d"; // Red for inactive
  }
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
      document.getElementById(
        "weather"
      ).textContent = `${data.temp} °C, ${data.humidity} % Humidity, ${data.weather}`;
      populateApacheMetrics(data.apache2metrics);
    })
    .catch((error) => console.error("Error updating background color:", error));
}

function update_apache_active(data) {
  const apache2ActiveElement = document.getElementById("apache2-active");
  if (data.apache_active) {
    apache2ActiveElement.textContent = "Active ✔";
    apache2ActiveElement.style.color = "#04aa6d"; // Green for activ
  } else {
    apache2ActiveElement.textContent = "Stopped ✘";
    apache2ActiveElement.style.color = "#ff4d4d"; // Red for inactive
  }
}

// Function to update weather data every 30 seconds
function updateEvery30s() {
  fetch("/update_30s")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById(
        "weather"
      ).textContent = `${data.temp} °C, ${data.humidity} % Humidity, ${data.weather}`;
      populateApacheMetrics(data.apache2metrics);
    })
    .catch((error) => console.error("Error updating weather:", error));
}

function populateApacheMetrics(metrics) {
  const metricsList = document.getElementById("apache-metrics"); // Target the <ul> element
  metricsList.innerHTML = ""; // Clear existing content in case it's being refreshed
  // Populate the <ul> with key-value pairs from the metrics object
  for (const [key, value] of Object.entries(metrics)) {
    const listItem = document.createElement("li");
    listItem.textContent = `${key}: ${value}`; // Format as "key: value"
    metricsList.appendChild(listItem); // Add the list item to the <ul>
  }
}

// Set intervals for updates
setInterval(updateEvery1s, 1000); // Every 1 second
setInterval(updateEvery10s, 10000); // Every 10 seconds
// setInterval(updateEvery30s, 30000); // Every 30 seconds

// Generic function to set up a button with an event listener
function setupButton(buttonId, endpoint, successMessage, errorMessage) {
  const button = document.getElementById(buttonId);
  if (button) {
    button.addEventListener("click", () => {
      fetch(endpoint, { method: "POST" })
        .then(() => {
          alert(successMessage);
        })
        .catch((error) => {
          console.error(`Error sending request to ${endpoint}:`, error);
          alert(errorMessage || "An error occurred. Please try again.");
        });
    });
  } else {
    console.warn(`Button with ID '${buttonId}' not found.`);
  }
}

// Set up buttons on page load
document.addEventListener("DOMContentLoaded", () => {
  setupButton(
    "reboot-button",
    "/reboot",
    "Rebooting the Raspberry Pi...",
    "Failed to reboot the Raspberry Pi. Please try again."
  );

  setupButton(
    "min-clock-button",
    "/min_clock",
    "Setting min CPU clock...",
    "Failed to set min CPU clock."
  );

  setupButton(
    "max-clock-button",
    "/max_clock",
    "Setting max CPU clock...",
    "Failed to set max CPU clock."
  );

  setupButton(
    "auto-clock-button",
    "/on_demand",
    "Setting auto on-demand CPU clock...",
    "Failed to set auto on-demand CPU clock."
  );

  setupButton(
    "watchdog-button",
    "/watchdog",
    "Switching watchdog...",
    "Failed to switch watchdog on/off."
  );
});
