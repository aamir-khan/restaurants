import csv
from datetime import datetime
import os.path
import re

DAY_TO_INT_MAP = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5, 'sun': 6}


def parse_time(time_str):
    """Parse the time_str to time object."""
    format_str = "%I:%M %p" if ':' in time_str else "%I %p"
    return datetime.strptime(time_str.strip(), format_str).time()


def schedule(working_days, working_time):
    """
    Update the schedule_per_day for given days and the working hours of those days.
    :param working_days: (list) Working days.
    :param working_time: (str) The working hours.
    :return: (dict) The dictionary of days and working hours of per day.
    """
    working_time_start, working_time_end = working_time.strip().split('-')

    working_time_start = parse_time(working_time_start)
    working_time_end = parse_time(working_time_end)

    schedule_per_day_map = {}
    for working_day in working_days:
        # If the days range
        if '-' in working_day:
            start_day, end_day = working_day.strip().split('-')
            start_day_index = DAY_TO_INT_MAP[start_day.strip().lower()]
            end_day_index = DAY_TO_INT_MAP[end_day.strip().lower()]
            for day in range(start_day_index, end_day_index+1):
                schedule_per_day_map[day] = {'start': working_time_start, 'end': working_time_end}
        else:
            day = DAY_TO_INT_MAP[working_day.strip().lower()]
            schedule_per_day_map[day] = {'start': working_time_start, 'end': working_time_end}
    return schedule_per_day_map


def parse_restaurant_work_schedule(restaurant_work_schedule):
    """Parse the working schedule of a restaurant in a week.
    :param restaurant_work_schedule: (str) The weekly work schedule in string format.
    :return: A dictionary of working days and time.
    """
    schedule_per_day = {}
    working_days_slots = restaurant_work_schedule.split('/')
    for slot in working_days_slots:
        working_days_slot = slot.strip()
        matcher = re.search(r"\d", working_days_slot)
        # Find the occurrence of time in the schedule. like Mon-Sun 11:30 am - 9 pm
        working_start_index = matcher.start()
        working_days = working_days_slot[:working_start_index]
        working_time = working_days_slot[working_start_index:]
        # Split on "," if the entry was like "Mon-Thu, Sun"
        working_days = working_days.strip().split(",")
        working_slot_map = schedule(working_days, working_time)
        schedule_per_day.update(**working_slot_map)

    return schedule_per_day


def is_time_between(begin_time, end_time, check_time):
    """Check if the time is between the working hours.
    :param begin_time:
    :param end_time:
    :param check_time:
    :return: True if the given time is in between the working hours.
    """
    if begin_time < end_time:
        return begin_time <= check_time <= end_time
    # crosses midnight
    else:
        return check_time >= begin_time or check_time <= end_time


def is_restaurant_open_at_given_datetime(restaurant_work_schedule, search_datetime):
    """Check if the restaurant is open at the given datetime.

    :param restaurant_work_schedule: (str) The work schedule of the restaurant.
    :param search_datetime: (datetime) The datetime to check.
    :return: True if the restaurant is open at the given datetime.
    """
    restaurant_work_days_and_hours = parse_restaurant_work_schedule(restaurant_work_schedule)
    search_weekday = search_datetime.weekday()
    search_time_only = search_datetime.time()
    if search_weekday in restaurant_work_days_and_hours:
        working_hours_of_day = restaurant_work_days_and_hours[search_weekday]
        if is_time_between(working_hours_of_day['start'], working_hours_of_day['end'], search_time_only):
            return True
    return False


def get_open_restaurants(csv_filename, search_datetime):
    """
    Search the list of open restaurants at given time.

    :param csv_filename: (str) CSV file containing the restaurants working hours data.
    :param search_datetime: (datetime) datetime to search the open restaurants.
    :raises IoError: If the file not found raises the IoError.
    :return: The list of restaurants names open at the given datetime.
    """
    open_restaurants = []
    with open(csv_filename) as csvfile:
        read_csv = csv.reader(csvfile)
        for restaurant in read_csv:
            restaurant_name, restaurant_work_schedule = restaurant[0], restaurant[1]
            if is_restaurant_open_at_given_datetime(restaurant_work_schedule, search_datetime):
                open_restaurants.append(restaurant_name)

    return open_restaurants


if __name__ == '__main__':
    while True:
        csv_file_name = raw_input("Please enter the csv file name(or press enter to use rest_hours.csv): ")
        if csv_file_name == "":
            csv_file_name = "rest_hours.csv"
            break
        elif os.path.isfile(csv_file_name):
            break
        else:
            print "This file doesn't exist in this directory."

    while True:
        search_time = raw_input("Please enter datetime(YYYY-MM-DD hh:mm:ss) or press ENTER to use now() to check the "
                                "open restaurants.: ")
        if search_time == "":
            search_time = datetime.now()
            break
        else:
            try:
                search_time = datetime.strptime(search_time, '%Y-%m-%d %H:%M:%S')
                break
            except ValueError:
                print "Wrong format!!!"

    open_restaurants_ = get_open_restaurants(csv_file_name, search_time)
    print "**********************************************************"
    print "Following restaurants are open:" if open_restaurants_ else "No restaurant open."
    print "\n".join(open_restaurants_)
    print "**********************************************************"
