# Progress Report

## Week 1 Status Update - 195 Words

During Week 1, our main goal was to get familiar with our data sources and make sure we could actually access everything we planned to use. We started by downloading and reviewing the SimpleMaps World Cities dataset. We looked through the fields it provided, such as city name, latitude, longitude, country, and population. We confirmed it includes the top cities we need and that the population values look reasonable for a global comparison project. We also noted that the population data is a single snapshot from 2025, which means we will not be able to look at population change over time, but it still works well for our project because we only need the most recent estimates.

At the same time, we worked on setting up and testing the Google Maps Air Quality API. We created a Google Cloud project, generated an API key, and tried sample requests to make sure the connection worked. We were able to successfully get real air quality and weather data for a few cities as a test. This gave us a better idea of what fields we will have available later, including things like AQI, PM2.5, and temperature.

## Week 2 Status Update - 193 Words

In Week 2, our focus was on building the basic structure of our data pipeline so that collecting and organizing data later would be easier. First, we set up a folder organization in our GitHub repository. We now have separate folders for raw data, processed data, scripts, and documentation. This will help keep things clean as the number of files grows throughout the project.

Next, we started writing the main functions that will be called the Google Air Quality API. We tested pulling in data using latitude and longitude pairs from the SimpleMaps dataset. We created a basic script that sends a request and then stores the JSON response so we can parse out variables like air quality index, pollutants, and temperature. 

We also discussed and made initial decisions on a consistent schema that we will use when we merge everything together. This included making sure we use the same column names for cities, making sure all coordinates stay in the same numeric format, and deciding which environmental variables we should keep. We also started a simple metadata document where we will track how each field is created and where it came from.

## Week 3 Status Update - 320 Words

During Week 3, our main goal was to scale up our work from the sample testing earlier to collect full air quality data for all 500 of the most populated cities in the world. We began by validating the full SimpleMaps dataset again to ensure that everything was still clean and usable before querying the API. We checked for missing values, confirmed that population data was available for almost every city, and verified that all latitude and longitude coordinates were valid. We also looked for duplicate cities using the city name and country fields, since duplicates could cause problems when merging later.

After confirming the dataset quality, we selected the top 500 cities by population and saved them as a new file so the collection process would be based on verified data. This reduced our dataset to exactly what we needed for API queries.

The largest piece of work in Week 3 was running the full API data collection process. We improved the API function by adding retry logic to handle issues like timeouts and rate limiting. We also included exponential backoff when the Google API returned too many requests at once. While collecting data, we printed status updates every 50 cities so we could monitor progress and ensure the script wasn't stuck or crashing. The full collection took around 7 minutes and successfully returned data for 500 cities, although 54 cities still had issues retrieving AQI information. These errors were logged in a separate file so we can decide later whether to retry those specific cities.

We stored the full raw dataset (including both successful and error results) as a timestamped CSV file to keep track of when the data was retrieved. We also created a separate error log so issues are documented and visible. Another aspect we recorded was timestamps and collection details in a curation log, which tracks every major processing action to support reproducibility and transparency.

## Week 4 Status Update - 329 Words

Week 4 focused on the cleaning, standardization, and integration of the large set of air quality data collected in Week 3. First, we loaded both the validated top 500 cities dataset and the full raw air quality dataset into a new working notebook. To keep track of important actions, we continued updating our curation log, which documents every major step with a timestamp and short description. This supports project reproducibility and helps us track any issues that appear later in the analysis.

The first cleaning task was standardizing column names. We renamed latitude and longitude columns so that both datasets used the same column names and structure. We also ensured values like population, latitude, longitude, and AQI were stored in numeric format, so there would be no errors when computing statistics later. Then, we trimmed any extra whitespace from city and country fields to reduce merge conflicts and mismatched city entries.

Next, we looked at missing data. As seen in Week 3, the API did not return air quality results for all cities, which led to 54 cities with missing AQI values. Instead of removing them immediately, we added a new column called data_quality_flag to mark whether each city's AQI data was complete or missing. This allows us to still keep the city in the dataset for population comparisons or geographic mapping, while being transparent about the air quality data quality.

The most important step in Week 4 was merging the cleaned datasets. We joined the city population data and the air quality data using the shared fields city and country. This resulted in 508 merged records, but after removing duplicates we ended with 496 unique city-country pairs. We then performed validation checks, such as confirming that coordinate ranges were still valid, verifying that AQI values fell within a reasonable range (0–98), and reviewing completeness percentages for each field. After confirming the data quality, we organized the final columns and saved the final integrated dataset to data/integrated_cities_air_quality_final.csv.

## Timeline Table

| Week | Planned Tasks | Status |
|------|--------------|--------|
| Week 1 | Data familiarization + API setup | Completed |
| Week 2 | Pipeline + folder structure | Completed |
| Week 3 | Large-scale data collection | Completed |
| Week 4 | Cleaning + integration | Completed |
| Week 5 | EDA + correlation analysis | Planned |
| Week 6 | Statistical testing + visuals | Planned |
| Week 7 | Finalization + report | Planned |

## Description of Changes and Reflection - 232 Words

So far, our project has mostly stayed close to the original plan, but a few things have changed as we actually worked with the data and the API.

First, we combined parts of Weeks 3 and 4 into one larger workflow notebook instead of keeping collection and cleaning completely separate. Once we started pulling data for all 500 cities, it made more sense to validate, clean, and merge the data in the same place where we logged the API calls. This changed the structure a bit, but the end result still matches the original goals for those weeks.

Second, API behavior caused some delays. Rate limiting and occasional timeouts meant that large-scale collection took longer than expected, and 54 cities ended up with missing AQI values. Instead of dropping them, we added a data_quality_flag column and kept them in the dataset. This is a small adjustment from "complete AQI for all cities" to "mostly complete AQI, with explicit flags for gaps."

Third, we have not yet pulled historical air quality or weather data, even though the original plan mentioned using a 2022–2025 time range. So far we are working with current conditions. Depending on time and credit limits, we may narrow that historical scope or focus more on cross-sectional patterns.

We have not received major feedback yet, but building the curation log and clear file structure are things we emphasized a lot.

## Team Member Contribution Statements - 57 Words

We both worked together on all key parts of the project, especially when writing and testing the code. While our assigned responsibilities focused on different weeks, our GitHub commits mainly reflect who led each stage rather than who contributed overall. We collaborated closely throughout, and both of us reviewed, improved, and supported the work done every week.
