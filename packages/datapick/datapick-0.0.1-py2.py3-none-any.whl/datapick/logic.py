""" Module for calling workflows. """

import os
import json
from typing import List, Union
from .utils import get_workflow, record_example, pdf_to_string
from .backends import ModelProvider, OpenAI, Anthropic, Groq

import re
TRAILING_COMMA_PATTERN = r',\s*}' # pattern for detecting trailing comma in JSON

if "DATAPICK_API_KEY" not in os.environ:
    print("WARNING: datapick credentials not found. Add your DATAPICK_API_KEY in a .env file.")

BACKEND_MAPPING = {}

if "OPENAI_API_KEY" in os.environ:
    BACKEND_MAPPING["openai"] = OpenAI()
if "GROQ_API_KEY" in os.environ:
    BACKEND_MAPPING["groq"] = Groq()
if "ANTHROPIC_API_KEY" in os.environ:
    BACKEND_MAPPING["anthropic"] = Anthropic()

if not BACKEND_MAPPING:
    print("WARNING: no backends available. Add your OPENAI_API_KEY, ANTHROPIC_API_KEY, etc. in a .env file.")
else:
    print("Available backends:", ", ".join(BACKEND_MAPPING.keys()))

def get_model_provider(backend_name: str) -> ModelProvider:
    if backend_name in BACKEND_MAPPING.keys():
        return BACKEND_MAPPING[backend_name]
    else:
        raise Exception("backend not available")

def get_default_backend():
    """ Get the default backend from the available ones. """
    available_backends = list(BACKEND_MAPPING.keys())
    if 'openai' in available_backends:
        return 'openai'
    elif 'anthropic' in available_backends:
        return 'anthropic'
    elif 'groq' in available_backends:
        return 'groq'
    else:
        raise Exception("no backend available")

def call(workflow_name: str, input_text: str = None, backend="auto", 
         from_file=None, output_json=False, record: bool = True, time_call: bool = False,
         model: str = None):
    # Get workflow details
    workflow = get_workflow(workflow_name)

    # Get default backend
    if backend == "auto":
        backend = get_default_backend()

    # Get the model provider, e.g. OpenAI, Anthropic, etc.
    model_provider = get_model_provider(backend)

    # Turn input file into text if necessary
    if from_file is not None:
        if from_file.endswith(".txt"):
            with open(from_file, "r") as file:
                input_text = file.read()
        elif from_file.endswith(".pdf"):
            input_text = pdf_to_string(from_file)
        else: 
            raise Exception("file must end in .txt or .pdf")

    # Get output from the backend LLM
    output = model_provider.call(input_text=input_text, workflow=workflow, 
                                 time_call=time_call, model=model)

    # Record input-output example in the database
    if record: record_example(workflow_name, input_text, output)

    # Sanitize output and return
    if output_json:
        sanitized_output = re.sub(TRAILING_COMMA_PATTERN, '}', 
                                  output.replace("'", '"'))
        return json.loads(sanitized_output)
    else:
        return output
    return output