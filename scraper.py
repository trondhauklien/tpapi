import json
import re

import requests

from bs4 import BeautifulSoup
from pydantic import parse_obj_as

from models import ScrapeOutput, TimetableOutput


URL = "https://tp.educloud.no/ntnu/timeplan"


def scrapeCourseAct(
    courses=None, activities=None, week=2, weekTo=18, ar=2023, timetable=False
):
    """
    Scrape timeplan for courses and activities.
    """

    params = {
        "type": "courseact",
        "week": week,
        "weekTo": weekTo,
        "ar": ar,
        "stop": "1",
    }
    if courses:
        params["id[]"] = [s + "¤" for s in courses]
    if activities:
        params["activityid[]"] = activities

    page = requests.get(URL, params=params)

    soup = BeautifulSoup(page.content, "html.parser")

    data = {}
    if not timetable:
        match_string = "var courseactMenu = "
        for tag in soup.find_all("script"):
            if match_string in tag.text:
                # extract data between match_string and ; using regex
                data = json.loads(re.search(match_string + "(.*);", tag.text).group(1))
        output = ScrapeOutput(**data)
        return output

    tag = soup.find(id="data-js")
    data = json.loads(tag.text)

    output: list[TimetableOutput] = []
    output = parse_obj_as(list[TimetableOutput], data)

    return output


scrapeCourseAct(courses=["TDT4102"], timetable=True)
