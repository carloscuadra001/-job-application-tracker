# -job-application-tracker
 A personal web application to help track job applications during the job search process.

## Features
- Track companies 
- Record application submissions
- Manage interview schedules
- Store contact information
## Technologies
- MySQL Database
- Python with Flask
- HTML/CSS with bootstrap for the web interface

## Setup
1. Open `config.example.py` and enter your MySQL credentials (host, user, password, database name).
2. Rename the file from `config.example.py` to `config.py` and save.
3. Open MySQL and create the database:
   ```sql
   CREATE DATABASE my_job_tracker;
   ```
4. Select the database, then run the data dump files in order to create tables and load sample data:
   ```sql
   USE my_job_tracker;
   SOURCE my_job_tracker_companies.sql;
   SOURCE my_job_tracker_jobs.sql;
   SOURCE my_job_tracker_contacts.sql;
   SOURCE my_job_tracker_applications.sql;
   ```
5. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
6. Start the application:
   ```
   python run.py
   ```

##