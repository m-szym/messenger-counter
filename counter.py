# Quick and dirty script for counting Messenger messages
# Author: Marek Szymanski

import os
import glob
import json
import re
import datetime


# Some pre-made sorting methods
# Method can be 'name', 'messages_nr', 'participants_nr', 'first', 'last', 'duration'
def sort_stats(_stats, method):
    if method == 'name':
        _sorted_stats = sorted(_stats.items(), key=lambda x: x[0])
    elif method == 'messages_nr':
        _sorted_stats = sorted(_stats.items(), key=lambda x: x[1]['messages_nr'], reverse=True)
    elif method == 'participants_nr':
        _sorted_stats = sorted(_stats.items(), key=lambda x: len(x[1]['participants']), reverse=True)
    elif method == 'first':
        _sorted_stats = sorted(_stats.items(), key=lambda x: x[1]['first'], reverse=True)
    elif method == 'last':
        _sorted_stats = sorted(_stats.items(), key=lambda x: x[1]['last'], reverse=True)
    elif method == 'duration':
        _sorted_stats = sorted(_stats.items(), key=lambda x: x[1]['last'] - x[1]['first'], reverse=True)
    else:
        print('Invalid method')
        return _stats
    return _sorted_stats


if __name__ == '__main__':
    inbox_path = 'F:\\your_facebook_activity\\messages\\inbox'  # <--- CHANGE THIS
    # Path to the folder containing the messages - default is something like "your_facebook_activity\messages\inbox"
    # Replace \ with \\ or / (because of escape characters)

    stats = {}
    # Dictionary to store the info for each conversation
    # the format is:
    # {
    #     "name": {
    #         "messages_nr": number of messages,
    #         "participants": list of participants *
    #         "first": timestamp** of the first message,
    #         "last": timestamp of the last message
    #     }
    # }
    # * encrypted conversations don't have the participants list
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

        conv_name = re.sub(r'_[0-9]+', ' ', folder).strip()
        stats[conv_name] = {
            "messages_nr": messages_count,
            "participants": participants,
            "first": first,
            "last": last
        }

    # Some useful filters
    # stats = {k: v for k, v in stats.items() if len(v["participants"]) <= 2}   # No group chats
    # stats = {k: v for k, v in stats.items() if v["messages_nr"] >= 10}        # No less than 10 messages

    # Sort the stats by the number of messages
    stats_sorted = sort_stats(stats, 'messages_nr')

    # Example output, customize as needed
    for conv_name, info in stats_sorted:
        name = f'{conv_name if len(conv_name) <= 20 else conv_name[:20] + "..."}'
        basic_info = f'{info["messages_nr"]}'
        if len(info["participants"]) > 2:
            basic_info += " [Group]"
        timespan = f'({datetime.datetime.fromtimestamp(info["first"] / 1000).strftime("%Y-%m-%d")} - ' \
                   f'{datetime.datetime.fromtimestamp(info["last"] / 1000).strftime("%Y-%m-%d")})'
        average = f' Avg: {info["messages_nr"] / ((info["last"] - info["first"]) // 86400000):.2f} /day' \
                  if (info["last"] - info["first"]) // 86400000 else ''
        print("{:<25} {:<15} {:<20} {:<10}".format(name, basic_info, timespan, average))
