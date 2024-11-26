// Function to update the background color every 3 seconds
function updateBackgroundColor() {
  fetch("/background_color")
    .then((response) => response.json())
    .then((data) => {
      document.querySelector(".box.age").style.backgroundColor = data.color;
    })
    .catch((error) => console.error("Error updating background color:", error));
}

// Function to update weather data every 30 seconds
function updateWeather() {
  fetch("/weather")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById(
        "weather"
      ).textContent = `Weather: ${data.weather}`;
    })
    .catch((error) => console.error("Error updating weather:", error));
}

// Function to update CPU and memory stats every second
function updateCpuStats() {
  fetch("/cpu_stats")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("cpu").textContent = `CPU Usage: ${data.cpu}%`;
      document.getElementById(
        "memory"
      ).textContent = `Memory Usage: ${data.memory}%`;
      document.getElementById(
        "cputemperature"
      ).textContent = `${data.cpu_temperature}°C`;
    })
    .catch((error) => console.error("Error updating CPU stats:", error));
}

// Set intervals for updates
setInterval(updateBackgroundColor, 1000); // Every 3 seconds
setInterval(updateWeather, 30000); // Every 30 seconds
setInterval(updateCpuStats, 1000); // Every 1 second
S;

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
