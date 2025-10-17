# Project Plan

## Overview

This project investigates the relationship between urban population characteristics and environmental conditions across global cities. Specifically, we will analyze how city population size correlates with air quality metrics and weather patterns using data from approximately 500 of the world's most populous cities. By integrating static population data with historical environmental measurements, we aim to identify patterns and relationships that may inform our understanding of urbanization's environmental impacts.

The project will employ a descriptive and exploratory analysis approach, with statistical correlation methods and data visualization techniques to reveal insights. Our analysis will examine both global patterns and potential regional variations, comparing how population-environment relationships differ across continents and development contexts. If time permits, we will develop an interactive bqplot map allowing users to explore the data spatially.

This work is significant because it addresses the intersection of two critical global trends: rapid urbanization and environmental change. Understanding whether and how city size relates to air quality and weather conditions can provide insights relevant to urban planning, public health policy, and sustainability initiatives.

## Research Questions

Our analysis will address three primary research questions:

**1. Is there a significant correlation between city population size and average air quality (AQI/PM2.5/Other metric, still WIP) over the 2022-2025 period?**

This question examines whether larger cities systematically experience worse air quality than smaller cities, using both the Universal Air Quality Index and specific pollutant measurements like fine particulate matter (PM2.5).

**2. Do larger cities experience higher temperatures or worse air quality compared to smaller cities?**

This comparative question will categorize cities into population brackets (e.g., mega-cities >10M, large cities 5-10M, medium cities 1-5M, smaller cities <1M) and compare their average environmental metrics. We will use visualization techniques such as box plots and violin plots to show distributions, and potential statistical tests as well.

**3. How do air quality patterns vary across cities of different sizes in different global regions?**

This question introduces a geographic dimension, examining whether the relationship between population size and air quality differs across continents or regions (Africa, Asia, Europe, Americas, Oceania). We will create regional scatter plots and calculate region-specific correlations to identify whether certain regions show stronger or weaker population-environment relationships.

## Team Roles and Responsibilities

**Maclain Prom & Diego Marquez**

### Shared Responsibilities:

- Acquire, process, and explore the SimpleMaps World Cities dataset and Google Maps Air Quality API data
- Manage API authentication, rate limiting, and error handling
- Develop and implement the city sampling strategy (e.g., filter top 500 cities by population)
- Collect, clean, and integrate population, air quality, and weather data into a unified dataset
- Perform descriptive statistics, correlation analysis, and statistical significance testing
- Create regional groupings and conduct comparative analyses
- Develop both static and interactive visualizations (scatter plots, regional comparisons, distributions, and maps)
- Refine the research question and interpret analytical results
- Document the full methodology, findings, and code structure
- Maintain repository organization, conduct code reviews, and ensure quality assurance
- Collaboratively prepare the final presentation and written report

### Deliverables (Joint):

- Clean, integrated dataset combining city, air quality, and weather data
- Statistical analysis results and correlation matrices
- Complete visualization suite (static and interactive if time permits)
- Comprehensive project report

## Datasets

### Dataset 1: SimpleMaps World Cities Database (Free Basic Version)

- **Source:** https://simplemaps.com/data/world-cities
- **Description:** Contains approximately 41,000 cities worldwide with geographic and demographic information. Last updated May 11, 2025.
- **Key Fields:** City name, latitude, longitude, country, ISO codes, population (static snapshot)
- **Use Case:** Provides baseline population data and coordinates for matching with environmental data
- **Limitations:** Static population snapshot with no growth rates or historical trends; free version has limited fields compared to paid version

### Dataset 2: Google Maps Air Quality API

- **Source:** https://developers.google.com/maps/documentation/air-quality/overview
- **Description:** Provides current and historical air quality measurements including pollutant concentrations and Air Quality Index values, along with weather data
- **Key Fields:** Universal AQI, PM2.5, PM10, O3, NO2, temperature, humidity, timestamps
- **Use Case:** Historical environmental conditions (2022-2025) for correlation with population metrics
- **API Access:** Free tier with $200/month credit (should be sufficient for 500 cities with reasonable queries)
- **Limitations:** Rate limits apply; historical data availability depends on location and time period

### Data Merging and Integration Approach:

1. Filter SimpleMaps dataset to top 500 cities by population
2. Extract coordinates (latitude, longitude) for each city
3. Query Google Air Quality API using coordinates to retrieve historical environmental data
4. Map country codes to regional classifications
5. Merge datasets on city, creating integrated dataset with population, coordinates, air quality, weather, and region
6. Handle missing data through appropriate methods (imputation, exclusion, or noting limitations)

