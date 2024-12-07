# StartUpConnect 
## A FullStack Application to Connect Students and Startups

This repo is a semester project for Database Management. We are creating a platform that uses backend code, an API, Flask, SQL, and some front-end/UI tools to create a holistic product to help students on co-op connect with startups.

## What is StartUpConnect?
StartUpConnect helps Northeastern take its experiential learning to the next level by
connecting the relevant people to actual startups that need help. By matching students with startups based on their skills, co-op cycle, and what industries they want to enter, StartUpConnect facilitates connections and helps more students get hired at co-op experiences they want to do!

## Introduction
Team Name: StartUpConnectors
Team Members:
    Harrison Dolgoff - dolgoff.h@northeastern.edu
    Jack Harmeling - harmeling.j@northeastern.edu
    Rohan Francis - francis.r@northeastern.edu
    Nicolas Ignaszewski - ignaszewski.n@northeastern.edu

## Key Components
- Student-startup matching based on skills and availability.
- Career center analytics for placement success, industry trends, and personalized help.
- Feedback to continue to improve the experience for both students and companies.
## How to Run
### WHAT YOU NEED
- Docker
- Docker Compose
- A proper python IDE

### ACTUALLY RUNNING IT
- Clone the [repo](https://github.com/HarrisonDlgf/StartUpConnect)
- Change into the repo directory in your terminal `cd StartUpConnect`
- Set up environment variables using our template
- Run docker-compose up -d --build
- This will spin the containers for the database, Flask API, and Streamlit frontend in detached mode.
- MySQL will be available on port 3306, the Flask API on port 4000, and the Streamlit UI on port 8502.

### OPEN THE WEBSITE
- To access the Streamlit UI, open a web browser and navigate to http://localhost:8502.

## Technologies Used
- Python
- Flask
- Streamlit
- Docker
- SQL
- Mockaroo

## Current Project Components
### REST API
The backend is built using Flask and can be broken down into each user persona:

- Students: Uploading resumes, searching for internships, and co-op updates.
- Startups: Posting job opportunities, accepting and receiving candidate applications, and posting feedback for co-ops.
- Northeastern Career Center: Viewing analytics on placements and skills trends.
- Post-Grads: Platform to view full-time job opportunities and feedback on specific startups.

### Streamlit
The front end is built using Streamlit
- Provides dashboards for different types of users (personas)
- Interacts with the back-end to query real time results

## Demo Video
- Here is a walkthrough on the project [here](https://youtu.be/pifwFx2vx1k)