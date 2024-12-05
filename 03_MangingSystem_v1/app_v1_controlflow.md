# the control flow

1. Initialization
   1. Reads config.json during startup
   2. Flask App Initialization [app = Flask(__name__) enables the program to handle HTTP requests.]
2.

### **Control Flow of the Python Program**

This program is a Flask web application that serves as a backend to handle requests from a frontend dashboard. The control flow can be described in the following steps:

---

### **1. Initialization**

1. **Configuration Loading**:

   - Reads `config.json` during startup using:
     ```python
     with open("config.json", "r") as f:
         config = json.load(f)
     ```
   - This configuration file contains settings, such as the city for fetching weather data.

2. **Flask App Initialization**:
   - A Flask app is created with:
     ```python
     app = Flask(__name__)
     ```
   - This enables the program to handle HTTP requests.

---

### **2. Route Definitions**

The application defines several routes that respond to HTTP requests. Here's how each route works:

#### **Route: `/` (GET)**

- **Purpose**: Serves the main dashboard HTML page.
- **Implementation**:
  ```python
  @app.route("/")
  def dashboard():
      return render_template("dashboard.html")
  ```
- **Behavior**:
  - When accessed, it renders the `dashboard.html` template.
  - This provides the structure for the webpage.

#### **Route: `/background_color` (GET)**

- **Purpose**: Returns a random color as JSON.
- **Implementation**:
  ```python
  @app.route("/background_color", methods=["GET"])
  def background_color():
      return jsonify({"color": extern_get_random_color()})
  ```
- **Behavior**:
  - Calls the `extern_get_random_color()` function to generate a random hexadecimal color.
  - Returns the color in JSON format, e.g., `{"color": "#3f8cc4"}`.

#### **Route: `/weather` (GET)**

- **Purpose**: Returns weather information as JSON.
- **Implementation**:
  ```python
  @app.route("/weather", methods=["GET"])
  def weather():
      return jsonify({"weather": extern_get_weather(config["city"])})
  ```
- **Behavior**:
  - Calls `extern_get_weather(city)` with the city from `config.json`.
  - Returns a JSON response, e.g., `{"weather": "22°C, Clear Skies"}`.

#### **Route: `/cpu_stats` (GET)**

- **Purpose**: Returns CPU and memory usage as JSON.
- **Implementation**:
  ```python
  @app.route("/cpu_stats", methods=["GET"])
  def cpu_stats():
      return jsonify(extern_get_cpu_memory_usage())
  ```
- **Behavior**:
  - Calls `extern_get_cpu_memory_usage()` to fetch the CPU usage percentage and memory usage.
  - Returns a JSON response, e.g., `{"cpu": 15.4, "memory": 62.1}`.

#### **Route: `/reboot` (POST)**

- **Purpose**: Reboots the Raspberry Pi when accessed via a POST request.
- **Implementation**:
  ```python
  @app.route("/reboot", methods=["POST"])
  def reboot():
      os.system("sudo reboot")
      return "Rebooting the Raspberry Pi...", 200
  ```
- **Behavior**:
  - Executes the `sudo reboot` command using `os.system`.
  - Responds with a success message (`200 OK`) if the command is executed.

---

### **3. External Helper Functions**

The program uses external functions to encapsulate specific functionalities:

1. **`extern_get_weather(city)`**:

   - **Purpose**: Simulates fetching weather data for a given city.
   - **Returns**: A hardcoded string, e.g., `"22°C, Clear Skies"`.

2. **`extern_get_cpu_memory_usage()`**:

   - **Purpose**: Uses the `psutil` library to get system stats.
   - **Returns**: A dictionary with:
     - `cpu`: CPU usage percentage.
     - `memory`: Memory usage percentage.

3. **`extern_get_random_color()`**:
   - **Purpose**: Generates a random color in hexadecimal format.
   - **Returns**: A string, e.g., `"#1f8acb"`.

---

### **4. Execution**

#### **Main Block**

- When the script is executed, the following block runs:
  ```python
  if __name__ == "__main__":
      app.run(host="0.0.0.0", port=5000)
  ```
- **Behavior**:
  - Starts the Flask development server on all available network interfaces (`0.0.0.0`) and port `5000`.
  - The application is now ready to handle incoming HTTP requests.

---

### **Flow of a Request**

#### Example: Request to `/weather`

1. **Browser or Client Makes Request**:

   - A GET request is sent to `http://<pi_ip>:5000/weather`.

2. **Flask Handles Request**:

   - The `/weather` route matches the request.
   - The `weather()` function is invoked.

3. **Helper Function is Called**:

   - `extern_get_weather(config["city"])` is called to fetch weather data.

4. **Response is Generated**:
   - The weather data is returned as JSON:
     ```json
     { "weather": "22°C, Clear Skies" }
     ```

---

### **Summary**

The control flow follows these key steps:

1. **Initialization**:
   - Load configuration and initialize Flask.
2. **Routing**:
   - Define routes to handle specific HTTP requests (`/`, `/weather`, `/cpu_stats`, etc.).
3. **Request Handling**:
   - When a request is received, the corresponding route is executed.
   - External helper functions provide the necessary data.
4. **Response**:
   - The server responds with HTML (for `/`) or JSON (for API endpoints like `/weather`).
5. **Actions (e.g., Reboot)**:
   - Certain routes (e.g., `/reboot`) trigger actions like rebooting the system.

Let me know if you need further clarifications! 😊