## Timeline

### Week 1: Data Familiarization and Setup

- Explore the SimpleMaps World Cities dataset to understand structure, coverage, and key fields — Maclain
- Configure and test the Google Air Quality API, including sample queries and response inspection — Diego
- Document both data sources, noting formats, licensing, and access limitations — Maclain
- Outline how the project fits into the data lifecycle model from class and define the main research question — Diego

### Week 2: Building the Data Pipeline

- Design the folder and file structure for raw, processed, and final datasets — Maclain
- Develop the main API functions for retrieving and parsing city-level air quality data — Diego
- Establish a unified schema for integration, with consistent column naming, datatypes, and units — Joint
- Set up metadata templates for all collected data — Joint

### Week 3: Full Data Collection

- Execute large-scale API data collection for the top 500 cities with error handling and rate limiting — Maclain
- Validate the SimpleMaps dataset, ensuring clean city identifiers and reliable population data — Diego
- Store both raw and processed files using consistent naming conventions and folder structure — Joint
- Record timestamps, logs, and collection notes for reproducibility — Joint

### Week 4: Cleaning, Normalization, and Integration

- Standardize field names, formats, and units across datasets — Maclain
- Merge population, air quality, and weather data into a single integrated table — Diego
- Run validation checks for duplicate cities, missing values, and inconsistent joins — Joint
- Document each cleaning and integration step in a structured curation log — Joint

### Week 5: Exploratory Data Analysis (Phase 1)

- Compute descriptive statistics for all major variables — Maclain
- Examine variable distributions (population, AQI, weather metrics) to identify trends and outliers — Diego
- Assess correlations between population size and air quality indicators — Diego
- Conduct regional comparisons to see how urban size and location relate to air quality — Maclain
- Record analytical results and note possible refinements to the research question — Joint

### Week 6: Statistical Testing and Interpretation (Phase 2)

- Perform correlation and significance tests - Maclain
- Investigate differences across regional or climate groupings — Diego
- Create summary visualizations that support interpretation (scatter plots, box plots, and heatmaps) — Joint
- Draft preliminary findings with an emphasis on what patterns the data reveals, not just the visuals — Joint

### Week 7: Metadata, Documentation, and Finalization

- Complete the data dictionary with full variable definitions, units, and source notes — Maclain
- Write workflow documentation describing each step from collection to analysis — Diego
- Review metadata, curation logs, and workflow documentation for clarity and completeness — Joint
- Finalize README, organize the GitHub repository, and prepare the final report — Joint

## Constraints

### Technical Constraints:

- **API Rate Limits:** Google Maps Air Quality API has quotas that limit the number of requests per day/month; must carefully plan query strategy to stay within free tier ($200/month credit)
- **Historical Data Availability:** Google API's historical coverage may vary by location and time period; some cities may have incomplete historical records
- **Computational Resources:** Local machines may face memory constraints when processing large datasets; may need to implement chunked processing or cloud solutions if issues arise
- **SimpleMaps Limitations:** Free version provides only basic city data without additional demographic or economic indicators that could enrich analysis

### Data Constraints:

- **Static Population Data:** SimpleMaps provides a single population snapshot (May 2025) with no historical trends or growth rates, limiting temporal analysis capabilities
- **No Population Density:** Must either calculate density (requires city area data from additional source) or use population size as proxy
- **City-Level Aggregation:** Environmental conditions can vary significantly within large cities; using single coordinate per city may not capture full urban area
- **Missing Data:** Some cities may lack complete air quality or weather records, requiring decisions about exclusion or imputation

### Time Constraints:

- Project must be completed within academic term timeline
- Both team members have other coursework and commitments affecting availability

### Skill Constraints:

- Team may need to refresh knowledge on certain tools and techniques (geographic data handling, API authentication)
- Statistical analysis methods may require additional research and validation
- No prior experience with Google Maps Air Quality API specifically

## Gaps

### Data Availability Uncertainties:

- **Historical Coverage:** Exact timeframe of available historical data from Google API for all 500 cities is unknown until querying begins; may need to adjust time period if data is sparse
- **Weather Data Inclusion:** Need to verify exactly which weather metrics are available through the Air Quality API endpoint vs. requiring separate queries

### Methodological Questions to Consider:

- **Statistical Approaches:** Specific statistical tests for significance and methods for controlling confounding variables (e.g., regional effects, climate zones) require a closer look.
- **Outlier Handling:** Strategy for dealing with cities that are statistical outliers (e.g., extremely polluted cities, unique geographic situations) needs definition