import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def load_final_dataset(filepath='data/integrated_cities_air_quality_final.csv'):
    df = pd.read_csv(filepath)
    print(f"Loaded {df.shape[0]} cities")
    return df

def compute_descriptive_statistics(df):
    print("\nDESCRIPTIVE STATISTICS")
    print("-" * 50)
    
    print("\nPopulation:")
    print(df['population'].describe())
    
    df_with_aqi = df[df['aqi'].notna()]
    print("\nAQI:")
    print(df_with_aqi['aqi'].describe())
    
    print("\nAQI by Category:")
    print(df_with_aqi.groupby('aqi_category')['aqi'].describe())
    
    print("\nDominant Pollutants:")
    print(df_with_aqi['dominant_pollutant'].value_counts())
    
    stats_summary = pd.DataFrame({
        'Population': df['population'].describe(),
        'AQI': df_with_aqi['aqi'].describe()
    })
    stats_summary.to_csv('data/descriptive_statistics.csv')
    
    return df_with_aqi

def assess_correlations(df):
    print("\nCORRELATION ANALYSIS")
    print("-" * 50)
    
    numeric_cols = ['population', 'aqi', 'latitude', 'longitude']
    correlation_matrix = df[numeric_cols].corr()
    
    print("\nCorrelation Matrix:")
    print(correlation_matrix)
    
    pop_aqi_corr = df['population'].corr(df['aqi'])
    print(f"\nPopulation vs AQI: {pop_aqi_corr:.4f}")
    
    correlation_matrix.to_csv('data/correlation_matrix.csv')
    
    return correlation_matrix

