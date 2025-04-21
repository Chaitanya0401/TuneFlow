# TuneFlow – Cloud-Based Music Subscription Service 🎵

## Project Overview
**TuneFlow** is a cloud-hosted web application that enables users to register, log in, and subscribe to music tracks. The platform is built using **AWS Cloud Services**, **Java-based backend**, and a **modern frontend UI**, ensuring scalability, availability, and a smooth user experience.

## Features
- User registration and login system
- Search songs by title, artist, album, or year
- Subscribe and unsubscribe to music tracks
- Display subscribed songs with artist images from S3
- Backend integration with AWS services:
  - **S3** for image storage
  - **DynamoDB** for user and music data
  - **API Gateway** and **Lambda** for handling business logic

## Technologies Used
- **Frontend:** HTML, CSS, Jinja (via Flask template engine)
- **Backend:** Java (serving Flask-style logic), REST endpoints
- **Database:** AWS DynamoDB
- **Storage:** AWS S3 (for artist images)
- **Serverless:** AWS Lambda (connected to API Gateway)
- **Hosting:** AWS EC2 (Ubuntu with Apache2)
- **Session Management:** Flask with session cookies

## AWS Services and Architecture
- **EC2**: Hosts the web application and handles HTTP(S) requests on ports 80/443.
- **S3**: Stores artist images. Accessed via public URLs.
- **DynamoDB**: 
  - `login_table`: Stores user credentials.
  - `music_table`: Stores music metadata.
  - `subscriptions_table`: Tracks user subscriptions.
- **API Gateway + Lambda**: Provides serverless endpoints for subscribing, unsubscribing, and registration actions.
- **IAM Role:** `LabRole` (used for permissions by Lambda functions).
