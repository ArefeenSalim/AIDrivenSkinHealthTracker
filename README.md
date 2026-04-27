# SkinTrack – AI-Driven Skin Health Tracker


# Project Overview

## SkinTrack is an AI-driven mobile health application designed to help users monitor daily lifestyle habits and identify possible triggers for skin flare-ups such as:
## Acne
## Eczema
## Psoriasis
## Rosacea

## The application allows users to log daily information such as:
## Sleep hours
## Stress level
## Water intake
## Diet quality
## Symptom severity
## Skin condition type

## The system also automatically retrieves:
## Temperature
## Humidity
## Weather conditions
## User location

## Using this combined data, SkinTrack predicts the likelihood of a skin flare-up and classifies the risk as:
## Low Risk
## Medium Risk
## High Risk

## The goal is not medical diagnosis, but proactive awareness and personalised health monitoring.


# Technologies Used

## Frontend
## - React Native
## - Expo

## Backend
## - Firebase (Authentication + Firestore)
## - Python (Prediction Logic)
## - Flask (Prediction API)

## Environmental Data 
## - OpenWeather API

## Machine Learning Logic
## - Rule-Based Prediction + AI Logic

## Sythetic Dataset
## Real medical datasets involving eczema, acne, psoriasis and rosacea flare-up history are difficult to access because of GDPR restrictions, patient privacy laws, NHS access limitations, ethical approval requirements.
## Because of this, a ynthetic dataset was created to simulate realistic user behaviour and skin health patterns.


# Installation 

## Step 1 - Install Visual Studio Code
## https://code.visualstudio.com/ 

## Step 2 - Install Node.js
## Download and install the LTS version from: https://nodejs.org/en
## Node.js is required because the project uses React Native, Expo, Firebase and npm packages
## After installation, verify it works by running these commands in the terminal: node -v and npm -v

## Step 3: Install Expo Go on your mobile devices
## Android: Google Play store
## iPhone: Apple App Store
## This is required to test the mobile application directly on your device using QR code scanning.

## Step 4: Clone the Project Repository from Github
## Open terminal inside VS Code and run:
## git clone https://github.com/ArefeenSalim/AIDrivenSkinHealthTracker.git

## Step 5: Install Project Dependencies 
## Run ' npm install ' in VS Code terminal 
## This installs all required project packages including React Native, Expo, Firebase, React Navigation, react-native-chart-kit, react-native-svg

## Step 6: Setup Python Virtual Environment
## This project uses a Flask backend for prediction logic.Before running the backend, a Python virtual environment must be created.
## Step 6.1: Download and install Python 3 from: https://www.python.org/downloads/ , after installation, verify if it works by putting ' python3 --version ' in the VS code terminal. This shoudl return a Python version number.
## Step 6.2: Create the Virtual Environment
## In the terminal run ' cd backend ' to get inside the backend folder. Then run ' python3 -m venv venv ', this creates a local virtual environment called venv
## Step 6.3: Activate the Virtual Environment in the terminal 
## - for Mac/Linux: source venv/bin/activate
## - for Windows: venv\Scripts\activate
## once activated, your terminal will show (venv) at the beginning of the line.
## Step 6.4: Install backend dependencies by running ' pip install flask pandas scikit-learn numpy ' 
## these packages are required for Flask API, Prediction Logic, Data Processing, Model Handling

## Step 7: Running the Project
## Step 7.1: in a new terminal first run the Flask app using the following commands:
## - cd backend
## - source venv/bin/activate
## - python3 app.py
## Step 7.2: in another new terminal run Expo using the following commands:
## - cd mobile
## - npx expo start -c

## Step 8: Scan the QR Code.
## note that the device the project is being run and the mobile device that is used for scanning are connected to the same wifi