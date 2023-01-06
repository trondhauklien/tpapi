from fastapi import FastAPI
from mongoengine import connect

from models import Activity, Course, CourseResponse, Event
from scraper import scrapeCourseAct


app = FastAPI()

connect("tp_scraper", host="mongodb://root:example@mongo:27017")


URL = "https://tp.educloud.no/ntnu/timeplan"


@app.get("/")
def root():
    return "Hello world from fapi!"


@app.get("/fetch")
def fetch():
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
    Course.objects.insert(courses, load_bulk=False)

    return {"Success": "Updated courses"}


@app.get("/courses")
def courses():
    courses = Course.objects.all()
    response = []
    for course in courses:
        response.append(CourseResponse(**course.to_mongo()))
    return response


@app.get("/course/{course_id}")
def course(course_id: str):
    course = Course.objects(course_id=course_id).first()
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
            course.save()

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
                )
            )
            for element in data
        ]
        course.timetable_fetched = True
        course.save()

    return CourseResponse(**course.to_mongo())
