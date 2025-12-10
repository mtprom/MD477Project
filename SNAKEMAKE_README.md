# Snakemake Workflow

This workflow automates the data pipeline from cleaning through analysis.

## For Grading (No API Key Required)

The workflow uses pre-collected data files included in the repo, so no API key is needed.

**Quick start:**
```bash
pip install -r requirements.txt
pip install snakemake
snakemake --cores 1
```

This runs data cleaning, integration, and generates all analysis outputs.

## What's Included

Pre-collected data files in the repo:
- `data/worldcities.csv`
- `data/raw_top_500_cities.csv`
- `data/raw_air_quality_*.csv`

## Running the Workflow

Basic run:
```bash
snakemake --cores 1
```

See what will run without executing:
```bash
snakemake -n
```

Run with full output:
```bash
snakemake --cores 1 --verbose
```

Force re-run everything:
```bash
snakemake --cores 1 --forceall
```

## Workflow Steps

1. `acquire_data` - Selects top 500 cities from SimpleMaps data
2. `collect_air_quality` - Gets air quality data from Google API (skipped by default)
3. `clean_and_integrate` - Cleans and merges datasets
4. `exploratory_analysis` - Generates statistics and visualizations

## Output Files

Data:
- `data/integrated_cities_air_quality_final.csv`
- `data/descriptive_statistics.csv`
- `data/correlation_matrix.csv`
- `data/outliers_summary.csv`
- `data/regional_comparison.csv`

Visualizations:
- `data/viz/aqi_distribution.png`
- `data/viz/population_distribution.png`
- `data/viz/aqi_by_category.png`
- `data/viz/population_vs_aqi.png`
- `data/viz/geographic_distribution.png`

Logs:
- `logs/acquire_data.log`
- `logs/clean_and_integrate.log`
- `logs/exploratory_analysis.log`

## Running Specific Parts

Just the cleaning:
```bash
snakemake data/integrated_cities_air_quality_final.csv --cores 1
```

Just the analysis:
```bash
snakemake data/descriptive_statistics.csv --cores 1
```

## With API Key (Optional)

If you have a Google Air Quality API key and want to collect fresh data:

1. Copy `config_template.py` to `config.py` and add your API key
2. Run: `snakemake all_with_api --cores 1`

## Troubleshooting

Missing input files:
```bash
ls data/worldcities.csv
ls data/raw_top_500_cities.csv
```

Create directories if needed:
```bash
mkdir -p data/viz logs
```

Delete output and re-run:
```bash
rm data/integrated_cities_air_quality_final.csv
snakemake --cores 1
```

## Cleanup

Remove all generated files:
```bash
snakemake --delete-all-output
```
