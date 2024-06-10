# TaskPilot

## Overview

TaskPilot is a Python-based web application designed to help you manage your tasks efficiently. It leverages Flask for the backend, SQLAlchemy for database interactions, and a simple HTML/CSS front-end for user interaction. TaskPilot allows you to create and manage applications, add tasks, update task statuses, reorder tasks, and download task lists in CSV and PDF formats.

## Features

- **Create and Manage Applications:** Add and delete applications to organize your tasks.
- **Add and Update Tasks:** Add new tasks to applications, update task statuses, and edit task details.
- **Reorder Tasks:** Drag and drop to reorder tasks within an application.
- **Download Task Lists:** Export tasks as CSV or PDF using the download buttons.
- **Import Tasks:** Upload tasks from a CSV file to import tasks.

## Requirements

- Python 3.x+
- Flask
- Flask-SQLAlchemy
- pandas
- reportlab

### Option 1: Using `app.py`

1. **Clone the repository:**

    ```bash
    git clone https://github.com/jenniferchrista23/task-pilot.git
    cd task-pilot
    ```

2. **Install the required packages:**

    ```bash
    pip install flask flask_sqlalchemy sqlalchemy pandas reportlab
    (or)
    cd dist
    pip install -r requirements.txt
    ```

3. **Run the application:**

    ```bash
    python app.py
    ```

4. **Open your web browser and navigate to:**

    ```
    http://127.0.0.1:5000/
    (or)
    http://localhost:5000
    ```
### Option 2: Using the Executable

## Running TaskPilot

### Windows

1. **Clone the repository:**
   
    ```bash
    git clone https://github.com/jenniferchrista23/task-pilot.git
    cd task-pilot/dist/windows
    ```

2. **Install the required packages:**

    ```bash
    pip install flask flask_sqlalchemy sqlalchemy pandas reportlab
    
3. **Download `taskpilot.exe`** and save it to a convenient location on your computer.
  
4. **Double-click the executable** to run the application.

### Linux

1. **Clone the repository:**
   
    ```bash
    git clone https://github.com/jenniferchrista23/task-pilot.git
    cd task-pilot/dist/linux
    ```
2. **Install the required packages:**

    ```bash
    pip install flask flask_sqlalchemy sqlalchemy pandas reportlab   
3. **Download `TaskPilot`** and save it to a convenient location on your computer.
4. **Make the file executable** by running the following command in your terminal:

    ```bash
    chmod +x task-pilot/dist/linux/TaskPilot
    ```

5. **Run the application** by executing:

    ```bash
    ./task-pilot/dist/linux/TaskPilot
    ```

### macOS

1. **Clone the repository:**
   
    ```bash
    git clone https://github.com/jenniferchrista23/task-pilot.git
    cd task-pilot/dist/macos
    ```
2. **Install the required packages:**

    ```bash
    pip install flask flask_sqlalchemy sqlalchemy pandas reportlab   
3. **Download `app`** and save it to a convenient location on your computer.
4. **Make the file executable** by running the following command in your terminal:

    ```bash
    chmod +x task-pilot/dist/macos/app
    ```

5. **Run the application** by executing:

    ```bash
    ./task-pilot/dist/macos/app
    ```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the existing code style and includes relevant tests.

## Contact

If you have any questions or need further assistance, please visit my [blog](https://devops-learning-spot.blogspot.com/) and leave a message. I'll be happy to help!

---

Thank you for using TaskPilot! I hope it helps you manage your tasks more efficiently.
