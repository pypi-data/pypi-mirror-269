from datetime import datetime
import json
import os
import time
import boto3
import pytz
import httpx
import asyncio

# client = httpx.AsyncClient()

sqs = boto3.client('sqs', region_name='us-east-1')
queue_url = 'https://sqs.us-east-1.amazonaws.com/764374292299/setnext_metering'

from langchain_community.llms import Bedrock

llm = Bedrock(model_id="anthropic.claude-v2:1",
              region_name="us-east-1",
              )


def count_token(message):
    num_token = llm.get_num_tokens(message)
    print("Num of Token Found", num_token)
    return num_token


def send(message, token_type, **kwargs):
    clientId = None
    ai_platform = None
    model_parent_id = None
    model_id = None
    application_name = None
    setnext_ai_metering_api_token = None
    print("kwargs:", kwargs)

    errors = []

    try:
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "CLIENT_ID":
                    clientId = value
                if key == "AI_PLATFORM":
                    ai_platform = value
                    print(ai_platform)

                if key == "MODEL_PARENT_ID":
                    model_parent_id = value

                if key == "MODEL_ID":
                    model_id = value

                if key == "APPLICATION_NAME":
                    application_name = value

                if key == "SETNEXT_METERING_API_TOKEN":
                    setnext_ai_metering_api_token = value

        if clientId is None:
            clientId = os.environ.get("CLIENT_ID")

            if clientId is None:
                raise Exception("Client ID is mandatory")

        if ai_platform is None:
            ai_platform = os.environ.get("AI_PLATFORM")
            print(ai_platform)
            if ai_platform is None:
                raise Exception(
                    "AI_PLATFORM is mandatory, Supported AI Platforms are aws-bedrock, openai, gcp-vertex, azure-ml")
            elif ai_platform not in ["aws-bedrock", "gcp-vertex", "azure-ml", "openai"]:
                print(ai_platform)
                print(ai_platform not in ["aws-bedrock", "gcp-vertex", "azure-ml", "openai"])
                raise Exception(
                    "AI_PLATFORM value is not supported, Supported AI Platforms are aws-bedrock, openai, gcp-vertex, azure-ml")
        elif ai_platform not in ["aws-bedrock", "gcp-vertex", "azure-ml", "openai"]:
            raise Exception(
                "AI_PLATFORM value is not supported, Supported AI Platforms are aws-bedrock, openai, gcp-vertex, azure-ml")
        if model_parent_id is None:
            model_parent_id = os.environ.get("MODEL_PARENT_ID")
            if model_parent_id is None:
                raise Exception(
                    "MODEL_PARENT_ID is mandatory, Supported Models are available in the following link https://setnext.ai/help/models")

        if model_id is None:
            model_id = os.environ.get("MODEL_ID")
            if model_id is None:
                raise Exception(
                    "MODEL_ID is mandatory, Supported Models are available in the following link https://setnext.ai/help/models")

        if application_name is None:
            application_name = os.environ.get("APPLICATION_NAME")
            if application_name is None:
                raise Exception("APPLICATION_NAME is mandatory")

        if setnext_ai_metering_api_token is None:
            setnext_ai_metering_api_token = os.environ.get("SETNEXT_METERING_API_TOKEN")
            if setnext_ai_metering_api_token is None:
                raise Exception(
                    "SETNEXT_METERING_API_TOKEN is mandatory, follow the tutorial to generate the API Token")

        token = count_token(message)
        tokenSize = "s"
        current_datetime = datetime.now().isoformat()
        current_unix_ts = int(time.mktime(datetime.now().timetuple()))
        tzInfo = pytz.timezone('Asia/Kolkata')

        fmt = '%d-%m-%Y %H:%M:%S %Z%z'
        india_date_time = datetime.fromtimestamp(current_unix_ts, tz=tzInfo).strftime(fmt)

        if token < 300:
            tokenSize = "s"
        elif 300 <= token <= 600:
            tokenSize = "m"
        elif 601 <= token <= 1000:
            tokenSize = "l"
        elif 1001 <= token <= 2000:
            tokenSize = "xl"
        elif 2001 <= token <= 3000:
            tokenSize = "xxl"
        elif 3001 <= token <= 4000:
            tokenSize = "xxxl"
        else:
            tokenSize = "4xl"

        messageBody = {"client_id": clientId, "num_of_token": token, "tokenSize": tokenSize,
                       "ai_plaform": ai_platform, "model_id": model_id, "application_name": application_name,
                       "date_time": current_datetime, "token_type": token_type, "india_date_time": india_date_time,
                       "unix_ts": current_unix_ts}

        print(messageBody)

        r = httpx.post('https://t7joqdff3l.execute-api.us-east-1.amazonaws.com/dev/logs', json=messageBody,
                       headers={"Content-Type": "application/json"})
        return {"status": "success"}
    except Exception as err:
        print("Exception Occurs in the configuration, Error :", err)
        return {"status": "failed", "error": err}


