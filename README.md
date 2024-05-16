# SMS-Automation-System
Automated SMS system: Sends updates via Infobip API based on Oracle DB changes. Easy deployment &amp; state management with JSON files.

This Python program automates the sending of SMS updates using the Infobip SMS API. It reads data from an Oracle database and sends SMS messages to recipients based on specific criteria. The program handles state management using JSON files and provides easy deployment on various servers.

## Features
- Integration with Infobip SMS API for sending SMS messages.
- Utilizes Oracle database to fetch data for SMS content.
- State management using JSON files for tracking the last execution time.
- Easily configurable and deployable on different servers.

## Installation
- Clone the repository to your local machine.
- Install the required dependencies using pip install -r requirements.txt.
- Configure the Oracle database connection details in the script.
- Set up Infobip API credentials in the script.
- Ensure the state.json file is present in the same directory as the script.

## Usage
- Run the main.py script to initiate the SMS automation process.
- Monitor the console for status updates and error messages.
- Check the log files for detailed execution logs and any potential issues.
