import google.generativeai as genai


GEMINI_API_KEY = "you_api_key"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

async def get_project_tasks(project_name: str, location: str) -> list[dict[str, str]]:
    prompt = f"Generate a list of necessary tasks to build a {project_name} in {location}. Return tasks as a numbered list."

    response = model.generate_content(prompt)

    if hasattr(response, "text") and response.text:
        tasks = [
            {"name": task.strip(), "status": "pending"}
            for task in response.text.split("\n")
            if task.strip()
        ]
        return tasks

    return []
