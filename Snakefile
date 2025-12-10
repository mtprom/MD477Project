"""
Snakemake workflow for Air Quality & Population Data Curation Project
Automates the complete pipeline from data acquisition to exploratory analysis

NOTE: For grading/reproduction without API key, the workflow skips API collection
and uses pre-collected data files that should be included in the repository.
"""

configfile: "config.yaml"

# Default rule - runs everything using pre-collected data
rule all:
    input:
        "data/integrated_cities_air_quality_final.csv",
        "data/descriptive_statistics.csv",
        "data/correlation_matrix.csv",
        "data/outliers_summary.csv",
        "data/regional_comparison.csv",
        "data/viz/aqi_distribution.png",
        "data/viz/population_distribution.png",
        "data/viz/aqi_by_category.png",
        "data/viz/population_vs_aqi.png",
        "data/viz/geographic_distribution.png"

# Optional: Full pipeline including API collection (requires API key)
rule all_with_api:
    input:
        "data/top_500_cities.csv",
        "data/raw_top_500_cities.csv",
        "data/integrated_cities_air_quality_final.csv",
        "data/descriptive_statistics.csv",
        "data/correlation_matrix.csv",
        "data/outliers_summary.csv",
        "data/regional_comparison.csv",
        "data/viz/aqi_distribution.png",
        "data/viz/population_distribution.png",
        "data/viz/aqi_by_category.png",
        "data/viz/population_vs_aqi.png",
        "data/viz/geographic_distribution.png"

rule acquire_data:
    input:
        "data/worldcities.csv"
    output:
        "data/top_500_cities.csv"
    log:
        "logs/acquire_data.log"
    shell:
        "python acquire_data.py > {log} 2>&1"

# This rule requires API key - only run if explicitly requested
rule collect_air_quality:
    input:
        "data/top_500_cities.csv"
    output:
        "data/raw_top_500_cities.csv"
    log:
        "logs/full_collection.log"
    shell:
        "python full_collection.py > {log} 2>&1"

rule clean_and_integrate:
    input:
        "data/raw_top_500_cities.csv"
    output:
        "data/integrated_cities_air_quality_final.csv"
    log:
        "logs/clean_and_integrate.log"
    shell:
        "python clean_and_integrate.py > {log} 2>&1"

rule exploratory_analysis:
    input:
        "data/integrated_cities_air_quality_final.csv"
    output:
        stats="data/descriptive_statistics.csv",
        corr="data/correlation_matrix.csv",
        outliers="data/outliers_summary.csv",
        regional="data/regional_comparison.csv",
        viz1="data/viz/aqi_distribution.png",
        viz2="data/viz/population_distribution.png",
        viz3="data/viz/aqi_by_category.png",
        viz4="data/viz/population_vs_aqi.png",
        viz5="data/viz/geographic_distribution.png"
    log:
        "logs/exploratory_analysis.log"
    shell:
        "python analysis_and_viz.py > {log} 2>&1"
