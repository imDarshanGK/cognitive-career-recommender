#!/usr/bin/env python3
"""
Quick Setup Script for Cognitive Career AI
Automates the initial setup process
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def create_env_file():
    """Create .env file with default values"""
    env_content = """# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_APP=app.py
FLASK_ENV=development

# Database Configuration
DATABASE_URL=sqlite:///cognitive_career_ai.db

# Email Configuration (Gmail example)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@cognitivecareer.ai

# Application Configuration
APP_NAME=Cognitive Career AI
BASE_URL=http://localhost:5000

# Development Settings
DEBUG=True
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ Created .env file with default configuration")

def setup_project():
    """Main setup function"""
    print("🚀 Setting up Cognitive Career AI...")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Create virtual environment
    if not Path("venv").exists():
        if not run_command("python -m venv venv", "Creating virtual environment"):
            sys.exit(1)
    else:
        print("✅ Virtual environment already exists")
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        print("⚠️  Some dependencies may have failed. Try installing manually:")
        print(f"   {pip_cmd} install -r requirements.txt")
    
    # Create .env file if it doesn't exist
    if not Path(".env").exists():
        create_env_file()
    else:
        print("✅ .env file already exists")
    
    # Create necessary directories
    directories = [
        "frontend/static/uploads/avatars",
        "frontend/static/uploads/resumes",
        "backend_new/logs",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    print("✅ Created necessary directories")
    
    # Initialize database
    print("\n🔄 Setting up database...")
    try:
        # Import here to avoid import issues
        from app import create_app
        from backend_new.models.database import db
        
        app = create_app()
        with app.app_context():
            db.create_all()
            print("✅ Database tables created")
            
            # Create admin user
            print("\n👤 Creating admin user...")
            from backend_new.models.database import db_manager
            admin = db_manager.create_admin_user(
                email='admin@cognitivecareer.ai',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            print("✅ Admin user created (email: admin@cognitivecareer.ai, password: admin123)")
            print("⚠️  Please change the admin password after first login!")
            
    except Exception as e:
        print(f"❌ Database setup failed: {str(e)}")
        print("You can set it up manually later with: python app.py init-db")
    
    # Setup completion
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📝 Next steps:")
    print("1. Activate virtual environment:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    
    print("\n2. Configure email settings in .env file")
    print("   - Update MAIL_USERNAME and MAIL_PASSWORD")
    print("   - For Gmail, use an app-specific password")
    
    print("\n3. Run the application:")
    print("   python app.py")
    
    print("\n4. Open your browser and go to:")
    print("   http://localhost:5000")
    
    print("\n5. Login with admin account:")
    print("   Email: admin@cognitivecareer.ai")
    print("   Password: admin123")
    print("   (Change this password immediately!)")
    
    print("\n📚 Additional commands:")
    print("   python app.py init-db     # Initialize database")
    print("   python app.py reset-db    # Reset database")
    print("   python app.py seed-db     # Add sample data")
    print("   python app.py create-admin # Create admin user")
    print("   python app.py test-email   # Test email configuration")
    
    print("\n🔧 Configuration files:")
    print("   .env                      # Environment variables")
    print("   requirements.txt          # Python dependencies")
    print("   README_FRONTEND.md        # Frontend documentation")

if __name__ == "__main__":
    try:
        setup_project()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {str(e)}")
        sys.exit(1)