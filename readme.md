
# EGPT Local Development Guide

This guide explains how to run and test the `utility_functions` and `utility_services` modules locally for EGPT, so future developers can get started quickly.

---


## Prerequisites (What You Actually Need)

- **Python 3.9+** (for running scripts and services)
- **Docker** (recommended for running the main app and agents)
- **.env file** (with all required environment variables; see below for examples)
- **egpt.env** (for Docker local testing, copy to `local_testing/`)
- **Google Cloud credentials** (if using Firestore or GCP features; put your `credentials.json` in `var/secrets/google/`)
- **MongoDB** (if using MongoDB as your database; can be local or remote)
- **Redis** (if you want to use caching; optional, only if your config uses it)

**Folder structure quick reference:**
- `utility_functions/` — core utility scripts and agents
- `utility_services/` — services like embedding model management
- `local_testing/` — for local Docker/dev setup
- `var/secrets/google/` — put your GCP credentials here

**In short:**
You need Python, Docker, a filled-out `.env`, and (if using GCP) your credentials in the right folder. MongoDB/Redis are only needed if your config uses them.

---

## 1. Clone the Repository

```sh
git clone <your-repo-url>
cd EGPT/EGPT_AI
```

---


## 2. Set Up for Local Docker Development

The recommended way to run and test EGPT locally is using Docker. Follow these steps:

### a. Prepare Environment Files

1. **Copy your environment file:**
   - Copy `egpt.env` into the `local_testing/` directory.
     ```sh
     cp egpt.env local_testing/
     ```
2. **Copy your Google credentials:**
   - Place your `credentials.json` inside `var/secrets/google/`.
     ```sh
     cp path/to/your/credentials.json var/secrets/google/
     ```

### b. Update Code for Local Testing

1. **Edit `server.py`:**
   - Add `import logging.config` at line 33.
   - Comment or uncomment any `# FIXME` lines as needed for local testing (see code comments for guidance).

### c. Build and Run Docker Image

1. **Build the Docker image:**
   ```sh
   sudo docker build -t egpt_ai .
   ```
2. **Run the Docker container:**
   ```sh
   sudo docker run -p 5001:5001 egpt_ai
   ```

This will start the EGPT service locally on port 5001. You can now test endpoints and utility functions via the running container.

---

---

## 3. Configure Environment Variables

Create a `.env` file in the project root (or use `agent.env` as referenced in `Config.py`).

**Example:**
```env
ENV=local
USE_DATABASE=mongo                # or 'firestore'
MONGO_URL=mongodb://localhost:27017
MONGO_DB=egpt_db
MONGO_CONNECTION_STRING=mongodb://localhost:27017
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
PUBSUB_PROJECT_ID=your-gcp-project
PUBSUB_MAIN_STREAMING_TOPIC_ID=your-topic
# ...add any other required variables from Config.py
```

---

## 4. Start Supporting Services

- **MongoDB:**
  - Make sure MongoDB is running locally or accessible via the URI in your config.
- **Redis:**
  - Start Redis if your code uses caching.
- **Firestore:**
  - If using Firestore, ensure you have the correct Google credentials and the Firestore emulator or a real GCP project.

---

## 5. Running Utility Functions/Services

### a. Testing Utility Functions


You can run and test utility functions by creating your own `test.py` script in the `utility_functions` folder. Here’s how:

1. **Create a file named `test.py` inside the `utility_functions` directory.**
2. **Try using the working functions like the following example code into it:**

```python
from utils.utils_no_sql_interface import NoSQLInterface
import Config

def test_agent_fetch():
    db = NoSQLInterface(database_name=Config.MONGODB_NAME)
    agent = db.find_one("agents", {"_id": "some_agent_id"})
    print(agent)

if __name__ == "__main__":
    test_agent_fetch()
```

3. **Run your test script:**

```sh
cd utility_functions
python test.py
```

- Make sure your test script imports and uses the correct interfaces (e.g., `NoSQLInterface`).
- You can also use `pytest` for more formal testing.

### b. Running Agent Services

Each agent (in `utility_functions/agents/<agent_name>/run.py`) can be run as a Flask app:

```sh
cd utility_functions/agents/<agent_name>
python run.py
```

- This will start a local server (usually on `localhost:5000` or as configured).
- You can send HTTP requests to test the agent endpoints.

### c. Testing Utility Services
---

## Running and Testing `utility_services/embedding_model_service`

To run the Embedding Model Service locally:

1. **Set up your `.env` file** (in the project root or `utility_services/embedding_model_service/`):

```env
ENV=dev
GOOGLE_APPLICATION_CREDENTIALS="var/secrets/google/my-credentials.json"
MODEL_MANAGEMENT_API=http://0.0.0.0:5002
MODEL_INFERENCE_API=http://0.0.0.0:5001
MODEL_STORE_FOLDER=model-artifacts
STORAGE_BUCKET_NAME="dev-llms-embedding-models"
MONGO_CONNECTION_STRING=""
MONGODB_DB_NAME=""
MONGODB_EMBEDDING_MODEL_COLLECTION_NAME="embedding-models"
```

2. **Run the service:**

```sh
cd utility_services/embedding_model_service
python server.py
```

3. **Test the endpoints:**
   - Use Postman, curl, or any API client to send requests to the endpoints (e.g., `http://localhost:5004/embedding_model_service/custom_management/get_embeddings`).
   - Refer to the Swagger docs at `/embedding_model_service/custom_management/apidocs/` for endpoint details.

---

## 6. Switching Databases

To switch between MongoDB and Firestore, change the `USE_DATABASE` variable in your `.env`:

```env
USE_DATABASE=mongo      # for MongoDB
USE_DATABASE=firestore  # for Firestore
```

Restart your service after changing this value.

---

## 7. Debugging Tips

- **Import Errors:**
  - Use absolute imports (e.g., `from utils.utils_no_sql_interface import NoSQLInterface`) when running scripts directly.
- **Environment Variables:**
  - If you see missing config errors, double-check your `.env` and that it's loaded before running scripts.
- **Database Connection:**
  - Ensure your DB services are running and accessible from your machine.
- **Logs:**
  - Check the logs for messages about which database is being used and for any connection errors.

---

## 8. Example: Testing a Utility Function

```python
# utility_functions/test.py
from utils.utils_no_sql_interface import NoSQLInterface
import Config

def test_agent_fetch():
    db = NoSQLInterface(database_name=Config.MONGODB_NAME)
    agent = db.find_one("agents", {"_id": "some_agent_id"})
    print(agent)

if __name__ == "__main__":
    test_agent_fetch()
```

Run with:
```sh
python utility_functions/test.py
```

---

## 9. Useful Commands

- **Install dependencies:**  `pip install -r requirements.txt`
- **Run a test script:**     `python utility_functions/test.py`
- **Run an agent service:**  `python utility_functions/agents/email_agent/run.py`
- **Run a utility service:** `python utility_services/embedding_model_service/run.py`

---

## 10. Troubleshooting

- **ModuleNotFoundError:**
  - Make sure you are running scripts from the project root or use `PYTHONPATH=.`.
- **Database not connecting:**
  - Check your URI, credentials, and that the service is running.
- **Config not loading:**
  - Ensure `.env` is present and loaded (use `python-dotenv` if needed).

---

## 11. Contributing

- Follow the existing code structure.
- Use the `NoSQLInterface` for all database operations.
- Add new configs to `.env` and `Config.py` as needed.
- Write tests in `test.py` or with `pytest`.

---

**Start Testing! Varshith Krishna**
