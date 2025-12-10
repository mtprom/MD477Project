"""
Data Acquisition Script
Loads SimpleMaps World Cities dataset and identifies top 500 cities by population
"""

import pandas as pd
import numpy as np
import requests
import json
from config_template import API_KEY, BASE_URL

def load_cities_data(filepath='data/worldcities.csv'):
    """Load SimpleMaps World Cities dataset"""
    cities_df = pd.read_csv(filepath)
    print(f"Successfully loaded {len(cities_df)} cities from SimpleMaps dataset")
    print(f"Dataset shape: {cities_df.shape}")
    print(f"Columns: {cities_df.columns.tolist()}")
    return cities_df

def explore_cities_data(cities_df):
    """Explore the dataset structure"""
    print("First 5 rows:")
    print(cities_df.head())
    
    print("\nDataset info:")
    cities_df.info()
    
    print("\nBasic statistics:")
    print(cities_df.describe())
    
    return cities_df

def check_data_quality(cities_df):
    """Check missing values and data quality"""
    print("Missing values per column:")
    print(cities_df.isnull().sum())
    
    print("\nUnique countries:")
    print(f"Total countries: {cities_df['country'].nunique()}")
    print(cities_df['country'].value_counts().head(10))
    
    print("\nPopulation statistics:")
    print(f"Cities with population data: {cities_df['population'].notna().sum()}")
    print(f"Cities without population data: {cities_df['population'].isna().sum()}")
    
    return cities_df

def select_top_cities(cities_df, n=500):
    """Select top N cities by population"""
    cities_with_pop = cities_df.dropna(subset=['population'])
    top_cities = cities_with_pop.nlargest(n, 'population')
    
    print(f"Population range: {top_cities['population'].min():,.0f} to {top_cities['population'].max():,.0f}")
    print("\nTop 10 most populous cities:")
    print(top_cities[['city', 'country', 'population']].head(10))
    
    return top_cities

def save_top_cities(top_cities, filepath='data/top_500_cities.csv'):
    """Save top cities to CSV"""
    top_cities.to_csv(filepath, index=False)
    print(f"\nSaved top {len(top_cities)} cities to {filepath}")

def test_api_connection():
    """Test basic API connectivity"""
    print(f"API Base URL: {BASE_URL}")
    print(f"API Key configured: {API_KEY[:10]}...")
    print("API configuration complete")
    return True

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

def main():
    """Main execution function"""
    print("=== Data Acquisition Script ===\n")
    
    # Load data
    cities_df = load_cities_data()
    
    # Explore data
    explore_cities_data(cities_df)
    
    # Check quality
    check_data_quality(cities_df)
    
    # Select top 500
    top_500 = select_top_cities(cities_df, n=500)
    
    # Save
    save_top_cities(top_500)
    
    # Test API
    test_api_connection()
    
    # Test sample API call
    print("\nTesting API with Pittsburgh coordinates...")
    sample_result = get_current_air_quality(40.4387, -79.9972, API_KEY)
    
    if 'error' in sample_result:
        print(f"API Error: {sample_result['error']}")
    else:
        print("API Response received successfully!")
        print(f"Response keys: {list(sample_result.keys())}")
        
        if 'indexes' in sample_result:
            for index in sample_result['indexes']:
                print(f"Index: {index.get('displayName', 'Unknown')}")
                print(f"AQI: {index.get('aqi', 'N/A')}")
                print(f"Category: {index.get('category', 'N/A')}")
    
    print("\n=== Data Acquisition Complete ===")

if __name__ == "__main__":
    main()
