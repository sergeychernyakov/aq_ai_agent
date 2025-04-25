# blank_python_project

## Overview

## Features

## Setup

### 1. Clone the Repository

Begin by cloning the repository to your local machine:

```bash
git clone https://github.com/sergeychernyakov/blank_python_project.git
cd blank_python_project
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv .venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment before installing dependencies.

- **Linux/MacOS:**

    ```bash
    source .venv/bin/activate
    ```

- **Windows:**

    ```bash
    .venv\Scripts\activate
    ```

### 4. Install Dependencies

Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

The application relies on environment variables for configuration. Create a `.env` file in the root directory with the following content:

```env
APP_ENV=development
```

- Ensure that the `.env` file is **not** committed to version control to protect sensitive information.

### 6. Export Installed Packages (Optional)

If you add new dependencies during development, update the `requirements.txt` file:

```bash
pip freeze > requirements.txt
```

## Usage

### Script Workflow

### Example Command

## Project Structure

```
.
├── README.md
├──media
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── config
│   │   ├── __init__.py
│   │   └── settings.py
├── tests
└── tmp
    └── logs
```

### Directory Breakdown

- **`media/`**: Contains input and output Excel files, and other media assets.
- **`src/`**: Source code organized into subdirectories:
- **`tests/`**: Unit tests for various components.
- **`tmp/`**: Temporary files and logs.

## Logging

Logs are stored in the `tmp/logs/` directory. Each module logs to its respective file.
Logging is configured to output both to the console and log files with varying levels based on the environment.

## Testing

Unit tests are located in the `tests/` directory. To run the tests, execute:

```bash
pytest
```
