# Task for Data Engineers

You can use any framework or library you like, however you should provide some
explanation on how to reproduce the calculations in your code on our machines.

Please take 1 hour to complete the task with as much details as you can.
We are providing all the data in files as a shortcut to easily complete the task,
however we are looking for how you deal with APIs as well.
We are looking after the way you structure your code, documentation, tests, database/files schema.

When taking shortcuts please explain why in comments so we know.
If you end up with some pieces of functionality not completely working due to
lack of time, then it's fine to submit that as well with some comments explaining.
Comments with ideas and reasons for improvement are welcome as well.

We want to know the half-hourly carbon footprint for a given asset.
So for a given day there will be 48 rows of data with `HalfHourId` from 1 to 48.

## Requirements

The task involves the following requirements:

- processing data from different data sources e.g. APIs and CSV files
- resampling the data to a common rate
- performing the calculations
- storing the results in a CSV file or SQLite database
- retrieving the results from the storage filtering them by `HalfHourId` range 14-20
- plot the retrieval (or the calculation, or the API data)

# Data sources

We need to combine data about the actual/forecast carbon footprint with the
power measurement of the asset identified by the ID `abc123xyz`.

## Carbon intensity data

The Carbon Intensity data can be retrieved via the API provided by National Grid.

API docs at: https://carbon-intensity.github.io/api-definitions/#intensity

Sample API call retrieving `gCO2eq/KWhe` (providing start/end as input parameters):

```sh
curl -X GET https://api.carbonintensity.org.uk/intensity/2019-11-25/2019-11-26 \
  -H 'Accept: application/json'
```

If for any reason the API retrieval does not work, then the file `carbon_intensity_2019-11-25.json`
can be used instead.

## Power measurements

The asset is measured following the COV rule (change of value). The data for
one day power measurements (`KW`) is in the CSV file `power_measurements_2019-09-25.csv`.

What's the COV for this time-series? Is it always the same?
