### **Data Dictionary: `integrated_cities_air_quality_final.csv`**

This table describes the final cleaned dataset produced by the pipeline. It includes population values from the SimpleMaps World Cities dataset and air quality metrics from the Google Maps Air Quality API.

| **Column Name** | **Type** | **Source** | **Description** |
|-----------------|----------|------------|-----------------|
| `city` | `string` | SimpleMaps | Official city name (may include alternate Latinized spellings depending on data provider). |
| `country` | `string` | SimpleMaps | Country where the city is located, written in English (e.g., *Japan, India*). |
| `iso2` | `string` | SimpleMaps | ISO 3166-1 alpha-2 country code (2 characters, e.g., `US`, `CN`). |
| `iso3` | `string` | SimpleMaps | ISO 3166-1 alpha-3 country code (3 characters, e.g., `USA`, `CHN`). |
| `latitude` | `float` | SimpleMaps | City latitude coordinate (degrees). Converted to numeric and validated for range (-90 to 90). |
| `longitude` | `float` | SimpleMaps | City longitude coordinate (degrees). Converted to numeric and validated for range (-180 to 180). |
| `population` | `float` | SimpleMaps | Estimated population of the city based on dataset snapshot. Used to rank the top 500 cities globally. |
| `aqi` | `float` *(nullable)* | Google Air Quality API | Real-time Air Quality Index measured at the moment of collection. Missing values indicate unavailable API data. |
| `aqi_category` | `string` *(nullable)* | Google Air Quality API | Text label describing AQI health category (e.g., *Good air quality*, *Poor air quality*). |
| `dominant_pollutant` | `string` *(nullable)* | Google Air Quality API | Main pollutant determining the AQI value (e.g., `pm25`, `pm10`, `o3`, `no2`, `so2`, `co`). Blank when monitoring data was unavailable. |
| `data_quality_flag` | `string` | Pipeline Cleaning Script | Indicates if AQI data is available: `complete` or `missing`. Missing rows are retained for transparency instead of deletion. |
| `collection_timestamp` | `string` | Google Air Quality API | ISO-8601 timestamp representing when the AQI value was retrieved (UTC). Captures real-time nature of air data. |

---

#### **Notes & Assumptions**

- Population values reflect a **single snapshot**, not historical data or projections.
- AQI values represent **real-time measurements**; they are **not daily or annual averages**.
- Cities marked `missing` for AQI **may not be clean** — absence of monitoring is not evidence of low pollution.
- Duplicate city–country pairs were resolved by retaining only one record to avoid ranking biases.

---