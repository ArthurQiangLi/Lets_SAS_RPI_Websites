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

1. **The frontend .js code is in a separated file**. The HTML file includes the script with a `script` tag that references `/static/script.js`.
2. **Dynamic updates for frontend items**. It's implemented in .js file. Eg. Weather Data: Updated every 30 seconds by fetching from `/weather` router; CPU and Memory Stats: Updated every 1 second by fetching from `/cpu_stats` router; Plus the `setInterval()` functions.

## 9. Development log

| Version or date | Screenshots                                                                                                      |
| :-------------- | :--------------------------------------------------------------------------------------------------------------- |
| v1.0            | Design the layout of the front gui. <br> ![v1.0](./markdown_media/Screenshot%20from%202024-11-24%2010-40-25.png) |
