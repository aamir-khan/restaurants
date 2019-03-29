# Restaurants
This is a restaurants data parsing and searching the open restaurants project.

# Requirements
Python 2.7

## Usage

```python
from restaurants import get_open_restaurants
from datetime import datetime

current_date = datetime.now()
csv_file_name = 'rest_hours.csv' # Note: The csv file must be in the project directory.
get_open_restaurants(csv_file_name, current_date) # Returns list of restaurants names that are open on current_date.
```

To run the restaurants module in an interactive mode.

    $ python restaurants.py
    
## Tests
To run the tests:

    $ python tests.py
