from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import parse_obj_as

from models import Activity, Course, CourseResponse, Event, Room
from scraper import scrapeCourseAct


app = FastAPI()


async def init():
    # Create Motor client
    client = AsyncIOMotorClient("mongodb://root:example@mongo:27017")

    # Init beanie with the Product document class
    await init_beanie(database=client.tpapi, document_models=[Course])


@app.get("/")
def root():
    return "Hello world from fapi!"


@app.get("/fetch")
async def fetch():
    await init()
    courses = []
    data = scrapeCourseAct()
    for c in data.allCourseTermin:
        courses.append(
            Course(
                **c.dict(exclude={"id", "courseid", "terminnr"}),
                course_id=c.courseid,
                slug=c.id,
            )
        )
    await Course.insert_many(courses)

    return {"Success": "Updated courses"}


@app.get("/courses")
async def courses():
    await init()

    courses = await Course.find_all().project(CourseResponse).to_list()

    return courses


@app.get("/course/{course_id}")
async def course(course_id: str):
    await init()
    course = await Course.find_one(Course.course_id == course_id)
    if not course.activities_fetched:
        data = scrapeCourseAct(courses=[course.course_id])
        for activity in data.allActivities:
            course.activities.append(
                Activity(
                    **activity.dict(exclude={"padnum", "courseid", "id"}),
                    activityid=activity.id,
                )
            )
            course.activities_fetched = True
            await course.save()

    if not course.timetable_fetched:
        data = scrapeCourseAct(
            courses=[course.course_id],
            activities=[activity.activityid for activity in course.activities],
            timetable=True,
        )
        course.events = [
            Event(
                **element.dict(
                    exclude={
                        "eventid",
                        "resources",
                        "room",
                        "editurl",
                        "courseid",
                        "aid",
                    }
                ),
                room=parse_obj_as(list[Room] | None, element.room),
            )
            for element in data
        ]
        course.timetable_fetched = True
        await course.save()

    return parse_obj_as(CourseResponse, course)
