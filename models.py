from datetime import datetime

from beanie import Document, Indexed
from pydantic import BaseModel, Field


class Activity(BaseModel):
    activityid: str
    name: str
    name_en: str | None
    name_nn: str | None
    coursetype: str


class Room(BaseModel):
    roomid: str
    roomurl: str
    campusid: str
    roomname: str
    videolink: str
    buildingid: str
    buildingurl: str
    roomacronym: str
    buildingname: str
    showforstudent: bool
    buildingacronym: str
    equipment_function: str | None


class Event(BaseModel):
    semesterid: str
    weeknr: int
    dtstart: datetime
    dtend: datetime
    lopennr: int | None
    teaching_method: str
    teaching_method_name: str
    teaching_title: str
    summary: str
    studentgroups: list[str] | None
    room: list[Room] | None
    terminnr: int
    status: str
    active: bool
    compulsory: bool
    coursetype: str
    virtual_course_name: str | None
    weeknumberid: int
    resources: list[str] | None
    weekday: int
    multiday: bool


class Course(Document):
    course_id: str = Field(indexed=True)
    slug: str
    name: str
    name_en: str | None
    name_nn: str | None
    activities_fetched: bool = False
    activities: list[Activity | None] = []
    timetable_fetched: bool = False
    events: list[Event | None] = []


class ActivityResponse(BaseModel):
    activityid: str
    name: str
    coursetype: str


class RoomResponse(BaseModel):
    roomurl: str
    roomname: str
    buildingname: str
    campusid: str


class EventResponse(BaseModel):
    teaching_method_name: str
    dtstart: datetime
    dtend: datetime
    studentgroups: list[str] | None
    room: list[RoomResponse] | None


class CourseResponse(BaseModel):
    course_id: str
    slug: str
    name: str
    activities: list[ActivityResponse] | None
    events: list[EventResponse] | None


class TPCourse(BaseModel):
    id: str
    name: str
    name_en: str | None
    name_nn: str | None
    terminnr: str | None
    courseid: str


class TPActivity(BaseModel):
    padnum: str
    name: str
    name_nn: str | None
    name_en: str | None
    id: str
    coursetype: str
    courseid: str


class ScrapeOutput(BaseModel):
    allCourseTermin: list[TPCourse]
    selCourseTermin: list
    selCourseNoTermin: list
    allActivities: list[TPActivity]
    selActivities: list
    activitiesToFetch: list
    activitytimesToFetch: list


class TPRoom(BaseModel):
    id: str
    roomid: str
    roomurl: str
    campusid: str
    roomname: str
    videolink: bool | str
    buildingid: str
    buildingurl: str
    roomacronym: str
    buildingname: str
    showforstudent: bool
    buildingacronym: str
    equipment_function: str | None


class TimetableOutput(BaseModel):
    id: str
    semesterid: str
    courseid: str
    weeknr: int
    dtstart: datetime
    dtend: datetime
    lopennr: int | None
    teaching_method: str = Field(alias="teaching-method")
    teaching_method_name: str = Field(alias="teaching-method-name")
    teaching_title: str = Field(alias="teaching-title")
    summary: str
    studentgroups: list[str] | None
    room: list[TPRoom] | None
    terminnr: int
    aid: str
    status: str
    active: bool
    compulsory: bool
    coursetype: str
    editurl: str
    virtual_course_name: str | None = Field(alias="virtual-course-name")
    weeknumberid: int
    resources: list[str]
    weekday: int
    eventid: str
    multiday: bool
