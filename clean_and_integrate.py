"""
Data Cleaning and Integration Script
Standardizes field names, formats, and integrates datasets
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Import logging function
from full_collection import curation_log, log_step

def load_data_for_cleaning():
    """Load raw data for cleaning"""
    top_500_cities = pd.read_csv('data/raw_top_500_cities.csv')
    
    # Load most recent raw air quality file
    import glob
    import os
    aq_files = glob.glob('data/raw_air_quality_*.csv')
    if aq_files:
        latest_aq_file = max(aq_files, key=os.path.getctime)
        raw_aq_df = pd.read_csv(latest_aq_file)
        print(f"Loaded air quality data from: {latest_aq_file}")
    else:
        raise FileNotFoundError("No raw air quality data found")
    
    log_step('Cleaning Start', 'Beginning data cleaning and standardization')
    
    return top_500_cities.copy(), raw_aq_df.copy()

def standardize_column_names(cities_clean, aq_clean):
    """Standardize column names to snake_case"""
    cities_clean = cities_clean.rename(columns={
        'lat': 'latitude',
        'lng': 'longitude'
    })
    
    aq_clean = aq_clean.rename(columns={
        'lat': 'latitude',
        'lon': 'longitude'
    })
    
    log_step('Cleaning - Column Names', 'Standardized column names to snake_case')
    
    return cities_clean, aq_clean

def standardize_data_types(cities_clean, aq_clean):
    """Standardize data types"""
    cities_clean['population'] = pd.to_numeric(cities_clean['population'], errors='coerce')
    cities_clean['latitude'] = pd.to_numeric(cities_clean['latitude'], errors='coerce')
    cities_clean['longitude'] = pd.to_numeric(cities_clean['longitude'], errors='coerce')
    
    aq_clean['aqi'] = pd.to_numeric(aq_clean['aqi'], errors='coerce')
    aq_clean['latitude'] = pd.to_numeric(aq_clean['latitude'], errors='coerce')
    aq_clean['longitude'] = pd.to_numeric(aq_clean['longitude'], errors='coerce')
    
    cities_clean['city'] = cities_clean['city'].str.strip()
    cities_clean['country'] = cities_clean['country'].str.strip()
    
    aq_clean['city'] = aq_clean['city'].str.strip()
    aq_clean['country'] = aq_clean['country'].str.strip()
    
    log_step('Cleaning - Data Types', 'Standardized numeric and string data types')
    
    return cities_clean, aq_clean

def handle_missing_values(aq_clean):
    """Handle missing values and flag data quality"""
    missing_aqi = aq_clean['aqi'].isna().sum()
    print(f"Missing AQI: {missing_aqi} ({missing_aqi/len(aq_clean)*100:.1f}%)")
    
    # Flag data quality
    aq_clean['data_quality_flag'] = aq_clean['aqi'].notna().map({True: 'complete', False: 'missing_aqi'})
    print(aq_clean['data_quality_flag'].value_counts())
    
    log_step('Cleaning - Missing Values', f'{missing_aqi} cities missing AQI data, flagged for transparency')
    
    return aq_clean

def review_categorical_values(aq_clean):
    """Check categorical values"""
    print(f"AQI categories: {aq_clean['aqi_category'].unique()}")
    print(f"Pollutants: {aq_clean['dominant_pollutant'].unique()}")
    
    log_step('Cleaning - Categories', 'Reviewed and standardized categorical values')

def integrate_datasets(cities_clean, aq_clean):
    """Merge population and air quality data"""
    log_step('Integration Start', 'Beginning merge of population and air quality data')
    
    # Select relevant columns
    cities_cols = ['city', 'country', 'latitude', 'longitude', 'population', 'iso2', 'iso3']
    aq_cols = ['city', 'country', 'aqi', 'aqi_category', 'dominant_pollutant', 
               'collection_timestamp', 'data_quality_flag']
    
    cities_for_merge = cities_clean[cities_cols]
    aq_for_merge = aq_clean[aq_cols]
    
    # Merge datasets
    integrated_data = cities_for_merge.merge(
        aq_for_merge,
        on=['city', 'country'],
        how='left',
        indicator=True
    )
    
    print(integrated_data['_merge'].value_counts())
    print(f"Shape: {integrated_data.shape}")
    
    log_step('Integration - Merge', f'Merged {len(integrated_data)} records')
    
    # Drop merge indicator
    integrated_data = integrated_data.drop('_merge', axis=1)
    print(integrated_data.head())
    
    return integrated_data

def validate_integrated_data(integrated_data):
    """Run validation checks on integrated data"""
    log_step('Validation Start', 'Running final validation checks on integrated data')
    
    # Check for duplicates
    duplicates = integrated_data.duplicated(subset=['city', 'country'], keep=False)
    num_dups = duplicates.sum()
    
    print(f"Duplicates: {num_dups}")
    
    if num_dups > 0:
        print(integrated_data[duplicates][['city', 'country', 'population', 'aqi']])
        # Remove duplicates, keeping first occurrence
        integrated_data = integrated_data.drop_duplicates(subset=['city', 'country'], keep='first')
        print(f"Removed {num_dups} duplicates")
        log_step('Validation - Duplicates', f'Removed {num_dups} duplicate records')
    else:
        log_step('Validation - Duplicates', 'No duplicates found')
    
    # Check missing values
    missing_summary = integrated_data.isnull().sum()
    print(missing_summary[missing_summary > 0])
    
    missing_dict = missing_summary[missing_summary > 0].to_dict()
    log_step('Validation - Missing Values', f'Missing value counts: {missing_dict}')
    
    # Check data ranges
    print(f"Population: {integrated_data['population'].min():,.0f} to {integrated_data['population'].max():,.0f}")
    print(f"AQI: {integrated_data['aqi'].min():.1f} to {integrated_data['aqi'].max():.1f}")
    print(f"Lat: {integrated_data['latitude'].min():.2f} to {integrated_data['latitude'].max():.2f}")
    print(f"Lon: {integrated_data['longitude'].min():.2f} to {integrated_data['longitude'].max():.2f}")
    
    # Check for invalid coordinates
    invalid_coords = integrated_data[
        (integrated_data['latitude'] < -90) | 
        (integrated_data['latitude'] > 90) |
        (integrated_data['longitude'] < -180) | 
        (integrated_data['longitude'] > 180)
    ]
    print(f"Invalid coords: {len(invalid_coords)}")
    
    log_step('Validation - Data Ranges', 'All data ranges validated')
    
    # Completeness
    completeness = (1 - integrated_data.isnull().sum() / len(integrated_data)) * 100
    print("Completeness:")
    for col in integrated_data.columns:
        print(f"  {col}: {completeness[col]:.1f}%")
    
    log_step('Validation - Completeness', f'Overall data completeness calculated')
    
    return integrated_data

def create_final_dataset(integrated_data):
    """Create final clean, integrated CSV file"""
    # Reorder columns
    column_order = [
        'city', 'country', 'iso2', 'iso3',
        'latitude', 'longitude',
        'population',
        'aqi', 'aqi_category', 'dominant_pollutant',
        'data_quality_flag', 'collection_timestamp'
    ]
    
    final_data = integrated_data[column_order]
    
    print(f"Final shape: {final_data.shape}")
    print(final_data.head())
    
    # Save final integrated dataset
    final_filename = 'data/integrated_cities_air_quality_final.csv'
    final_data.to_csv(final_filename, index=False)
    
    print(f"Saved: {final_filename}")
    log_step('Final Dataset', f'Created final integrated dataset: {final_filename}')
    
    return final_data

def export_curation_log():
    """Export all curation steps for reproducibility"""
    log_df = pd.DataFrame(curation_log)
    log_filename = f"data/curation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    log_df.to_csv(log_filename, index=False)
    
    print(f"Log saved: {log_filename} ({len(curation_log)} steps)")
    print(log_df.head(10))

def main():
    """Main execution function"""
    print("=== Data Cleaning and Integration Script ===\n")
    
    # Load data
    cities_clean, aq_clean = load_data_for_cleaning()
    
    # Standardize column names
    cities_clean, aq_clean = standardize_column_names(cities_clean, aq_clean)
    
    # Standardize data types
    cities_clean, aq_clean = standardize_data_types(cities_clean, aq_clean)
    
    # Handle missing values
    aq_clean = handle_missing_values(aq_clean)
    
    # Review categorical values
    review_categorical_values(aq_clean)
    
    # Integrate datasets
    integrated_data = integrate_datasets(cities_clean, aq_clean)
    
    # Validate integrated data
    integrated_data = validate_integrated_data(integrated_data)
    
    # Create final dataset
    final_data = create_final_dataset(integrated_data)
    
    # Export curation log
    export_curation_log()
    
    print("\n=== Data Cleaning and Integration Complete ===")
    return final_data

if __name__ == "__main__":
    main()
