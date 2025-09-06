#!/usr/bin/env python3
"""
Script to run agentic chunking using the existing agentic_chunker.py
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Run agentic chunking using the existing script"""
    print("Starting agentic chunking process...")
    print("-" * 60)
    
    try:
        # Get the current directory
        current_dir = Path(__file__).parent
        
        # Run the existing agentic_chunker.py
        print("Running existing agentic_chunker.py...")
        result = subprocess.run([sys.executable, "agentic_chunker.py"], 
                              cwd=current_dir, 
                              capture_output=True, 
                              text=True, 
                              encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ Agentic chunking completed successfully")
            if result.stdout:
                print("Output:", result.stdout)
        else:
            print("❌ Agentic chunking failed")
            if result.stderr:
                print("Error:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running agentic chunking: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main()
