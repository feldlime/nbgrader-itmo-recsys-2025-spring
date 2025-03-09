# GitHub Assignment Puller

A Streamlit-based service for automatically pulling student assignments from GitHub repositories.

## Project Structure
```
puller/
├── docker/             # Docker-related files
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── src/               # Source code
│   ├── app.py         # Main Streamlit application
│   ├── config.py      # Configuration management
│   └── github_client.py # GitHub interaction logic
└── tests/             # Test files
    └── test_github_client.py
```

## Testing Locally

1. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r docker/requirements.txt
pip install pytest pytest-asyncio
```

2. Create `.env` file:
```bash
cp docker/.env.example .env
# Edit .env with your GitHub token and repository list
```

3. Run tests:
```bash
pytest tests/
```

4. Run the application:
```bash
PYTHONPATH=. streamlit run src/app.py
```

The app will be available at http://localhost:8501

## Testing with Docker

1. Create `.env` file:
```bash
cp docker/.env.example docker/.env
# Edit docker/.env with your GitHub token and repository list
```

2. Build and run:
```bash
docker build -f docker/Dockerfile -t github-puller .
docker run -p 8501:8501 --env-file docker/.env github-puller
```

The app will be available at http://localhost:8501

## Testing Features

1. GitHub Token Test:
- Open the "Configuration" section
- Click "Test GitHub Token" to verify your token works

2. Manual Repository Pull:
- Each repository has its own card
- Click "Pull Now" to trigger a manual pull

3. Auto-pull:
- The service automatically pulls every 5 minutes (configurable)
- You can see the last pull timestamp for each repository

4. Error Handling:
- Try with an invalid token or repository to test error handling
- Error messages will be displayed in the UI
