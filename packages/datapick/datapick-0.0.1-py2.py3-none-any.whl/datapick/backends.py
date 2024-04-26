from .definitions import GetWorkflowResponse, Example
from typing import List
from abc import ABC, abstractmethod
import openai
import anthropic
import groq
from time import time

class ModelProvider(ABC):
    @abstractmethod
    def call(self, input_text: str, workflow: GetWorkflowResponse, time_call: bool,
             model: str = None):
        """ This interface must be implemented by all ModelProviders. """
        pass

    @staticmethod
    def example_to_string(example: Example):
        return "INPUT: {}\nOUTPUT: {}\n".format(example.input, example.output)
    
    @staticmethod
    def input_to_string(input_text: str):
        return ModelProvider.example_to_string(Example(input=input_text, output=""))

    @staticmethod
    def examples_to_string(examples: List[Example]):
        return "\n".join([ModelProvider.example_to_string(ex) for ex in examples])


class OpenAI(ModelProvider):
    def __init__(self):
        self.client = openai.OpenAI()

    @staticmethod
    def select_model(input_text: str, workflow: GetWorkflowResponse):
        return "gpt-4"

    @staticmethod
    def make_prompt(input_text: str, workflow: GetWorkflowResponse):
        system_prompt = ("You are a helpful assistant."
            + " You will receive a description of task consisting"
            + " of mapping inputs to the right outputs. You will be"
            + " given a few examples of correct input-output pairings."
            + " Your job is to provide the correct output for a new input,"
            + " according to the pattern.")
        user_prompt = (
            "### TASK DESCRIPTION\n\n{task_description}\n\n\n### EXAMPLES\n\n{examples}\n\n### NEW INPUT\n\n{input}"
            ).format(
                task_description=workflow.description, 
                examples=ModelProvider.examples_to_string(workflow.examples),
                input=ModelProvider.input_to_string(input_text)
            )
        return {"system_prompt": system_prompt, "user_prompt": user_prompt}

    def call(self, input_text: str, workflow: GetWorkflowResponse, time_call: bool,
             model: str = None):
        prompt = OpenAI.make_prompt(input_text, workflow)

        start_time = time()

        response = self.client.chat.completions.create(
            model=model if model is not None else OpenAI.select_model(input_text, workflow),
            messages=[
                {"role": "system", "content": prompt['system_prompt']},
                {"role": "user", "content": prompt['user_prompt']}
        ]
        )

        end_time = time()
        if time_call: print(f"Latency: {end_time - start_time}s")

        return response.choices[0].message.content
    

class Anthropic(ModelProvider):
    def __init__(self, max_tokens=1000):
        self.client = anthropic.Anthropic()
        self.max_tokens=max_tokens

    @staticmethod
    def select_model(input_text: str, workflow: GetWorkflowResponse):
        return "claude-3-opus-20240229"
    
    @staticmethod
    def make_prompt(input_text: str, workflow: GetWorkflowResponse):
        system_prompt = ("You are a helpful assistant."
            + " You will receive a description of task consisting"
            + " of mapping inputs to the right outputs. You will be"
            + " given a few examples of correct input-output pairings."
            + " Your job is to provide the correct output for a new input,"
            + " according to the pattern.")
        user_prompt = (
            "### TASK DESCRIPTION\n\n{task_description}\n\n\n### EXAMPLES\n\n{examples}\n\n### NEW INPUT\n\n{input}"
            ).format(
                task_description=workflow.description, 
                examples=ModelProvider.examples_to_string(workflow.examples),
                input=ModelProvider.input_to_string(input_text)
            )
        return {"system_prompt": system_prompt, "user_prompt": user_prompt}
    
    def call(self, input_text: str, workflow: GetWorkflowResponse, time_call: bool,
             model: str = None):
        prompt = Anthropic.make_prompt(input_text, workflow)

        start_time = time()

        response = self.client.messages.create(
            model=model if model is not None else Anthropic.select_model(input_text, workflow),
            system=prompt['system_prompt'],
            messages=[
                {"role": "user", "content": prompt['user_prompt']}
            ],
            max_tokens=self.max_tokens
        )

        end_time = time()
        if time_call: print(f"Latency: {end_time - start_time}s")

        return response.content[0].text
    
    
class Groq(ModelProvider):
    def __init__(self):
        self.client = groq.Groq()

    @staticmethod
    def select_model(input_text: str, workflow: GetWorkflowResponse):
        return "llama3-8b-8192"
    
    @staticmethod
    def make_prompt(input_text: str, workflow: GetWorkflowResponse):
        system_prompt = ("You are a helpful assistant."
            + " You will receive a description of task consisting"
            + " of mapping inputs to the right outputs. You will be"
            + " given a few examples of correct input-output pairings."
            + " Your job is to provide the correct output for a new input,"
            + " according to the pattern.")
        user_prompt = (
            "### TASK DESCRIPTION\n\n{task_description}\n\n\n### EXAMPLES\n\n{examples}\n\n### NEW INPUT\n\n{input}"
            ).format(
                task_description=workflow.description, 
                examples=ModelProvider.examples_to_string(workflow.examples),
                input=ModelProvider.input_to_string(input_text)
            )
        return {"system_prompt": system_prompt, "user_prompt": user_prompt}
    
    def call(self, input_text: str, workflow: GetWorkflowResponse, time_call: bool,
             model: str = None):
        prompt = Groq.make_prompt(input_text, workflow)

        start_time = time()

        response = self.client.chat.completions.create(
            model=model if model is not None else Groq.select_model(input_text, workflow),
            messages=[
                {"role": "system", "content": prompt['system_prompt']},
                {"role": "user", "content": prompt['user_prompt']}
        ]
        )

        end_time = time()
        if time_call: print(f"Latency: {end_time - start_time}s")
        return response.choices[0].message.content