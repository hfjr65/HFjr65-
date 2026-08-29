"""
Flask Web Application for HFjr65™ Random Joke Generator
========================================================

Main Flask app with routes for serving jokes and web interface.

Author: Håkon Fløstad Jr. (HFjr65™)
License: MIT
"""

from flask import Flask, render_template, jsonify, request, session
import json
import os
from datetime import datetime
from joke_generator import JokeGenerator

app = Flask(__name__)
app.secret_key = 'hfjr65_secret_key_2026'

# Initialize joke generator
generator = JokeGenerator()

# Simple in-memory storage for demo
joke_history = []
favorites = []

@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html')

@app.route('/api/joke', methods=['GET'])
def get_joke():
    """Get a random joke."""
    api_choice = request.args.get('api', None)
    
    joke = generator.get_random_joke(api_choice)
    
    if joke:
        # Add timestamp
        joke['timestamp'] = datetime.now().isoformat()
        joke_history.append(joke)
        
        # Keep only last 50
        if len(joke_history) > 50:
            joke_history.pop(0)
        
        return jsonify({
            'success': True,
            'joke': joke,
            'total_fetched': len(joke_history)
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Could not fetch joke'
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get joke history."""
    return jsonify({
        'history': joke_history,
        'count': len(joke_history)
    })

@app.route('/api/favorites', methods=['GET', 'POST', 'DELETE'])
def manage_favorites():
    """Manage favorite jokes."""
    if request.method == 'POST':
        joke = request.json
        if joke not in favorites:
            favorites.append(joke)
        return jsonify({'success': True, 'count': len(favorites)})
    
    elif request.method == 'DELETE':
        joke_id = request.json.get('id')
        favorites[:] = [j for j in favorites if j.get('id') != joke_id]
        return jsonify({'success': True, 'count': len(favorites)})
    
    else:  # GET
        return jsonify({
            'favorites': favorites,
            'count': len(favorites)
        })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get application statistics."""
    return jsonify({
        'total_jokes_fetched': len(joke_history),
        'total_favorites': len(favorites),
        'available_apis': list(generator.APIS.keys()),
        'status': 'running'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
