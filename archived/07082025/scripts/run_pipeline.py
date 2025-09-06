#!/usr/bin/env python3
"""
Main script to run the complete chunking pipeline
"""

import os
import sys
import subprocess
from pathlib import Path

def run_phase(phase_name, script_path):
    """Run a specific phase of the pipeline"""
    print(f"\n🚀 Running {phase_name}...")
    print("=" * 60)
    
    try:
        # Run the script from project root
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print(f"✅ {phase_name} completed successfully")
            if result.stdout:
                print("Output:", result.stdout)
        else:
            print(f"❌ {phase_name} failed")
            if result.stderr:
                print("Error:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running {phase_name}: {e}")
        return False
    
    return True

def main():
    """Run the complete pipeline"""
    print("🎯 Contextual Retrieval - Chunking Pipeline")
    print("=" * 60)
    
    # Get the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Phase 1: Rough Chunking
    phase1_script = "pipeline/phase1_rough_chunking/run_tang_chi.py"
    if not run_phase("Phase 1: Rough Chunking", phase1_script):
        print("\n❌ Pipeline failed at Phase 1")
        return
    
    # Phase 2: Agentic Chunking
    phase2_script = "pipeline/phase2_agentic_chunking/run_agentic_chunking.py"
    if not run_phase("Phase 2: Agentic Chunking", phase2_script):
        print("\n❌ Pipeline failed at Phase 2")
        return
    
    print("\n🎉 Pipeline completed successfully!")
    print("\n📁 Results available in:")
    print("   - results/phase1_rough_chunks.txt")
    print("   - results/phase2_agentic_chunks.txt")

if __name__ == "__main__":
    main()
