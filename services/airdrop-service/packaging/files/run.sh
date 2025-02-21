#!/bin/sh
# Exit immediately if any command fails
set -e

# Optional: perform any pre-start tasks here, e.g., migrations or logging setup

# Start the application
exec python main.py
