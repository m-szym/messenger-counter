# Quick and dirty script for plotting Messenger messages over time
# Author: Marek Szymanski

import json
import matplotlib.pyplot as plt
import glob
import datetime
import re

if __name__ == '__main__':

    folder_path = 'F:\\your_facebook_activity\\messages\\inbox\\johnsmith_1234567890'  # <--- CHANGE THIS
    # Path to the folder containing the messages - default is something like "your_facebook_activity\messages\inbox\XYZ_number"
    # Replace \ with \\ or / (because of escape characters)
    title = re.sub(r'_[0-9]+', ' ', folder_path.split('\\')[-1])    # Title for the plots
    fig_size = (20, 12)  # Size of the plot

    messages_per_day = {}       # Dictionary to store the number of messages for each day
    messages_per_week = {}      # Dictionary to store the number of messages for each week
    messages_per_month = {}     # Dictionary to store the number of messages for each month

    # Function to update the dictionaries, don't worry about it
    def update_date(_timestamp, dictionary, time_format):
        date = datetime.datetime.fromtimestamp(_timestamp).strftime(time_format)
        if date in dictionary:
            dictionary[date] += 1
        else:
            dictionary[date] = 1

    for file in glob.glob(folder_path + '/*.json'):
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for message in data['messages']:
                if 'timestamp_ms' in message:
                    timestamp = message['timestamp_ms'] / 1000
                elif 'timestamp' in message:
                    timestamp = message['timestamp']
                else:
                    continue

                update_date(timestamp, messages_per_day, '%Y-%m-%d')
                update_date(timestamp, messages_per_week, '%Y-%W')
                update_date(timestamp, messages_per_month, '%Y-%m')

    # Plot the daily message counts
    def plot_daily():
        plt.figure(figsize=fig_size)
        x = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in messages_per_day.keys()]
        y = list(messages_per_day.values())
        plt.plot(x, y, label="Daily")
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.title("Daily messages for " + title)
        plt.show()

    # Plot the weekly message counts
    def plot_weekly():
        plt.figure(figsize=fig_size)
        x = [datetime.datetime.strptime(date + '-1', '%Y-%W-%w') for date in messages_per_week.keys()]
        y = list(messages_per_week.values())
        plt.plot(x, y, label="Weekly", marker='o', color='orange')
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.title("Weekly messages for " + title)
        plt.show()

    # Plot the monthly message counts
    def plot_monthly():
        plt.figure(figsize=fig_size)
        x = [datetime.datetime.strptime(date, '%Y-%m') for date in messages_per_month.keys()]
        y = list(messages_per_month.values())
        plt.plot(x, y, label="Monthly", marker='o', color='green')
        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.title("Monthly messages for " + title)
        plt.show()

    # All above in one plot (daily, weekly, monthly)
    # Not recommended - the different scales make it unreadable
    def plot_all():
        plt.figure(figsize=fig_size)

        x = [datetime.datetime.strptime(date, '%Y-%m-%d') for date in messages_per_day.keys()]
        y = list(messages_per_day.values())
        plt.plot(x, y, label="Daily")

        x = [datetime.datetime.strptime(date + '-1', '%Y-%W-%w') for date in messages_per_week.keys()]
        y = list(messages_per_week.values())
        plt.plot(x, y, label="Weekly")

        x = [datetime.datetime.strptime(date, '%Y-%m') for date in messages_per_month.keys()]
        y = list(messages_per_month.values())
        plt.plot(x, y, label="Monthly")

        plt.gcf().autofmt_xdate()
        plt.legend()
        plt.title("Messages for " + title)
        plt.show()

    plot_daily()    # Plot the daily messages
    plot_weekly()   # Plot the weekly messages
    plot_monthly()  # Plot the monthly messages
    # plot_all()    # Plot all in one