def create_visualizations(df, output_dir='data/viz'):
    os.makedirs(output_dir, exist_ok=True)
    df_with_aqi = df[df['aqi'].notna()].copy()
    
    print("\nCreating visualizations...")
    
    # A: AQI distribution
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.hist(df_with_aqi['aqi'], bins=30, color='steelblue', alpha=0.7, edgecolor='black')
    plt.xlabel('Air Quality Index (AQI)')
    plt.ylabel('Frequency')
    plt.title('Distribution of AQI Values')
    plt.grid(axis='y', alpha=0.3)
    
    plt.subplot(1, 2, 2)
    df_with_aqi['aqi'].plot(kind='kde', color='steelblue', linewidth=2)
    plt.xlabel('Air Quality Index (AQI)')
    plt.ylabel('Density')
    plt.title('AQI Density Distribution')
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/aqi_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # B: Population distribution
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.hist(df['population']/1e6, bins=30, color='coral', alpha=0.7, edgecolor='black')
    plt.xlabel('Population (Millions)')
    plt.ylabel('Frequency')
    plt.title('Distribution of City Population')
    plt.grid(axis='y', alpha=0.3)
    
    plt.subplot(1, 2, 2)
    (df['population']/1e6).plot(kind='kde', color='coral', linewidth=2)
    plt.xlabel('Population (Millions)')
    plt.ylabel('Density')
    plt.title('Population Density Distribution')
    plt.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/population_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # C: AQI by category
    plt.figure(figsize=(12, 6))
    category_order = df_with_aqi.groupby('aqi_category')['aqi'].median().sort_values().index
    
    sns.boxplot(data=df_with_aqi, x='aqi_category', y='aqi', order=category_order, palette='Set2')
    plt.xlabel('AQI Category')
    plt.ylabel('Air Quality Index (AQI)')
    plt.title('AQI Distribution by Category')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    
    for i, category in enumerate(category_order):
        count = len(df_with_aqi[df_with_aqi['aqi_category'] == category])
        plt.text(i, plt.ylim()[1]*0.95, f'n={count}', ha='center', va='top', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/aqi_by_category.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # D: Population vs AQI scatter
    plt.figure(figsize=(12, 8))
    categories = df_with_aqi['aqi_category'].unique()
    colors = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(categories)))
    
    for i, category in enumerate(sorted(categories)):
        mask = df_with_aqi['aqi_category'] == category
        plt.scatter(df_with_aqi[mask]['population']/1e6, df_with_aqi[mask]['aqi'],
                   label=category, alpha=0.6, s=50, color=colors[i])
    
    z = np.polyfit(df_with_aqi['population'], df_with_aqi['aqi'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(df_with_aqi['population'].min(), df_with_aqi['population'].max(), 100)
    plt.plot(x_trend/1e6, p(x_trend), "r--", alpha=0.8, linewidth=2, label='Trend line')
    
    plt.xlabel('Population (Millions)')
    plt.ylabel('Air Quality Index (AQI)')
    plt.title('Population vs Air Quality Index')
    plt.legend(loc='best')
    plt.grid(alpha=0.3)
    
    corr = df_with_aqi['population'].corr(df_with_aqi['aqi'])
    plt.text(0.05, 0.95, f'Correlation: {corr:.3f}', transform=plt.gca().transAxes,
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/population_vs_aqi.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # G: Geographic distribution
    plt.figure(figsize=(16, 10))
    scatter = plt.scatter(df_with_aqi['longitude'], df_with_aqi['latitude'],
                         c=df_with_aqi['aqi'], s=df_with_aqi['population']/100000,
                         cmap='RdYlGn_r', alpha=0.6, edgecolors='black', linewidth=0.5)
    
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Global Distribution of Cities by Air Quality\n(Size = Population, Color = AQI)')
    
    cbar = plt.colorbar(scatter, label='Air Quality Index (AQI)')
    plt.grid(alpha=0.3, linestyle='--')
    
    legend_sizes = [1e6, 5e6, 10e6, 20e6]
    legend_labels = ['1M', '5M', '10M', '20M']
    legend_handles = [plt.scatter([], [], s=size/100000, c='gray', alpha=0.6, edgecolors='black') 
                     for size in legend_sizes]
    plt.legend(legend_handles, legend_labels, title='Population', loc='lower left')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/geographic_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Done")

def identify_outliers(df):
    print("\nOUTLIERS")
    print("-" * 50)
    
    df_with_aqi = df[df['aqi'].notna()].copy()
    
    print("\nTop 10 by population:")
    top_pop = df.nlargest(10, 'population')[['city', 'country', 'population', 'aqi']]
    print(top_pop.to_string(index=False))
    
    print("\nWorst air quality:")
    top_aqi = df_with_aqi.nlargest(10, 'aqi')[['city', 'country', 'population', 'aqi', 'aqi_category']]
    print(top_aqi.to_string(index=False))
    
    print("\nBest air quality:")
    low_aqi = df_with_aqi.nsmallest(10, 'aqi')[['city', 'country', 'population', 'aqi', 'aqi_category']]
    print(low_aqi.to_string(index=False))
    
    outliers_summary = pd.DataFrame({
        'Metric': ['Highest Population', 'Worst Air Quality', 'Best Air Quality'],
        'City': [top_pop.iloc[0]['city'], top_aqi.iloc[0]['city'], low_aqi.iloc[0]['city']],
        'Country': [top_pop.iloc[0]['country'], top_aqi.iloc[0]['country'], low_aqi.iloc[0]['country']],
        'Value': [top_pop.iloc[0]['population'], top_aqi.iloc[0]['aqi'], low_aqi.iloc[0]['aqi']]
    })
    outliers_summary.to_csv('data/outliers_summary.csv', index=False)

def regional_comparison(df):
    print("\nREGIONAL COMPARISON")
    print("-" * 50)
    
    df_with_aqi = df[df['aqi'].notna()].copy()
    
    print("\nTop 15 countries by average AQI:")
    country_stats = df_with_aqi.groupby('country').agg({
        'aqi': ['mean', 'median', 'std', 'count']
    }).round(2)
    country_stats.columns = ['Mean_AQI', 'Median_AQI', 'Std_AQI', 'City_Count']
    country_stats = country_stats[country_stats['City_Count'] >= 3]
    country_stats = country_stats.sort_values('Mean_AQI', ascending=False).head(15)
    print(country_stats)
    
    country_stats.to_csv('data/regional_comparison.csv')

def main():
    print("EXPLORATORY DATA ANALYSIS")
    print("=" * 50)
    
    df = load_final_dataset()
    df_with_aqi = compute_descriptive_statistics(df)
    correlation_matrix = assess_correlations(df_with_aqi)
    create_visualizations(df)
    identify_outliers(df)
    regional_comparison(df)
    
    print("\nDone. Files saved to data/")

if __name__ == "__main__":
    main()
