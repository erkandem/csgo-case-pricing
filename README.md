# csgo case pricing

a django app to calculate the price a counter strike global offensive
container from its components


## status
see first commit or prototype.

-  admin currently was just written to check the data. Not used to work on the objects.

## getting started

initialise the database for example with:

    python manage.py populate_cases operation_broken_fang_case
    python manage.py calculate_case operation_broken_fang_case
    python manage.py fix_prices operation_broken_fang_case # uuid printed from calculate_case step


TODOs:
- create a package for constants
  - write `setup.py`
  - CI steps?
  - publish on PYPI
- create a package for cases_data
- expand info inside cases_data package
