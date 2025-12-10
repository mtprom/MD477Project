import os
import sys
from datetime import datetime

def run_script(script_name):
    print(f"\n{'='*60}")
    print(f"Running {script_name}")
    print('='*60)
    result = os.system(f"python {script_name}")
    if result != 0:
        print(f"\nError running {script_name}")
        sys.exit(1)
    print(f"\n✓ {script_name} completed successfully")

def main():
    print("\nAIR QUALITY & POPULATION DATA PIPELINE")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    os.makedirs('data', exist_ok=True)
    os.makedirs('data/viz', exist_ok=True)
    os.makedirs('logs', exist_ok=True)
    
    if len(sys.argv) > 1 and sys.argv[1] == '--skip-collection':
        print("\nSkipping data collection (using existing data)")
        skip = True
    else:
        print("\nRunning full pipeline (including API collection)")
        skip = False
    
    if not skip:
        run_script("acquire_data.py")
        run_script("full_collection.py")
    
    run_script("clean_and_integrate.py")
    run_script("exploratory_analysis.py")
    
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
