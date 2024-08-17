# Quick and dirty script for counting Messenger messages
# Author: Marek Szymanski

import os
import glob
import json
import re
import datetime

if __name__ == '__main__':
    inbox_path = 'F:\\your_facebook_activity\\messages\\inbox'  # <--- CHANGE THIS
    # Path to the folder containing the messages - default is something like "your_facebook_activity\messages\inbox"
    # Replace \ with \\ or / (because of escape characters)

    stats = {}
    # Dictionary to store the info for each chat
    # the format is:
    # {
    #     "name": {
    #         "messages_nr": number of messages,
    #         "participants": list of participants *
    #         "first": timestamp** of the first message,
    #         "last": timestamp of the last message
    #     }
    # }
    # * encrypted chats don't have the participants list
    # ** timestamps are Unix time in milliseconds

    for folder in os.listdir(inbox_path):
        folder_path = os.path.join(inbox_path, folder)
        messages_count = 0
        participants = []
        first = 0
        last = 0
        for file in glob.glob(folder_path + '/*.json'):
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)

                if messages_count == 0:
                    participants = data["participants"]
                    if 'timestamp_ms' in data['messages'][0]:
                        last = data['messages'][0]['timestamp_ms']
                    elif 'timestamp' in data['messages'][0]:
                        last = data['messages'][0]['timestamp'] * 1000
                    else:
                        last = 0

                messages_count += len(data['messages'])
                if 'timestamp_ms' in data['messages'][-1]:
                    first = data['messages'][-1]['timestamp_ms']
                elif 'timestamp' in data['messages'][-1]:
                    first = data['messages'][-1]['timestamp'] * 1000
                else:
                    first = 0

        chat_name = re.sub(r'_[0-9]+', ' ', folder).strip()
        stats[chat_name] = {
            "messages_nr": messages_count,
            "participants": participants,
            "first": first,
            "last": last
        }

    # Some useful filters
    # stats = {k: v for k, v in stats.items() if len(v["participants"]) <= 2}                 # No group chats
    # stats = {k: v for k, v in stats.items() if v["messages_nr"] >= 10}                      # No less than 10 messages

    # Some sorting methods
    stats_sorted = sorted(stats.items(), key=lambda x: x[0])                                # By chat name
    # stats_sorted = sorted(stats.items(), key=lambda x: x[1]['messages_nr'], reverse=True)   # By number of messages
    # stats_sorted = sorted(stats.items(), key=lambda x: len(x[1]['participants']),
    #                       reverse=True)                                                     # By nr of participants
    # stats_sorted = sorted(stats.items(), key=lambda x: x[1]['first'],
    #                       reverse=True)                                                     # By first timestamp
    # stats_sorted = sorted(stats.items(), key=lambda x: x[1]['last'],
    #                       reverse=True)                                                     # By last timestamp
    # stats_sorted = sorted(stats.items(), key=lambda x: x[1]['last'] - x[1]['first'],
    #                       reverse=True)                                                     # By chat duration

    # Example output, customize as needed
    i = 0
    print("{:<4}  {:<25}  {:<6}  {:<25}  {:<10}  {:<10}".format('#', "Chat name", "Count", "Timespan", "Avg", "Type"))
    print("-" * 88)
    for chat_name, info in stats_sorted:
        name = f'{chat_name if len(chat_name) <= 20 else chat_name[:20] + "..."}'
        basic_info = f'{info["messages_nr"]}'
        timespan = f'({datetime.datetime.fromtimestamp(info["first"] / 1000).strftime("%Y-%m-%d")} - ' \
                   f'{datetime.datetime.fromtimestamp(info["last"] / 1000).strftime("%Y-%m-%d")})'
        average = f'{info["messages_nr"] / ((info["last"] - info["first"]) // 86400000):.2f} /day' \
            if (info["last"] - info["first"]) // 86400000 else ''
        group = 'Group' if len(info["participants"]) > 2 else 'Private'
        print("{:<4}  {:<25}  {:<6}  {:<15}  {:<10}  {:<10}".format(i, name, basic_info, timespan, average, group))
        i += 1
