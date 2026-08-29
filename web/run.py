#!/usr/bin/env python3
"""
Run the Flask web app - make sure you're in the web/ directory first!

Usage:
    python run.py

Then visit: http://localhost:5000
"""

from app import app

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════╗
    ║  🎭 HFjr65™ Joke Generator Web App   ║
    ║                                        ║
    ║  Starting on http://localhost:5000    ║
    ║  Press CTRL+C to stop                 ║
    ╚════════════════════════════════════════╝
    """)
    app.run(debug=True, host='0.0.0.0', port=5000)
