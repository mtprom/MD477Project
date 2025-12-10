"""
Snakemake workflow for Air Quality & Population Data Curation Project
Automates the complete pipeline from data acquisition to exploratory analysis
"""

configfile: "config.yaml"

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

rule acquire_data:
    input:
        "data/worldcities.csv"
    output:
        "data/top_500_cities.csv"
    log:
        "logs/acquire_data.log"
    shell:
        "python acquire_data.py > {log} 2>&1"

rule collect_air_quality:
    input:
        "data/top_500_cities.csv"
    output:
        validated="data/raw_top_500_cities.csv",
        raw_data=temp("data/raw_air_quality_temp.csv")
    log:
        "logs/full_collection.log"
    shell:
        "python full_collection.py > {log} 2>&1"

rule clean_and_integrate:
    input:
        "data/raw_top_500_cities.csv"
    output:
        final="data/integrated_cities_air_quality_final.csv",
        log_file=temp("data/curation_log_temp.csv")
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
        "python exploratory_analysis.py > {log} 2>&1"
