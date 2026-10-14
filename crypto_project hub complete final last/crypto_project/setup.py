#!/usr/bin/env python3
"""
CryptoHub — Complete Setup & Run Script
Run this once to set up everything:  python setup.py
"""

import os
import sys
import subprocess


def run_cmd(cmd, desc=""):
    print(f"\n▶ {desc or cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr and result.returncode != 0:
        print("⚠ ", result.stderr.strip())
    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        sys.exit(1)
    return result


def main():
    print("\n" + "=" * 55)
    print("  🔐 CryptoHub — Full-Stack Django Setup")
    print("=" * 55)

    # Check Python
    print(f"\n✅ Python {sys.version.split()[0]} detected")

    # Install Django
    print("\n[Step 1] Installing Django...")
    run_cmd("pip install django --break-system-packages -q", "Installing Django")

    # Apply migrations
    print("\n[Step 2] Creating database...")
    run_cmd("python manage.py makemigrations crypto_app", "Making migrations")
    run_cmd("python manage.py migrate", "Applying migrations")

    # Seed data
    print("\n[Step 3] Seeding initial data...")
    run_cmd("python seed_data.py", "Seeding database")

    print("\n" + "=" * 55)
    print("✅ Setup complete! Start the server with:")
    print("   python manage.py runserver")
    print("\n🌐 Open: http://127.0.0.1:8000/")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
