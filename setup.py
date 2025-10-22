#!/usr/bin/env python3
"""
Setup script for WorkMate Job Matching Platform
This script helps set up both backend and frontend environments
"""

import os
import sys
import subprocess
import platform

def run_command(command, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error output: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command: {command}")
        print(f"Exception: {e}")
        return False

def check_python():
    """Check if Python is installed"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✅ Python {version.major}.{version.minor}.{version.micro} found")
            return True
        else:
            print(f"❌ Python {version.major}.{version.minor}.{version.micro} found, but Python 3.8+ is required")
            return False
    except Exception as e:
        print(f"❌ Python not found: {e}")
        return False

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} found")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except Exception as e:
        print(f"❌ Node.js not found: {e}")
        return False

def setup_backend():
    """Set up the backend environment"""
    print("\n🔧 Setting up Backend...")
    
    backend_dir = "Backend"
    if not os.path.exists(backend_dir):
        print(f"❌ Backend directory not found: {backend_dir}")
        return False
    
    # Check if virtual environment exists
    venv_path = os.path.join(backend_dir, "venv")
    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        if not run_command("python -m venv venv", cwd=backend_dir):
            return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    print("Installing Python dependencies...")
    if not run_command(f"{pip_cmd} install -r requirements.txt", cwd=backend_dir):
        return False
    
    print("✅ Backend setup completed")
    return True

def setup_frontend():
    """Set up the frontend environment"""
    print("\n🔧 Setting up Frontend...")
    
    frontend_dir = "Frontend"
    if not os.path.exists(frontend_dir):
        print(f"❌ Frontend directory not found: {frontend_dir}")
        return False
    
    print("Installing Node.js dependencies...")
    if not run_command("npm install", cwd=frontend_dir):
        return False
    
    print("✅ Frontend setup completed")
    return True

def test_algorithms():
    """Test the algorithms"""
    print("\n🧪 Testing Algorithms...")
    
    backend_dir = "Backend"
    if platform.system() == "Windows":
        python_cmd = "venv\\Scripts\\python"
    else:
        python_cmd = "venv/bin/python"
    
    if not run_command(f"{python_cmd} test_algorithms.py", cwd=backend_dir):
        print("❌ Algorithm tests failed")
        return False
    
    print("✅ All algorithms are working correctly")
    return True

def main():
    """Main setup function"""
    print("🚀 WorkMate Job Matching Platform Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_python():
        print("\n❌ Please install Python 3.8+ and try again")
        return False
    
    if not check_node():
        print("\n❌ Please install Node.js 16+ and try again")
        return False
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed")
        return False
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed")
        return False
    
    # Test algorithms
    if not test_algorithms():
        print("\n❌ Algorithm tests failed")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Start the backend server:")
    print("   cd Backend")
    if platform.system() == "Windows":
        print("   venv\\Scripts\\activate")
        print("   python app.py")
    else:
        print("   source venv/bin/activate")
        print("   python app.py")
    
    print("\n2. Start the frontend server (in a new terminal):")
    print("   cd Frontend")
    print("   npm run dev")
    
    print("\n3. Open your browser and go to: http://localhost:3000")
    print("\n📖 For more information, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
