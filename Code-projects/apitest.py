import pandas as pd
from twilio.rest import Client
from flask import Flask, request
import threading

# Twilio credentials (replace with your actual credentials)
ACCOUNT_SID = 'your_twilio_account_sid'
AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_PHONE_NUMBER = '+1234567890'  # Your Twilio phone number
YOUR_PHONE_NUMBER = '+1987654321'  # Your personal phone number to receive the summary

# Google Form or Question Template
question_body_template = "Hi {name}! 🎉 You're invited to our event. Can you attend? Reply 'Yes' or 'No'."

# Flask app for webhook
app = Flask(__name__)

# Global variable to store responses
responses = {}

# Function to read phone numbers from a CSV file
def read_csv(file_path):
    """
    Reads phone numbers and names from a CSV file.
    Assumes columns: 'Name' and 'Phone'
    """
    try:
        df = pd.read_csv(file_path)
        contacts = df[['Name', 'Phone']].dropna().to_dict('records')
        return contacts
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

# Function to send invites
def send_invites(contacts):
    """
    Sends a Yes/No question via SMS using Twilio.
    """
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for contact in contacts:
        name = contact.get("Name", "there")
        phone_number = contact["Phone"]
        message_body = question_body_template.format(name=name)

        try:
            message = client.messages.create(
                body=message_body,
                from_=TWILIO_PHONE_NUMBER,
                to=phone_number
            )
            print(f"Message sent to {phone_number}. SID: {message.sid}")
        except Exception as e:
            print(f"Failed to send message to {phone_number}: {e}")

# Route to handle incoming responses
@app.route("/sms", methods=["POST"])
def receive_sms():
    """
    Webhook to receive SMS responses from Twilio.
    """
    from_number = request.form.get("From")
    body = request.form.get("Body").strip().lower()

    if from_number:
        # Save the response
        responses[from_number] = body
        print(f"Response received from {from_number}: {body}")

    return "Response received", 200

# Function to send summary of responses to your phone number
def send_summary():
    """
    Sends a summary of Yes/No responses to your personal phone number.
    """
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    yes_count = sum(1 for response in responses.values() if response == "yes")
    no_count = sum(1 for response in responses.values() if response == "no")
    unknown_count = len(responses) - yes_count - no_count

    summary = (
        f"Summary of responses:\n"
        f"Yes: {yes_count}\n"
        f"No: {no_count}\n"
        f"Other/Invalid: {unknown_count}"
    )

    try:
        message = client.messages.create(
            body=summary,
            from_=TWILIO_PHONE_NUMBER,
            to=YOUR_PHONE_NUMBER
        )
        print(f"Summary sent to {YOUR_PHONE_NUMBER}. SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send summary: {e}")

if __name__ == "__main__":
    # Step 1: Send invites
    file_path = 'contacts.csv'  # Path to your CSV file
    contacts = read_csv(file_path)

    if contacts:
        print("Sending invites...")
        send_invites(contacts)

    # Step 2: Run the Flask app to receive responses
    print("Starting Flask server to receive SMS responses...")
    threading.Thread(target=lambda: app.run(port=5000)).start()

    # Step 3: Wait for responses and send summary manually after some time
    input("Press Enter when you're ready to send the summary...")
    send_summary()
