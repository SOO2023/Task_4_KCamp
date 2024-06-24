from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from utils import (
    resquest_weather_api,
    simple_calculator,
    get_greeting,
    get_feature_status,
)
from model import WeatherModel, MathModel, GreetingModel, FeatureModel


app = FastAPI()


# -------------------------------------------------------------------------------------------------------------------------------------------
# TASK 1 - Dependency Injected Calculator API
# -------------------------------------------------------------------------------------------------------------------------------------------
@app.get("/math-operation", response_model=MathModel, tags=["calculator"])
def math_operation(result_dict: dict = Depends(simple_calculator)):
    return result_dict


# -------------------------------------------------------------------------------------------------------------------------------------------
# TASK 2 - Configurable Greeting API
# -------------------------------------------------------------------------------------------------------------------------------------------
@app.get("/greeting", response_model=GreetingModel, tags=["greeting"])
def greeting(greeting_dict: dict = Depends(get_greeting)):
    return greeting_dict


# -------------------------------------------------------------------------------------------------------------------------------------------
# TASK 3 - Configurable Feature Flags API
# -------------------------------------------------------------------------------------------------------------------------------------------
@app.get("/features/{feature}", response_model=FeatureModel, tags=["feature"])
def get_feature(feature_dict: dict = Depends(get_feature_status)):
    status = feature_dict.get("status")
    feature = feature_dict.get("feature")
    if not status:
        raise HTTPException(
            status_code=403,
            detail={
                "msg": "Forbidden feature. Feature is currently disabled.",
                "feature": feature,
                "feature_is_enable": status,
            },
        )
    return {"feature_is_enable": status, "feature": feature}


# -------------------------------------------------------------------------------------------------------------------------------------------
# TASK 4 - Third-Party API Integration
# -------------------------------------------------------------------------------------------------------------------------------------------
@app.get("/weather", response_model=WeatherModel, tags=["weather"])
def weather(weather_dict: dict = Depends(resquest_weather_api)):
    return JSONResponse(content=weather_dict, status_code=200)
