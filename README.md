# Star Planner Coaching System

The Star Planner Coaching System is a comprehensive platform designed for Academic Coaching (AC), aiming to support the coaching cycle and generate useful reports for schools, teachers, and students.

## Features

- **Goal Setting & Evaluation**: Set and evaluate goals.
- **Task Setting & Evaluation**: Create and assess tasks.
- **Mini-Timetable**: Organize goals and tasks with drag & drop functionality.
- **Session Report**: Generate session reports with basic information and AC scores.
- **Final Report**: Generate comprehensive reports including Social Style, Academic Coaching Focus, Skills & Competencies Model, and more.

## Technology Stack & Architecture

- **Frontend**: React.js
- **Backend**: Django.py
- **Database**: MySQL
- **Deployment**: Azure Web Services

The system follows a client-server architecture with a RESTful API. Frontend communicates with the backend via HTTP requests, and the backend interacts with the MySQL database.

## API Endpoints

For detailed information on available endpoints and how to interact with the API, refer to the [API Documentation](#api-documentation).

## Frontend Folder 

For detailed information on the frontend folder structure and how to navigate the codebase, refer to the [Frontend Folder Structure](#frontend-folder-structure).

## Usage

1. **Installation**: Follow the instructions in the [Installation](#installation) section to set up the backend and frontend locally.
2. **Accessing the Application**: After installation, access the application at `http://localhost:3000`. Sign in with your credentials to start using the system.

## Installation

### Backend (Django)

1. Install Python and pip.
2. Navigate to the `/star-planner-api` directory.
3. Run `pip install -r requirements.txt` to install dependencies.
4. Set up environment variables as needed.
5. Run `python manage.py runserver` to start the local backend server.

### Frontend (React)

1. Install Node.js and npm.
2. Navigate to the `/star-planner-fe/frontend` directory.
3. Run `npm install` to install dependencies.
4. Run `npm start` to start the local frontend server.
# Make sure the API_URL is set to the correct backend URL in the `API.tsx` file.

## Version

- **Backend (Django)**: v4.1
- **Frontend (React)**: v18.2.0

## License

This project is proprietary and owned by Star Planner. Unauthorized use, reproduction, or distribution is strictly prohibited.

## API Documentation

### Student Dashboard Endpoints

1. **Get Student Dashboard**
   - **URL**: `/api/student_dashboard_api/`
   - **Method**: POST
   - **Description**: Retrieves the student's dashboard, including goals, tasks, and subjects.
   - **Permissions**: Authenticated users only
   - **Request Body**: None
   - **Response**: Returns goals, tasks, and subjects associated with the student. HTTP status 200 if successful.

2. **Add Goal**
   - **URL**: `/api/add_goal/`
   - **Method**: POST
   - **Description**: Adds a new goal for the student.
   - **Permissions**: Authenticated users only
   - **Request Body**: Details of the goal to be added
   - **Response**: HTTP status 201 if successful.

3. **Evaluate Goal**
   - **URL**: `/api/evaluate_goal/`
   - **Method**: POST
   - **Description**: Evaluates a goal and updates its status.
   - **Permissions**: Authenticated users only
   - **Request Body**: Evaluation details including progress, effort, etc.
   - **Response**: HTTP status 200 if successful.

4. **Add Task**
   - **URL**: `/api/add_task/`
   - **Method**: POST
   - **Description**: Adds a new task for the student.
   - **Permissions**: Authenticated users only
   - **Request Body**: Details of the task to be added
   - **Response**: HTTP status 201 if successful.

5. **Evaluate Task**
   - **URL**: `/api/evaluate_task/`
   - **Method**: POST
   - **Description**: Evaluates a task and updates its details.
   - **Permissions**: Authenticated users only
   - **Request Body**: Evaluation details including effort, effectiveness, etc.
   - **Response**: HTTP status 200 if successful.

6. **Get Calendar Data**
   - **URL**: `/api/get_calendar_data/`
   - **Method**: POST
   - **Description**: Retrieves calendar data for the student's dashboard.
   - **Permissions**: Authenticated users only
   - **Request Body**: None
   - **Response**: Calendar data for the student.

7. **Save Calendar Data**
   - **URL**: `/api/save_calendar_data/`
   - **Method**: POST
   - **Description**: Saves calendar data for the student's dashboard.
   - **Permissions**: Authenticated users only
   - **Request Body**: Data to be saved
   - **Response**: HTTP status 201 if successful.

### Session Report Endpoints

8. **Get Session Reports**
   - **URL**: `/api/get_session_reports/`
   - **Method**: POST
   - **Description**: Retrieves session report headers (date and section) for a student.
   - **Permissions**: Authenticated users only
   - **Request Body**: Student ID
   - **Response**: List of session report headers.

9. **Get Session Report**
   - **URL**: `/api/get_session_report/`
   - **Method**: POST
   - **Description**: Retrieves details of a session report.
   - **Permissions**: Authenticated users only
   - **Request Body**: Report ID
   - **Response**: Details of the session report.

10. **Add Session Report**
    - **URL**: `/api/add_session_report/`
    - **Method**: POST
    - **Description**: Adds a new session report for a student.
    - **Permissions**: Authenticated users only
    - **Request Body**: Details of the session report
    - **Response**: HTTP status 201 if successful.

### Final Report Endpoints

11. **Edit Session Report**
    - **URL**: `/api/edit_session_report/`
    - **Method**: POST
    - **Description**: Edits an existing session report.
    - **Permissions**: Authenticated users only
    - **Request Body**: Details of the session report to be edited
    - **Response**: HTTP status 200 if successful.

12. **Edit Academic Coaching Record**
    - **URL**: `/api/edit_ac_record/`
    - **Method**: POST
    - **Description**: Edits the Academic Coaching Focus/Model scores and comment in a session report.
    - **Permissions**: Authenticated users only
    - **Request Body**: Details of the academic coaching record to be edited
    - **Response**: HTTP status 200 if successful.

13. **Get Comment List**
    - **URL**: `/api/get_comment_list/`
    - **Method**: POST
    - **Description**: Retrieves a list of comments for a student in the final report.
    - **Permissions**: Authenticated users only
    - **Request Body**: Student ID
    - **Response**: List of comments.

14. **Get GPT Comment**
    - **URL**: `/api/get_gpt_comment/`
    - **Method**: POST
    - **Description**: Retrieves a generated comment for a section in the final report.
    - **Permissions**: Authenticated users only
    - **Request Body**: Details of the comment generation
    - **Response**: Generated comment.

15. **Get Final Report**
    - **URL**: `/api/get_final_report/`
    - **Method**: POST
    - **Description**: Retrieves the final report of a student.
    - **Permissions**: Authenticated users only
    - **Request Body**: Student ID, Coach ID
    - **Response**: Final report data.

16. **Edit Final Report**
    - **URL**: `/api/edit_final_report/`
    - **Method**: POST
    - **Description**: Edits a part (Social Style/Academic Coaching Focus/ Skills & Competencies Model) of the final report.
    - **Permissions**: Authenticated users only
    - **Request Body**: Details of the report to be edited
    - **Response**: HTTP status 200 if successful.

17. **Get Subject Comments**
    - **URL**: `/api/get_subject_comments/`
    - **Method**: POST
    - **Description**: Retrieves the list of subject comments in the final report.
    - **Permissions**: Authenticated users only
    - **Request Body**: Student ID
    - **Response**: List of subject comments.

18. **Add Subject Comment**
    - **URL**: `/api/add_subject_comment/`
    - **Method**: POST
    - **Description**: Adds a subject comment to the final report.
    - **Permissions**: Authenticated users only
    - **Request Body**: Details of the comment to be added
    - **Response**: HTTP status 201 if successful.

19. **Edit Subject Comment**
    - **URL**: `/api/edit_subject_comment/`
    - **Method**: POST
    - **Description**: Edits a subject comment in the final report.
    - **Permissions**: Authenticated users only
    - **Request Body**: Details of the comment to be edited
    - **Response**: HTTP status 200 if successful.

### Other Endpoints

20. **Get Student List**
    - **URL**: `/api/get_student_list/`
    - **Method**: GET
    - **Description**: Retrieves the list of students associated with the logged-in coach.
    - **Permissions**: Authenticated users only
    - **Response**: Returns a JSON object containing student profiles, role information, and coach details. HTTP status 200 if successful.

21. **Get Social Style**
    - **URL**: `/api/get_social_style/`
    - **Method**: POST
    - **Description**: Retrieves the social style records for a specific student.
    - **Permissions**: Authenticated users only
    - **Request Body**: Student ID
    - **Response**: Returns a JSON object containing social style records. HTTP status 200 if successful.

22. **Add Social Style**
    - **URL**: `/api/add_social_style/`
    - **Method**: POST
    - **Description**: Adds a new social style score record for the current student.
    - **Permissions**: Authenticated users only
    - **Request Body**: Details of the social style record
    - **Response**: HTTP status 201 if successful.

23. **Get Pre-AC Record**
    - **URL**: `/api/get_pre_ac_record/`
    - **Method**: POST
    - **Description**: Retrieves the Pre-Academic Coaching Focus/Model Scores for a student.
    - **Permissions**: Authenticated users only
    - **Response**: Returns a JSON object containing Pre-Academic Coaching Focus/Model Scores. HTTP status 200 if successful.

24. **Add/Edit Pre-AC Record**
    - **URL**: `/api/add_edit_pre_ac_record/`
    - **Method**: POST
    - **Description**: Adds or edits the Pre-Academic Coaching Focus/Model Scores for a student.
    - **Permissions**: Authenticated users only
    - **Request Body**: Details of the Pre-Academic Coaching Focus/Model Scores
    - **Response**: HTTP status 200 if successful.

25. **Handle Delete**
    - **URL**: `/api/handle_delete/`
    - **Method**: POST
    - **Description**: Deletes a goal, task, eca, qualification, or study method for a student.
    - **Permissions**: Authenticated users only
    - **Request Body**: Student ID, section (goal, task, eca, qualification, or study method), and ID of the item to delete.
    - **Response**: HTTP status 200 if successful.

26. **Signout**
    - **URL**: `/api/signout/`
    - **Method**: GET
    - **Description**: Signs out the current user.
    - **Permissions**: AllowAny
    - **Response**: HTTP status 204 if successful.

## Frontend Folder Structure

The frontend folder structure is as follows:

```bash

star-planner-fe/frontend/
|-- public/
| |-- favicon.ico
| |-- index.html
| |-- manifest.json
| |-- web.config
| |-- log.png
|-- src/
| |-- assets/
| | |-- brand_logo/
| |-- components/
| | |-- header.tsx
| | |-- (list of .tsx files storing the componential codes)
| |-- pages/
| | |-- Dashboard.tsx
| | |-- FinalReport.tsx
| | |-- PreACRecord.tsx
| | |-- SessionReport.tsx
| | |-- SignInSignUp.tsx
| | |-- SocialStyle.tsx
| |-- primitives/
| | |-- Draggable.tsx
| | |-- Droppable.tsx
| |-- styles/
| | |-- style.const.tsx
| | |-- style.css
| | |-- style.module.css
| |-- API.tsx
| |-- App.tsx
| |-- Constants.tsx
| |-- Interface.tsx
|-- package.json

```