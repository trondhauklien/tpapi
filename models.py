from datetime import datetime

from mongoengine import (
    BooleanField,
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    IntField,
    ListField,
    StringField,
)
from pydantic import BaseModel, Field


class Activity(EmbeddedDocument):
    activityid = StringField()
    name = StringField()
    name_en = StringField()
    name_nn = StringField()
    coursetype = StringField()


class Room(EmbeddedDocument):
    roomid = StringField()
    roomurl = StringField()
    campusid = StringField()
    roomname = StringField()
    videolink = StringField()
    buildingid = StringField()
    buildingurl = StringField()
    roomacronym = StringField()
    buildingname = StringField()
    showforstudent = BooleanField()
    buildingacronym = StringField()
    equipment_function = StringField()


class Event(EmbeddedDocument):
    semesterid = StringField()
    weeknr = IntField()
    dtstart = DateTimeField()
    dtend = DateTimeField()
    lopennr = IntField()
    teaching_method = StringField()
    teaching_method_name = StringField()
    teaching_title = StringField()
    summary = StringField()
    studentgroups = ListField(StringField())
    room = list[Room]
    terminnr = IntField()
    status = StringField()
    active = BooleanField()
    compulsory = BooleanField()
    coursetype = StringField()
    virtual_course_name = StringField()
    weeknumberid = IntField()
    resources = list[str]
    weekday = IntField()
    multiday = BooleanField()


class Course(Document):
    course_id = StringField()
    slug = StringField()
    name = StringField()
    name_en = StringField()
    name_nn = StringField()
    activities_fetched = BooleanField(default=False)
    activities = ListField(EmbeddedDocumentField(Activity))
    timetable_fetched = BooleanField(default=False)
    events = ListField(EmbeddedDocumentField(Event))


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
    dtstart: str
    dtend: str
    studentgroups: list[str]
    # room: list[RoomResponse]


class CourseResponse(BaseModel):
    course_id: str
    slug: str
    name: str
    activities: list[ActivityResponse]
    # events: list[EventResponse]


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
