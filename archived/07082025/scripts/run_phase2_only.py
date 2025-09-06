#!/usr/bin/env python3
"""
Script to run only Phase 2: Agentic Chunking
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    """Run only Phase 2: Agentic Chunking"""
    print("🎯 Running Phase 2: Agentic Chunking Only")
    print("=" * 60)
    
    try:
        # Get the project root directory
        project_root = Path(__file__).parent.parent
        
        # Path to Phase 2 script
        phase2_script = project_root / "pipeline" / "phase2_agentic_chunking" / "run_agentic_chunking.py"
        
        if not phase2_script.exists():
            print(f"❌ Phase 2 script not found: {phase2_script}")
            return False
        
        print(f"📁 Project root: {project_root}")
        print(f"🚀 Phase 2 script: {phase2_script}")
        print("-" * 60)
        
        # Run Phase 2
        print("Starting Phase 2: Agentic Chunking...")
        result = subprocess.run([sys.executable, str(phase2_script)], 
                              cwd=project_root, 
                              capture_output=True, 
                              text=True, 
                              encoding='utf-8')
        
        if result.returncode == 0:
            print("\n✅ Phase 2: Agentic Chunking completed successfully!")
            if result.stdout:
                print("\n📋 Output:")
                print(result.stdout)
        else:
            print("\n❌ Phase 2: Agentic Chunking failed!")
            if result.stderr:
                print("\n🚨 Error:")
                print(result.stderr)
            return False
            
    except Exception as e:
        print(f"\n❌ Error running Phase 2: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Phase 2 completed successfully!")
        print("📁 Check results in: results/phase2_agentic_chunks.txt")
    else:
        print("\n💥 Phase 2 failed!")
        sys.exit(1)
