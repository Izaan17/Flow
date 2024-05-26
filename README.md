# Flow

## TO-DO Manager X Classwork Organizer

### Key Features:

#### 1. To-Do List Management:

- Create, edit, and delete tasks.
- Set due dates and times for tasks. 
- Categorize tasks by subject or priority.
- Mark tasks as completed.
- File Organization:

#### 2. Notifications:

- Receive reminders for upcoming tasks and due dates.

### 3. User-Friendly Interface:

- Intuitive design tailored for students.
- Easy navigation between tasks and files.

Upload and organize files related to different subjects or projects.


![An Image showcasing flows UI](flow.jpeg)

# Setup
Setting up Flow is easy! Run the following commands.
1. Clone the repo.
2. Use pip to install the packages.
```shell
pip install -r requirements.txt
```  
3. Run the file.
```shell
python main.py
```

## Importing tasks from blackboard

### Getting the iCalendar URL
To get the iCalendar URL you have to login to blackboard and follow the next steps.

![An image showcasing blackboard main menu](https://private-user-images.githubusercontent.com/93177492/284038594-048bcccf-1dd7-486b-8057-4ebdf2dc829c.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTIyODgwMjQsIm5iZiI6MTcxMjI4NzcyNCwicGF0aCI6Ii85MzE3NzQ5Mi8yODQwMzg1OTQtMDQ4YmNjY2YtMWRkNy00ODZiLTgwNTctNGViZGYyZGM4MjljLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA0MDUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNDA1VDAzMjg0NFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTRmM2ZiZjgxYWUxMzQ1MzMxYmRiNTdjMDM4NWQyNTM3MzUzZmJmYTRlNTkxOTQ3MTQ4ZTY0NmRhMTZkMzUxMGYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.D7umVJXVuFYbzPSYNagBkpFu9xHv_He3qK0xcaQc5-c)

* Click on your name (indicated by the black box)

---

![](https://private-user-images.githubusercontent.com/93177492/284038609-a617ccdf-48b6-49c4-986d-ac02e5faaf4e.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTIyODgwMjQsIm5iZiI6MTcxMjI4NzcyNCwicGF0aCI6Ii85MzE3NzQ5Mi8yODQwMzg2MDktYTYxN2NjZGYtNDhiNi00OWM0LTk4NmQtYWMwMmU1ZmFhZjRlLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA0MDUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNDA1VDAzMjg0NFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTlhNWEyMTdhMWQwZGJlMjM0NjM2NDcxNWI4ZTMwYmNjYmZhMjRjYWQ1OGYwZDRiMTAzNTY4OGY0ZTEzNjM3MjEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.TSBQI4OSGN_SepGDuNRzuPRukB8VQxK3hHYsiZBsafA)

* Next click on the calendar icon indicated by the yellow box.

---

![](https://private-user-images.githubusercontent.com/93177492/284038621-d8278f4f-41fd-4fd5-a088-a096181e3171.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MTIyODg0NjMsIm5iZiI6MTcxMjI4ODE2MywicGF0aCI6Ii85MzE3NzQ5Mi8yODQwMzg2MjEtZDgyNzhmNGYtNDFmZC00ZmQ1LWEwODgtYTA5NjE4MWUzMTcxLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDA0MDUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwNDA1VDAzMzYwM1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTllZWY5ZjM2NzUxNmQ5OWRjYzI5MzhjOGM2Y2FhMDk3MzlmOWVkM2Q2YmQ1NTZmMjZiZTUzNzBkNDdlNDAxYTImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JmFjdG9yX2lkPTAma2V5X2lkPTAmcmVwb19pZD0wIn0.xZufh-iGpcwjKU3X2OTuNNoW3T7fVT6dlyEXPa8z6Pg)

* Scroll down till you see this button.
* Click on it to get your iCalendar URL.
* Copy the url and paste it into import tasks button and click 'Save URL'.


