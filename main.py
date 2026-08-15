import subprocess
import sys
import os

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    print("Launching AI Product Manager Copilot Application...")
    subprocess.run([sys.executable, "-m", "streamlit", "run", "frontend/app.py"])

if __name__ == "__main__":
    main()