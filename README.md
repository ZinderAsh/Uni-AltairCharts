# Assignment 6

Scripts and data for visualizing corona statistics in Norwegian counties. Also includes a Flask app to host these statistics.
This app was written for a university assignment.

## Dependencies

Python3 is required to run these scripts.

These packages are requires for this scripts:
- pandas (v1.1.3)
- altair (v4.1.0)
- flask (v1.1.2)

Install these using [pip](https://pip.pypa.io/en/stable/).
```
pip install pandas
pip install altair
pip install flask
```

## Usage

To start the flask app, simply run the script from the terminal using:
```
python web_visualization.py
```

To use this module's methods, import it and use it as such. You can see templates/help_page.html for documentation.

```python
import web_visualization as wv

# counties is a dictionary of all counties as well as their respective filenames for data (with .csv omitted)
wv.counties

# Use this to get the complete filepath for a county's data
county_file = wv.get_county_file("Oslo")

# Use this to only make a dataframe of data, without turning it into a chart
df = wv.make_dataframe(county="Oslo")
# You can also set start and end date for the statistics. County can also be omitted to include all counties
df = wv.make_dataframe(fromdate="2020-05-01", todate="2020-05-31")

# Use these methods to generate charts with various data
# All these methods accept the optional county, fromdate and todate arguments
reported_cases = plot_reported_cases()
cumulative_cases = plot_cumulative_cases()
both_cases = plot_both()

# To start det flask app, you can run
wv.main()
```
