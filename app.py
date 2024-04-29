from flask import Flask, render_template, request, redirect, url_for, jsonify
import datetime


app = Flask(__name__)

import datetime

# Define the start and end dates of the month
start_date = datetime.date(2024, 5, 1)
end_date = datetime.date(2024, 5, 31)

# Initialize the available times dictionary
available_times = {}

# Populate the available times for each day of the month
current_date = start_date
while current_date <= end_date:
    # Define available times for each day
    if current_date.weekday() != 4 or current_date.weekday():  # Consider only weekdays (Monday to Friday)
        available_times[current_date.strftime('%Y-%m-%d')] = [
            "08:30 AM", "09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM", "11:00 AM",
            "11:30 AM", "12:00 PM", "12:30 PM", "01:00 PM", "01:30 PM", "02:00 PM",
            "02:30 PM", "03:00 PM", "03:30 PM", "04:00 PM", "04:30 PM", "05:00 PM",
            "05:30 PM", "06:00 PM", "06:30 PM", "07:00 PM", "07:30 PM", "08:00 PM",
            "08:30 PM"
        ]
    else:
        # Weekend, no appointments
        available_times[current_date.strftime('%Y-%m-%d')] = []

    # Move to the next day
    current_date += datetime.timedelta(days=1)


@app.route('/')
def index():
    available_dates = [date for date, times in available_times.items() if times]
    return render_template('index.html', available_dates=available_dates)

@app.route('/book', methods=['POST'])
def book_appointment():
    selected_date = request.form['date']
    selected_time = request.form['time']
    if selected_date in available_times and selected_time in available_times[selected_date]:
        # Appointment available, remove the selected time from available times for the selected date
        available_times[selected_date].remove(selected_time)
        
        # Check if no more available times for the selected date, remove the date from available_dates
        if not available_times[selected_date]:
            del available_times[selected_date]

        # Send confirmation email or perform other actions
        #send_confirmation_email(selected_date, selected_time)
        
        return render_template('confirmation.html', date=selected_date, time=selected_time)
    else:
        return "Sorry, the selected time is not available."

@app.route('/get_times', methods=['POST'])
def get_available_times():
    selected_date = request.form['date']
    if selected_date in available_times:
        times = available_times[selected_date]
        return jsonify({'times': times})
    else:
        return jsonify({'times': []})

if __name__ == '__main__':
    app.run(debug=True)