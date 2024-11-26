// Function to update CPU and memory stats every second
function updateEvery1s() {
  fetch("/update_1s")
    .then((response) => response.json())
    .then((data) => {
      document.querySelector(".box.age").style.backgroundColor = data.color;
      document.getElementById("age").textContent = `${data.age}`;
      document.getElementById(
        "cpu"
      ).textContent = `${data.cpu}%, @${data.arm_clock}Mhz, total-${data.total_cpu}`;
      document.getElementById(
        "memory"
      ).textContent = `Memory: ${data.memory} %`;
      document.getElementById(
        "cputemperature"
      ).textContent = `${data.cpu_temperature} °C`;
      updateThrottledStatus(data.throttled_status);
    })
    .catch((error) => console.error("Error updating CPU stats:", error));
}

// Function to update the throttled status box
function updateThrottledStatus(data) {
  for (const [key, value] of Object.entries(data)) {
    const element = document.getElementById(key);
    if (element) {
      element.textContent = value ? "✔" : "✘"; // Display check or cross
      element.style.color = value ? "#04aa6d" : "#ff4d4d"; // Green for true, red for false
    }
  }
}

// Function to update the background color every 3 seconds
function updateEvery10s() {
  fetch("/update_10s")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById(
        "apache2-active"
      ).textContent = `${data.apache_active}`;
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

// Set up the reboot button functionality on page load
document.addEventListener("DOMContentLoaded", () => {
  setupRebootButton();
});
