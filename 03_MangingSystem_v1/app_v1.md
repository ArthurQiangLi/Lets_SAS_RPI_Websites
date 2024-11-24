## Directory Structure

```sh
project/
├── static/
│   ├── style.css       # CSS file for styling
│   ├── script.js       # JavaScript logic
├── templates/
│   ├── dashboard.html  # HTML file for the dashboard
├── app.py              # Flask backend

```

## 1. How the frontend and backend works

### Basic design

1. **The frontend .js code is in a separated file**. The HTML file includes the script with a `script` tag that references `/static/script.js`.
2. **Dynamic updates for frontend items**. It's implemented in .js file. Eg. Weather Data: Updated every 30 seconds by fetching from `/weather` router; CPU and Memory Stats: Updated every 1 second by fetching from `/cpu_stats` router; Plus the `setInterval()` functions.

### Important data flow

In this Flask-based project, there are data flows between the frontend(_dashboard.html + script.js_) and the backend (_app.py_) in a structed way.

#### step1. Initial rendering(.html + .py)

Backend is responsible for preparing and updating the data and store them in strings or dictionaries (in python data). Take `weather`(string) and `stats`(dictionary) for instance.

- the frontend .js use route(`/`) to request for a data, the Flask server hadles the request.
- the data is updated by app.py in the backend. app.py pass the values to dashboard.html template using Flask's `render_template()` function.

```py
in app.py
@app.route("/")
def dashboard():
    weather = get_weather(config["city"])  # Weather data from API
    stats = get_cpu_memory_usage()  # CPU and memory usage from psutil
    return render_template("dashboard.html", weather=weather, stats=stats)

```

Here, the current weather string (e.g., "Sunny, 22°C") is passed to the template. <br> stats: A dictionary containing CPU usage and other metrics, e.g., {"cpu": 25, "memory": 60}.

The dashboard.html file is rendered by Flask with the data inserted into placeholders using Jinja2 template synax `{{ ... }}`.

```html
<h1>Raspberry Pi Dashboard</h1>
<h2>Weather: {{ weather }}</h2>
<!-- Displays weather data -->
<h2>CPU Usage: {{ stats['cpu'] }}%</h2>
<!-- Displays CPU usage -->
```

As a result, the Flask replaces {{ weather }} and {{ stats['cpu'] }} with data Flask passed from .py program. it will display like:

```html
<h1>Raspberry Pi Dashboard</h1>
<h2>Weather: Sunny, 22°C</h2>
<h2>CPU Usage: 25%</h2>
```

#### step 2..n Constantly updating (.js + .py + .html)

After the step1, js will dynamically fetch data (new weather and cpu status for example) and insert it into the page.

**In .py **we have separate routes to **serve** data in JSON format:

```py
in app.py
@app.route("/weather", methods=["GET"])
def weather():
    return jsonify({"weather": get_weather(config["city"])})
    #returns like:  {"weather": "Sunny, 23°C"}
@app.route("/cpu_stats", methods=["GET"])
def cpu_stats():
    return jsonify(get_cpu_memory_usage())
    #returns like: {"cpu": 30, "memory": 55}
```

**In .js,** functions periodically **fetchs** new data from these endpoints(routes) and **updates the DOM** in html:

```js
function updateWeather() {
  fetch("/weather") //[1.]JavaScript sends an HTTP GET request to the /weather endpoints.
    .then((response) => response.json()) //[2.]wait the backend responds with JSON data (e.g., {"cpu": 30}).
    .then((data) => {
      //[3.] parses this data and updates the corresponding HTML elements dynamically.
      document.querySelector(
        "#weather"
      ).textContent = `Weather: ${data.weather}`;
    });
}

function updateCpuStats() {
  fetch("/cpu_stats")
    .then((response) => response.json())
    .then((data) => {
      document.querySelector("#cpu").textContent = `CPU Usage: ${data.cpu}%`;
    });
}

// Set update intervals
setInterval(updateWeather, 30000); // Update weather every 30 seconds
setInterval(updateCpuStats, 1000); // Update CPU stats every second
```

**In .html**, similar to step1, the content of the <h2> elements in dashboard.html is updated in real-time without refreshing the page.

## 9. Development log

| Version or date | Screenshots                                                                                                      |
| :-------------- | :--------------------------------------------------------------------------------------------------------------- |
| v1.0            | Design the layout of the front gui. <br> ![v1.0](./markdown_media/Screenshot%20from%202024-11-24%2010-40-25.png) |
