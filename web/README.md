# HFjr65™ Web Application Setup

Quick start for the Flask web app:

## Installation

```bash
cd web
pip install -r requirements_web.txt
```

## Running

```bash
python app.py
```

Then visit: `http://localhost:5000`

## Features

- 🎭 Get random jokes from 3 APIs
- 📋 View history of all jokes
- ⭐ Save favorites
- 📤 Share jokes
- 📊 View statistics

## API Endpoints

- `GET /` - Main page
- `GET /api/joke?api=official` - Get a joke
- `GET /api/history` - Get joke history
- `GET /api/favorites` - Get favorites
- `POST /api/favorites` - Add favorite
- `DELETE /api/favorites` - Remove favorite
- `GET /api/stats` - Get statistics