async def asend(message, token_type, **kwargs):
    clientId = None
    ai_platform = None
    model_parent_id = None
    model_id = None
    application_name = None
    setnext_ai_metering_api_token = None
    print("kwargs:", kwargs)

    errors = []

    try:
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == "CLIENT_ID":
                    clientId = value
                if key == "AI_PLATFORM":
                    ai_platform = value
                    print(ai_platform)

                if key == "MODEL_PARENT_ID":
                    model_parent_id = value

                if key == "MODEL_ID":
                    model_id = value

                if key == "APPLICATION_NAME":
                    application_name = value

                if key == "SETNEXT_METERING_API_TOKEN":
                    setnext_ai_metering_api_token = value

        if clientId is None:
            clientId = os.environ.get("CLIENT_ID")

            if clientId is None:
                raise Exception("Client ID is mandatory")

        if ai_platform is None:
            ai_platform = os.environ.get("AI_PLATFORM")
            print(ai_platform)
            if ai_platform is None:
                raise Exception(
                    "AI_PLATFORM is mandatory, Supported AI Platforms are aws-bedrock, openai, gcp-vertex, azure-ml")
            elif ai_platform not in ["aws-bedrock", "gcp-vertex", "azure-ml", "openai"]:
                print(ai_platform)
                print(ai_platform not in ["aws-bedrock", "gcp-vertex", "azure-ml", "openai"])
                raise Exception(
                    "AI_PLATFORM value is not supported, Supported AI Platforms are aws-bedrock, openai, gcp-vertex, azure-ml")
        elif ai_platform not in ["aws-bedrock", "gcp-vertex", "azure-ml", "openai"]:
            raise Exception(
                "AI_PLATFORM value is not supported, Supported AI Platforms are aws-bedrock, openai, gcp-vertex, azure-ml")
        if model_parent_id is None:
            model_parent_id = os.environ.get("MODEL_PARENT_ID")
            if model_parent_id is None:
                raise Exception(
                    "MODEL_PARENT_ID is mandatory, Supported Models are available in the following link https://setnext.ai/help/models")

        if model_id is None:
            model_id = os.environ.get("MODEL_ID")
            if model_id is None:
                raise Exception(
                    "MODEL_ID is mandatory, Supported Models are available in the following link https://setnext.ai/help/models")

        if application_name is None:
            application_name = os.environ.get("APPLICATION_NAME")
            if application_name is None:
                raise Exception("APPLICATION_NAME is mandatory")

        if setnext_ai_metering_api_token is None:
            setnext_ai_metering_api_token = os.environ.get("SETNEXT_METERING_API_TOKEN")
            if setnext_ai_metering_api_token is None:
                raise Exception(
                    "SETNEXT_METERING_API_TOKEN is mandatory, follow the tutorial to generate the API Token")

        token = count_token(message)
        tokenSize = "s"
        current_datetime = datetime.now().isoformat()
        current_unix_ts = int(time.mktime(datetime.now().timetuple()))
        tzInfo = pytz.timezone('Asia/Kolkata')

        fmt = '%d-%m-%Y %H:%M:%S %Z%z'
        india_date_time = datetime.fromtimestamp(current_unix_ts, tz=tzInfo).strftime(fmt)

        if token < 300:
            tokenSize = "s"
        elif 300 <= token <= 600:
            tokenSize = "m"
        elif 601 <= token <= 1000:
            tokenSize = "l"
        elif 1001 <= token <= 2000:
            tokenSize = "xl"
        elif 2001 <= token <= 3000:
            tokenSize = "xxl"
        elif 3001 <= token <= 4000:
            tokenSize = "xxxl"
        else:
            tokenSize = "4xl"

        messageBody = {"client_id": clientId, "num_of_token": token, "tokenSize": tokenSize,
                       "ai_plaform": ai_platform, "model_id": model_id, "application_name": application_name,
                       "date_time": current_datetime, "token_type": token_type, "india_date_time": india_date_time,
                       "unix_ts": current_unix_ts}

        print(messageBody)

        async with httpx.AsyncClient() as client:

            r = await client.post('https://t7joqdff3l.execute-api.us-east-1.amazonaws.com/dev/logs', json=messageBody,
                                  headers={"Content-Type": "application/json"})
        print("Message Sent")
        return {"status": "success"}
    except Exception as err:
        print("Exception Occurs in the configuration, Error :", err)
        return {"status": "failed", "error": err}


def receive(client_id):
    return client_id + ":" + "Hello"


async def a():
    await asend("Hello How are you", "input")


# asyncio.run(asend("Hello How are you", "input"))
send("Hello How are you Hello How are you Hello How are you Hello How are you", "output")