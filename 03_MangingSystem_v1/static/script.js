document.addEventListener("DOMContentLoaded", () => {
  const fetchData = () => {
    fetch("/data")
      .then((response) => response.json())
      .then((data) => {
        document.getElementById(
          "weather"
        ).textContent = `Weather: ${data.weather}`;
        document.getElementById(
          "cpu"
        ).textContent = `CPU Usage: ${data.cpu_percent}%`;
        document.getElementById(
          "memory"
        ).textContent = `Memory Usage: ${data.memory_used} MB / ${data.memory_total} MB`;
        document.getElementById("age").textContent = `Age: ${data.age} years`;
        document.getElementById(
          "inner-temp"
        ).textContent = `Inner Temp: ${data.inner_temp}`;
      });
  };

  // Random background color change
  setInterval(() => {
    document.body.style.backgroundColor = `rgb(${Math.random() * 255}, ${
      Math.random() * 255
    }, ${Math.random() * 255})`;
  }, 3000);

  // Fetch data every 5 seconds
  fetchData();
  setInterval(fetchData, 5000);

  // Reboot button
  document.getElementById("reboot-button").addEventListener("click", () => {
    fetch("/reboot", { method: "POST" })
      .then(() => alert("Rebooting..."))
      .catch((err) => alert("Error: " + err));
  });
});

//////////////
// Function to update the background color every 3 seconds
function updateBackgroundColor() {
  fetch("/background_color")
    .then((response) => response.json())
    .then((data) => {
      document.querySelector("h1").style.color = data.color;
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
    })
    .catch((error) => console.error("Error updating CPU stats:", error));
}

// Set intervals for updates
setInterval(updateBackgroundColor, 3000); // Every 3 seconds
setInterval(updateWeather, 30000); // Every 30 seconds
setInterval(updateCpuStats, 1000); // Every 1 second
