# How this `monitoring dashboard` works

There're many ways to create information dashboard on RPI.

1. Using python with a lightweight web framework (Flask)
2. A GUI library such as PyQt or Tkinter

Here we use `Flask` reference link: [Flask official site]().

## 1. Directory structure

> The '.css' and '.html' files have to go to the designated directory, according to `Flask`'s usage.

```
dashboard/
├── app.py                 # Main Flask application
├── static/
│   └── style.css          # CSS file
├── templates/
│   └── dashboard.html     # HTML template
├── config.json            # Configuration file
└── requirements.txt       # Python dependencies

```

## Running outcome:

![alt text](./document_media/dashboard_example.png)
