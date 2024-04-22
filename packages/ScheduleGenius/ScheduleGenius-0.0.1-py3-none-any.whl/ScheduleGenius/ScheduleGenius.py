import os

def load_schedule(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return file.readlines()
    else:
        return []

def save_schedule(file_path, schedule):
    with open(file_path, 'w') as file:
        file.writelines(schedule)

def is_duplicate_event(schedule, event):
    return event + '\n' in schedule

def add_schedule(file_path, event):
    schedule = load_schedule(file_path)
    if not is_duplicate_event(schedule, event):
        schedule.append(event + '\n')
        save_schedule(file_path, schedule)
    else:
        print(f"일정 '{event}'은 이미 존재합니다.")

def get_schedule(file_path):
    return load_schedule(file_path)

def save_schedule_by_date(file_path):
    schedule = load_schedule(file_path)
    schedule_by_date = {}
    for event in schedule:
        date, event_text = event.split(':', 1)
        date = date.strip()
        event_text = event_text.strip()
        if date in schedule_by_date:
            schedule_by_date[date].append(event_text)
        else:
            schedule_by_date[date] = [event_text]

    for date, events in schedule_by_date.items():
        file_name = f"{date}_schedule.txt"
        with open(file_name, 'w') as file:
            file.writelines('\n'.join(events))

def print_sorted_schedule(file_path):
    schedule = load_schedule(file_path)
    schedule_by_date = {}
    for event in schedule:
        date, event_text = event.split(':', 1)
        date = date.strip()
        event_text = event_text.strip()
        if date in schedule_by_date:
            schedule_by_date[date].append(event_text)
        else:
            schedule_by_date[date] = [event_text]

    sorted_schedule = sorted(schedule_by_date.items(), key=lambda x: x[0])
    for date, events in sorted_schedule:
        print(f"{date}:")
        for event in events:
            print(f"\t{event}")
