# Construction AI Backend

This is the backend service for the Construction AI project, built using FastAPI and SQLite.

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

### Get All Projects

```sh
curl -X GET "http://127.0.0.1:8000/projects/"
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
