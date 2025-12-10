"""
Full Data Collection Script
Executes large-scale API data collection for all 500 cities with error handling
"""

import pandas as pd
import numpy as np
import requests
import json
import time
from datetime import datetime
from config_template import API_KEY, BASE_URL

# Create log list to track all operations
curation_log = []

def log_step(step_name, details):
    """Log a curation step with timestamp"""
    timestamp = datetime.now().isoformat()
    log_entry = {
        'timestamp': timestamp,
        'step': step_name,
        'details': details
    }
    curation_log.append(log_entry)
    print(f"[{timestamp}] {step_name}: {details}")

def validate_simplemaps_data(filepath='data/worldcities.csv'):
    """Load and validate the SimpleMaps dataset"""
    cities_df = pd.read_csv(filepath)
    log_step('Data Load', f'Loaded {len(cities_df)} cities from SimpleMaps dataset')
    print(f"Shape: {cities_df.shape}")
    print(cities_df.head(3))
    
    # Check missing values
    missing_data = cities_df.isnull().sum()
    print(missing_data[missing_data > 0])
    missing_summary = missing_data[missing_data > 0].to_dict()
    log_step('Validation - Missing Values', f'{len(missing_summary)} columns have missing values')
    
    # Check duplicates
    duplicate_cities = cities_df.duplicated(subset=['city', 'country'], keep=False)
    num_duplicates = duplicate_cities.sum()
    print(f"Duplicates: {num_duplicates}")
    if num_duplicates > 0:
        print(cities_df[duplicate_cities][['city', 'country', 'lat', 'lng']].head(10))
    log_step('Validation - Duplicates', f'Found {num_duplicates} duplicate city-country combinations')
    
    # Population data check
    cities_with_pop = cities_df[cities_df['population'].notna()]
    pop_coverage = len(cities_with_pop) / len(cities_df) * 100
    print(f"Population coverage: {pop_coverage:.1f}%")
    print(f"Missing: {cities_df['population'].isna().sum()}")
    print(cities_with_pop['population'].describe())
    log_step('Validation - Population Data', f'{pop_coverage:.1f}% of cities have population data')
    
    # Check coordinate validity
    invalid_coords = cities_df[
        (cities_df['lat'].isna()) | 
        (cities_df['lng'].isna()) |
        (cities_df['lat'] < -90) | 
        (cities_df['lat'] > 90) |
        (cities_df['lng'] < -180) | 
        (cities_df['lng'] > 180)
    ]
    print(f"Invalid coords: {len(invalid_coords)}")
    if len(invalid_coords) > 0:
        print(invalid_coords[['city', 'country', 'lat', 'lng']].head())
    log_step('Validation - Coordinates', f'{len(invalid_coords)} cities with invalid coordinates')
    
    return cities_df

def select_top_500_cities(cities_df):
    """Select top 500 cities by population"""
    valid_cities = cities_df[
        (cities_df['population'].notna()) &
        (cities_df['lat'].notna()) &
        (cities_df['lng'].notna())
    ].copy()
    
    top_500_cities = valid_cities.nlargest(500, 'population').reset_index(drop=True)
    
    print(f"Pop range: {top_500_cities['population'].min():,.0f} to {top_500_cities['population'].max():,.0f}")
    print(top_500_cities[['city', 'country', 'population']].head(10))
    
    # Save validated top 500 cities
    top_500_cities.to_csv('data/raw_top_500_cities.csv', index=False)
    log_step('Data Selection', 'Selected and saved top 500 cities by population')
    
    return top_500_cities

def get_current_air_quality(lat, lon, api_key, retry_count=3):
    """Get current air quality with retry logic and error handling"""
    url = f"{BASE_URL}currentConditions:lookup"
    params = {"key": api_key}
    data = {
        "location": {
            "latitude": lat,
            "longitude": lon
        }
    }
    
    for attempt in range(retry_count):
        try:
            response = requests.post(url, params=params, json=data, timeout=10)
            
            if response.status_code == 200:
                return {'status': 'success', 'data': response.json()}
            elif response.status_code == 429:
                # Rate limit hit, wait longer
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                return {'status': 'error', 'error_type': 'http_error', 'code': response.status_code}
                
        except requests.exceptions.Timeout:
            if attempt < retry_count - 1:
                time.sleep(1)
                continue
            return {'status': 'error', 'error_type': 'timeout'}
        except Exception as e:
            return {'status': 'error', 'error_type': 'exception', 'message': str(e)}
    
    return {'status': 'error', 'error_type': 'max_retries'}

