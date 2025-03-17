# Construction AI Backend

This project is a FastAPI-based microservice that simulates an AI-powered construction task manager. Designed as a solution for a 24-hour coding challenge, it leverages the Gemini Pro Free Tier API to generate construction project tasks dynamically, stores project and task data in an SQLite database, and provides a RESTful API for managing construction projects. The service also includes a background process to simulate task completion, enhancing its functionality beyond the core requirements.

Key features:

- Accepts construction project requests (e.g., "Build a restaurant in San Francisco").
- Uses Gemini API to generate a list of required tasks.
- Stores and retrieves project data using SQLite and SQLAlchemy.
- Exposes API endpoints for creating and retrieving projects.
- Simulates task completion in the background using asyncio.

## Setup Instructions

### Requirements

Ensure you have Python 3.13 installed.

1. Clone the repository:

   ```sh
   git clone https://github.com/UnwreckerNick/construction_ai.git
   cd construction_ai
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the application:

   ```sh
   uvicorn app.main:app --reload
   ```

5. Access the API documentation at:

   - OpenAPI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Database Setup (SQLite)

The application uses SQLite as the database.

1. The database file is automatically created in the project directory.
2. To apply migrations, use:

   ```sh
   alembic upgrade head
   ```

## API Usage Examples

### Create a Project

```sh
curl -X POST "http://127.0.0.1:8000/projects/" \
     -H "Content-Type: application/json" \
     -d '{"project_name": "Mall", "location": "New York"}'
```

### Get Project by ID

```sh
curl -X GET "http://127.0.0.1:8000/projects/1"
```

### Run Tests

To execute the test suite:

```sh
pytest -v
```

## Example Response

A successful request to retrieve a project will return a JSON response in the following format.
### Request:
```json
{
  "project_name": "Mall",
  "location": "New York"
}
```
### Response:
```json
{
  "id": 1,
  "project_name": "Mall",
  "location": "New York",
  "status": "processing",
  "tasks": [
    {
      "name": "Okay, here's a numbered list of necessary tasks to build a mall in New York City...",
      "status": "pending"
    },
    {
      "name": "**I. Pre-Construction & Planning:**",
      "status": "pending"
    },
    {
      "name": "1. **Market Research & Feasibility Study:** Analyze demographics, consumer spending habits...",
      "status": "pending"
    }
    ...
  ]
}
