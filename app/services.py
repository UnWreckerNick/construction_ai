import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

async def get_project_tasks(project_name: str, location: str) -> list[dict[str, str]]:
    prompt = f"Generate a list of necessary tasks to build a {project_name} in {location}. Return tasks as a numbered list."

    try:
        response = model.generate_content(prompt)

        if not hasattr(response, "text") or not response.text:
            raise ValueError("Empty response from AI model.")

        tasks = [
            {"name": task.strip(), "status": "pending"}
            for task in response.text.split("\n")
            if task.strip()
        ]

        if not tasks:
            raise ValueError("AI returned no valid tasks.")

        return tasks

    except GoogleAPIError as e:
        print(f"Google API error: {e}")
        return []
    except ValueError as e:
        print(f"Data processing error: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in AI processing: {e}")
        return []