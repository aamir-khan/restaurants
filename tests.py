from datetime import datetime
import unittest

from restaurants import get_open_restaurants, parse_restaurant_work_schedule


class SimpleTest(unittest.TestCase):

    testing_data_csv = 'rest_hours_tests.csv'

    def test_file_not_found(self):
        with self.assertRaises(IOError):
            current_date = datetime.now()
            get_open_restaurants('unknown_file.csv', current_date)

    def test_schedule_parsing_with_comma_separated_schedule(self):
        schedule_str = "Mon, Wed-Sun 11 am - 10 pm"
        working_time_start = datetime.strptime('11 am', '%I %p').time()
        working_time_end = datetime.strptime('10 pm', '%I %p').time()
        schedule_days_map = parse_restaurant_work_schedule(schedule_str)

        # Assert that the restaurant opens for only 6 days.
        self.assertEqual(len(schedule_days_map.keys()), 6)
        monday_opening_time = schedule_days_map[0]['start']
        monday_closing_time = schedule_days_map[0]['end']
        self.assertEqual(monday_opening_time, working_time_start)
        self.assertEqual(monday_closing_time, working_time_end)
        tuesday_week_day_number = 1
        # Assert that the restaurant is closed on Tuesday.
        self.assertIsNone(schedule_days_map.get(tuesday_week_day_number))

    def test_schedule_parsing_with_multiple_working_slot(self):
        schedule_str = "Mon 11:30 am - 10:30 pm / Tue 10:30 am - 10:30 pm"
        working_time_start = datetime.strptime('11:30 am', '%I:%M %p').time()
        working_time_end = datetime.strptime('10:30 pm', '%I:%M %p').time()
        schedule_days_map = parse_restaurant_work_schedule(schedule_str)

        # Assert that the restaurant opens for only 2 days.
        self.assertEqual(len(schedule_days_map.keys()), 2)
        monday_opening_time = schedule_days_map[0]['start']
        monday_closing_time = schedule_days_map[0]['end']
        self.assertEqual(monday_opening_time, working_time_start)
        self.assertEqual(monday_closing_time, working_time_end)
        wednesday_week_day_number = 2
        self.assertIsNone(schedule_days_map.get(wednesday_week_day_number),
                          "The restaurant must be closed on Wednesday")

    def test_only_one_restaurant_open_on_3_am(self):
        """Test that on Monday only "Naan 'N' Curry" restaurant is open."""
        monday_april_one_3_am = datetime.strptime('2019-04-01 03:00:00', '%Y-%m-%d %H:%M:%S')
        open_restaurants = get_open_restaurants(self.testing_data_csv, monday_april_one_3_am)
        self.assertEqual(len(open_restaurants), 1)
        self.assertEqual(open_restaurants[0], "Naan 'N' Curry")

    def test_no_restaurant_open_after_4_am(self):
        monday_april_one_5_am = datetime.strptime('2019-04-01 05:00:00', '%Y-%m-%d %H:%M:%S')
        open_restaurants = get_open_restaurants(self.testing_data_csv, monday_april_one_5_am)
        self.assertEqual(len(open_restaurants), 0)

    def test_no_restaurant_open_after_9_pm(self):
        wed_9_pm = datetime.strptime('2019-03-27 19:00:00', '%Y-%m-%d %H:%M:%S')
        open_restaurants = get_open_restaurants(self.testing_data_csv, wed_9_pm)
        self.assertGreater(len(open_restaurants), 1)
        self.assertIn('A-1 Cafe Restaurant', open_restaurants)


if __name__ == '__main__':
    unittest.main()
