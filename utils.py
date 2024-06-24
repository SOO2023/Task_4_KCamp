import requests
from dotenv import load_dotenv
import os
from fastapi.exceptions import HTTPException
from fastapi import Query, Path
from sympy import sympify
import re
from datetime import datetime

load_dotenv()
WEATHER_API = os.getenv("WEATHER_API")


# ----------------------------------------------------------------------------------------------------------------------------------------
# Functions for Task 1
# ----------------------------------------------------------------------------------------------------------------------------------------
def simple_calculator(
    math_expression: str = Query(
        description="A simple calculator that does basic mathematical operations.",
        pattern="^[+-]?\d+(\.\d+)?(\s*[\+\-\*/]\s*[+-]?\d+(\.\d+)?)+",
        examples=["2.2 * 16 / 17 - 19 + 1"],
        tags=["calculator"],
    )
) -> dict:
    math_expression_cleaned = re.sub(
        ".[\+\-\*/]+(\s*[\+\-\*/]*)?$", "", math_expression
    )
    math_expression_cleaned = re.sub("(?<=\d) +(?=\d)", "", math_expression_cleaned)
    try:
        result = sympify(math_expression_cleaned).evalf()
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail={
                "msg": f"The mathematical expression could not be parsed.",
                "expression": math_expression,
            },
        )
    return {
        "message": "The mathematical operation was successfully evaluated.",
        "mathematical_expression": math_expression_cleaned,
        "result": result,
    }


# ----------------------------------------------------------------------------------------------------------------------------------------
# Functions for Task 2
# ----------------------------------------------------------------------------------------------------------------------------------------
def get_greeting() -> dict:
    time = datetime.now()
    hour = time.hour
    if 6 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon"
    elif 18 <= hour < 22:
        greeting = "Good Evening"
    else:
        greeting = "Hello"

    return {"greeting": greeting, "time": time.strftime("%a, %b %d, %Y %I:%M:%S %p")}


# ----------------------------------------------------------------------------------------------------------------------------------------
# Functions for Task 3
# ----------------------------------------------------------------------------------------------------------------------------------------
feature_flags = {
    "feature_1": True,
    "feature_2": False,
    "feature_3": True,
}


def get_feature_status(feature: str = Path()) -> dict:
    status = feature_flags.get(feature)
    if status is None:
        raise HTTPException(
            status_code=400,
            detail={"msg": "The feature entered is invalid.", "feature": feature},
        )
    return {"status": status, "feature": feature}


# ----------------------------------------------------------------------------------------------------------------------------------------
# Functions for Task 4
# ----------------------------------------------------------------------------------------------------------------------------------------
def resquest_weather_api(city: str = Query(min_length=2, pattern="[A-Za-z]+")) -> dict:
    city = city.title()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric"

    api_request = requests.get(url)
    json_response = api_request.json()
    if int(api_request.status_code) != 200:
        raise HTTPException(
            status_code=int(json_response.get("cod")),
            detail={"message": json_response.get("message")},
        )

    return {
        "message": f"{city} weather statistics successfully generated.",
        "detail": json_response,
    }
