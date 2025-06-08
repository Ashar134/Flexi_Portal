# Flexi – Unified Academic Web App

Flexi is a Django-based web app combining features from Google Classroom and Flex. It simplifies academic tasks for students, teachers, and admins by integrating class materials, attendance, grading, schedules, and communication into a single platform.

## Features

### Teachers
- Mark attendance and grades
- Upload study materials
- View assigned students

### Students
- View timetables and attendance
- Check uploaded materials
- Join discussion forums
- Add tasks in to-do vault
- View marks
- Browse teacher list (via web scraping)

### Admins
- Manage users
- Assign students to teachers
- Manage timetables

## Tech Stack
- HTML, CSS
- Django (Python)
- BeautifulSoup (Web scraping)
- Regex (Validation)

## Setup Instructions
```bash
git clone https://github.com/Ashar134/Flexi_Portal.git
cd Flexi_Portal
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