def collect_all_air_quality_data(top_500_cities):
    """Collect air quality data for all 500 cities"""
    collection_start = datetime.now()
    air_quality_data = []
    error_log = []
    
    print(f"Collecting data for 500 cities:")
    log_step('API Collection Start', f'Beginning collection for {len(top_500_cities)} cities')
    
    for idx, row in top_500_cities.iterrows():
        city_name = row['city']
        country = row['country']
        lat = row['lat']
        lon = row['lng']
        population = row['population']
        
        if (idx + 1) % 50 == 0:
            print(f"{idx + 1}/{len(top_500_cities)}")
        
        result = get_current_air_quality(lat, lon, API_KEY)
        
        if result['status'] == 'success':
            api_data = result['data']
            
            aqi = None
            category = None
            dominant_pollutant = None
            
            if 'indexes' in api_data and len(api_data['indexes']) > 0:
                index_data = api_data['indexes'][0]
                aqi = index_data.get('aqi', None)
                category = index_data.get('category', None)
                dominant_pollutant = index_data.get('dominantPollutant', None)
            
            air_quality_data.append({
                'city': city_name,
                'country': country,
                'lat': lat,
                'lon': lon,
                'aqi': aqi,
                'aqi_category': category,
                'dominant_pollutant': dominant_pollutant,
                'collection_timestamp': datetime.now().isoformat(),
                'status': 'success'
            })
        else:
            # Error log
            error_log.append({
                'city': city_name,
                'country': country,
                'error_type': result.get('error_type', 'unknown'),
                'timestamp': datetime.now().isoformat()
            })
            
            air_quality_data.append({
                'city': city_name,
                'country': country,
                'lat': lat,
                'lon': lon,
                'aqi': None,
                'aqi_category': None,
                'dominant_pollutant': None,
                'collection_timestamp': datetime.now().isoformat(),
                'status': 'error'
            })
        
        # Rate limiting
        time.sleep(0.25)
    
    collection_end = datetime.now()
    duration = (collection_end - collection_start).total_seconds()
    
    print(f"Done! {duration} seconds)")
    log_step('API Collection Complete', f'Collected {len(air_quality_data)} records in {duration:.1f}s, {len(error_log)} errors')
    
    return air_quality_data, error_log

def save_raw_data(air_quality_data, error_log):
    """Save raw API data and error log"""
    # Save raw data
    raw_aq_df = pd.DataFrame(air_quality_data)
    raw_filename = f"data/raw_air_quality_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    raw_aq_df.to_csv(raw_filename, index=False)
    log_step('Data Storage', f'Saved raw API data: {raw_filename}')
    
    # Save error log if there are errors
    if len(error_log) > 0:
        error_df = pd.DataFrame(error_log)
        error_filename = f"data/collection_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        error_df.to_csv(error_filename, index=False)
        print(f"Saved errors: {error_filename}")
        log_step('Error Logging', f'Saved {len(error_log)} errors to {error_filename}')
    
    return raw_aq_df

def main():
    """Main execution function"""
    print("=== Full Data Collection Script ===\n")
    
    # Part 1: Validate SimpleMaps data
    cities_df = validate_simplemaps_data()
    
    # Part 2: Select top 500
    top_500_cities = select_top_500_cities(cities_df)
    
    # Part 3: Collect all air quality data
    air_quality_data, error_log = collect_all_air_quality_data(top_500_cities)
    
    # Part 4: Save raw data
    raw_aq_df = save_raw_data(air_quality_data, error_log)
    
    print("\n=== Full Data Collection Complete ===")
    return raw_aq_df

if __name__ == "__main__":
    main()
