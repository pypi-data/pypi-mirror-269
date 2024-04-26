import os
from typing import Optional, List
from dotenv import load_dotenv
import requests
from .definitions import GetWorkflowResponse, \
    RecordExampleResponse, CreateWorkflowResponse
import datetime
import PyPDF2


load_dotenv()

BASE_URL = "https://api.datapick.ai"
API_KEY = os.getenv('DATAPICK_API_KEY')
HEADERS = {
    "Authorization": f"Bearer {API_KEY}"
}


def get_timestamp():
    """ Get ISO 8601 timestamp. """
    return datetime.datetime.now(datetime.UTC).isoformat()


def list_workflows():
    """ List the names of all workflows for this user. """
    try:
        json_response = requests.post(
            url = BASE_URL + "/" + "workflows/read",
            headers = HEADERS
        ).json()
    except:
        print("Something went wrong.")
    return [ record['name'] for record in json_response ]


def get_workflow(workflow_name) -> GetWorkflowResponse:
    """ Get the details for a specific workflow."""
    try:
        json_response = requests.post(
            json = {"name": workflow_name}, 
            url = BASE_URL + "/" + "workflows/read",
            headers = HEADERS
        ).json()
    except Exception as e:
        print(e)
        print("Something went wrong.")

    if len(json_response) == 0:
        raise Exception("Workflow does not exist")
    elif len(json_response) == 1:
        return GetWorkflowResponse(**(json_response[0]))
    else:
        raise Exception("Something went wrong.")
    

def create_workflow(
        workflow_name: str,
        workflow_description: str
    ) -> CreateWorkflowResponse:
    try:
        response = requests.post(
            json = {
                "name": workflow_name, 
                "description": workflow_description
            }, 
            url = BASE_URL + "/" + "workflows/create",
            headers = HEADERS
        )
        return CreateWorkflowResponse(
            success=response.status_code==200
        )
    except Exception as e:
        print(e)
        print("Something went wrong.")
    

def record_example(
        workflow_name: str,
        input_text: str, output_text: str, 
        tags: Optional[List[str]] = None
    ) -> RecordExampleResponse:
    """ Record a call to an LLM. """
    timestamp = get_timestamp()
    try:
        data = {
            "workflow_name": workflow_name,
            "input": input_text, "output": output_text,
            "timestamp": timestamp
        }

        # optionally add tags
        if tags is not None:
            data['tags'] = tags

        # post to the API
        response = requests.post(
            json = data, 
            url = BASE_URL + "/" + "workflows/record",
            headers = HEADERS
        )
        return RecordExampleResponse(
            success=response.status_code==200
        )
    except Exception as e:
        print(e)
        print("Something went wrong.")


def pdf_to_string(file_path):
    text = ""
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            # Append text of each page followed by newline
            text += page.extract_text() + "\n"
    return text

