import asyncio
from sqlite3 import IntegrityError, OperationalError

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.schemas import ProjectDetailsSchema, ProjectCreateSchema, TaskDetailsSchema
from app.models import Projects, Tasks
from app.services import get_project_tasks

router = APIRouter(prefix="/projects", tags=["Projects"])

# Simulate background tasks using asyncio
async def complete_tasks(project_id: int):
    await asyncio.sleep(10)

    async for session in get_session():
        try:
            result = await session.execute(select(Tasks).where(Tasks.project_id == project_id))
            tasks = result.scalars().all()

            for task in tasks:
                task.status = "complete"

            await session.commit()
        except Exception as e:
            print(f"Error completing tasks for project {project_id}: {e}")
        finally:
            await session.close()


@router.post(
    "/",
    response_model=ProjectDetailsSchema,
    summary="Create a new construction project request."
)
async def create_construction_request(project: ProjectCreateSchema, session: AsyncSession = Depends(get_session)):
    try:
        # Adding new project to DB
        new_project = Projects(
            name=project.project_name, location=project.location, status="processing"
        )
        session.add(new_project)
        await session.commit()
        await session.refresh(new_project)

        # Adding tasks to DB
        tasks_data = await get_project_tasks(project.project_name, project.location)
        tasks = [Tasks(project_id=new_project.id, name=t["name"], status=t["status"]) for t in tasks_data]
        session.add_all(tasks)
        await session.commit()

        # Creating background task
        asyncio.create_task(complete_tasks(new_project.id))  # type: ignore

        return ProjectDetailsSchema(
            id=new_project.id,  # type: ignore
            project_name=new_project.name,  # type: ignore
            location=new_project.location,  # type: ignore
            status=new_project.status,  # type: ignore
            tasks=[TaskDetailsSchema(**t) for t in tasks_data],
        )

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Project creation failed due to integrity error.")
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database operation failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.get(
    "/{project_id}/",
    response_model=ProjectDetailsSchema,
    summary="Retrieve project details."
)
async def retrieve_project_details(project_id: int, session: AsyncSession = Depends(get_session)):
    try:
        # Getting project from DB by ID
        result = await session.execute(select(Projects).where(Projects.id == project_id))
        project = result.scalars().first()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        result = await session.execute(select(Tasks).where(Tasks.project_id == project_id))
        tasks = result.scalars().all()

        return ProjectDetailsSchema(
            id=project.id,
            project_name=project.name,
            location=project.location,
            status=project.status,
            tasks=[TaskDetailsSchema(name=t.name, status=t.status) for t in tasks],
        )
    except OperationalError:
        raise HTTPException(status_code=500, detail="Database error.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")