"""
Air Quality Collection Script
Collects air quality data for a sample of cities from the Google Air Quality API
"""

import pandas as pd
import numpy as np
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
from config_template import API_KEY, BASE_URL
import time
from datetime import datetime

def load_top_cities(filepath='data/top_500_cities.csv'):
    """Load top 500 cities from Week 1"""
    top_cities = pd.read_csv(filepath)
    print(f"Loaded {len(top_cities)} cities")
    print(f"Columns: {top_cities.columns.tolist()}")
    print("\nFirst 5 cities:")
    print(top_cities[['city', 'country', 'lat', 'lng', 'population']].head())
    return top_cities

def get_current_air_quality(lat, lon, api_key):
    """Get current air quality for given coordinates"""
    url = f"{BASE_URL}currentConditions:lookup"
    params = {"key": api_key}
    data = {
        "location": {
            "latitude": lat,
            "longitude": lon
        }
    }
    
    try:
        response = requests.post(url, params=params, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status code: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def collect_sample_air_quality(top_cities, sample_size=50):
    """Collect air quality data for sample cities"""
    sample_cities = top_cities.head(sample_size).copy()
    air_quality_data = []
    
    for idx, row in sample_cities.iterrows():
        city_name = row['city']
        lat = row['lat']
        lon = row['lng']
        
        if idx % 10 == 0:
            print(f"Processing city {idx+1}/{sample_size}: {city_name}")
        
        result = get_current_air_quality(lat, lon, API_KEY)
        
        # Extract AQI value if available
        aqi = None
        category = None
        
        if 'indexes' in result and len(result['indexes']) > 0:
            aqi = result['indexes'][0].get('aqi', None)
            category = result['indexes'][0].get('category', None)
        
        air_quality_data.append({
            'city': city_name,
            'lat': lat,
            'lon': lon,
            'aqi': aqi,
            'category': category,
            'timestamp': datetime.now().isoformat()
        })
        
        # Rate limiting
        time.sleep(0.5)
    
    print(f"\nCompleted! Collected data for {len(air_quality_data)} cities")
    return air_quality_data

def create_integrated_dataset(sample_cities, air_quality_data):
    """Combine population data with air quality data"""
    aq_df = pd.DataFrame(air_quality_data)
    
    integrated_data = sample_cities.merge(
        aq_df[['city', 'aqi', 'category', 'timestamp']], 
        on='city', 
        how='left'
    )
    
    print(f"Shape: {integrated_data.shape}")
    print(f"\nColumns: {integrated_data.columns.tolist()}")
    print(integrated_data[['city', 'country', 'population', 'aqi', 'category']].head())
    
    return integrated_data

def check_data_quality(integrated_data):
    """Check data quality of integrated dataset"""
    print(f"Total cities: {len(integrated_data)}")
    print(f"AQI data: {integrated_data['aqi'].notna().sum()}")
    print(f"missing AQI data: {integrated_data['aqi'].isna().sum()}")
    print(integrated_data['aqi'].describe())

def save_integrated_data(integrated_data, filepath='data/integrated_cities_aqi.csv'):
    """Save integrated dataset"""
    integrated_data.to_csv(filepath, index=False)
    print(f"Saved integrated dataset to {filepath}")

def create_visualization(integrated_data, output_dir='data/viz'):
    """Create initial exploratory visualization"""
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    clean_data = integrated_data.dropna(subset=['aqi'])
    print(f"Working with {len(clean_data)} cities with complete data")
    
    # Box plot: AQI by category
    plt.figure(figsize=(10, 6))
    clean_data.boxplot(column='aqi', by='category', figsize=(10, 6))
    plt.xlabel('AQI Category')
    plt.ylabel('Air Quality Index')
    plt.title('AQI Distribution by Category')
    plt.suptitle('')  # Remove default title
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    output_path = f'{output_dir}/aqi_by_category.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {output_path}")
    plt.close()

def main():
    """Main execution function"""
    print("=== Air Quality Collection Script ===\n")
    
    # Load top cities
    top_cities = load_top_cities()
    
    # Collect sample data (50 cities for testing)
    sample_size = 50
    air_quality_data = collect_sample_air_quality(top_cities, sample_size)
    
    # Create integrated dataset
    sample_cities = top_cities.head(sample_size).copy()
    integrated_data = create_integrated_dataset(sample_cities, air_quality_data)
    
    # Check quality
    check_data_quality(integrated_data)
    
    # Save
    save_integrated_data(integrated_data)
    
    # Create visualization
    create_visualization(integrated_data)
    
    print("\n=== Air Quality Collection Complete ===")

if __name__ == "__main__":
    main()
