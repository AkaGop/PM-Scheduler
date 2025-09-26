# Professional Maintenance Scheduler for the Semiconductor Industry

This project is a professional, mobile-friendly Maintenance Scheduler web application built with Python and the Streamlit framework. It is designed for use by maintenance managers and technicians in the semiconductor industry, where data accuracy and traceability are critical.

## Features

*   **Multi-Tier User & Role Management:** Flexible user authentication with role-based permissions.
*   **Main Dashboard:** Displays key performance indicators (KPIs) and maintenance analysis charts.
*   **Interactive Maintenance Schedule:** A searchable and filterable table of all maintenance tasks.
*   **PM Task Workflow:** A complete workflow for starting, tracking, and completing maintenance tasks, including detailed downtime logging.
*   **Flexible Scheduling:** Supports default and custom maintenance frequencies.
*   **Notifications:** In-app alerts for overdue and upcoming maintenance.
*   **Data Export:** Export schedules and reports to Excel, CSV, and PDF.

## Project Structure

```
.
├── app.py                  # Main application file (handles login)
├── data/                   # Directory for Excel data files
│   ├── equipment.xlsx
│   ├── frequencies.xlsx
│   ├── maintenance_log.xlsx
│   ├── roles.xlsx
│   └── users.xlsx
├── pages/                  # Streamlit pages for different app sections
│   ├── 1_Dashboard.py
│   ├── 2_Maintenance_Schedule.py
│   └── 3_Settings.py
├── requirements.txt        # Project dependencies
└── utils/                  # Utility modules
    ├── data_loader.py
    ├── exporters.py
    └── notifications.py
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run the Application

Once the dependencies are installed, you can run the Streamlit application with the following command:

```bash
streamlit run app.py
```

The application will be accessible in your web browser at `http://localhost:8501`.

## Default Login Credentials

You can log in with the following default credentials:

| Username   | Password     | Role       |
|------------|--------------|------------|
| `admin`      | `admin_pass`   | Admin      |
| `manager`    | `manager_pass` | Manager    |
| `technician` | `tech_pass`    | Technician |