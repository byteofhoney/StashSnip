# StashSnip 

> I stash my snips! A developer snippet manager built to save, organize and find code fast.

![Python](https://img.shields.io/badge/Python-3.11-brown?style=flat-square)
![Flask](https://img.shields.io/badge/Flask-3.0-orange?style=flat-square)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-amber?style=flat-square)

---

## The Problem

Every developer accumulates dozens of useful code snippets. A regex that finally worked, a MongoDB aggregation pipeline, a Flask decorator you keep rewriting from scratch. They end up scattered across Notion pages, random `.txt` files and old Stack Overflow tabs.

**StashSnip** keeps them in one place tagged, searchable and always one click away.

---

## Features

- Save snippets with title, language, description and tags
- Search by keyword across title and description
- Filter by language or tag
- Syntax highlighting via highlight.js
- Copy to clipboard in one click
- Edit and delete snippets
- Custom delete modal with snippet name confirmation
- Auto dismissing flash messages

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | MongoDB Atlas + PyMongo |
| Frontend | HTML, CSS, Vanilla JS |
| Forms | Flask-WTF |
| Syntax Highlighting | highlight.js |
| Version Control | Git + GitHub |

---

## Interface

> *(coming soon )*

---


## Getting Started

### Prerequisites
- Python 3.11+
- MongoDB Atlas account 

### Setup

```bash
# Clone the repo
git clone https://github.com/byteofhoney/StashSnip.git
cd StashSnip

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your MongoDB URI and secret key

# Run the app
python run.py
```

Visit `http://127.0.0.1:5000`

---

## Environment Variables

| Variable | Description |
|---|---|
| `MONGO_URI` | Your MongoDB Atlas connection string |
| `SECRET_KEY` | Flask secret key for session security |
| `FLASK_ENV` | `development` or `production` |

---

## What I Learned

- Structuring a Flask app using the app factory pattern and Blueprints
- Connecting Flask to MongoDB Atlas using PyMongo
- Building dynamic search and filtering with MongoDB regex queries
- Managing environment variables securely with python-dotenv

---

## License

MIT — see [LICENSE](LICENSE)