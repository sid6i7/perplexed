import os

from dotenv import load_dotenv
import google.generativeai as genai

from model import config
from utils.reddit import *

load_dotenv()

key = os.environ['GEMINI_API_KEY']
genai.configure(api_key=key)

class ChatMessage:
    """
    A class representing a chat message.
    """

    def __init__(self, model_provider="gemini", role="user", message="") -> None:
        """
        Initializes the ChatMessage object.

        Args:
            model_provider (str, optional): The model provider. Defaults to "gemini".
            role (str, optional): The role of the chat message. Defaults to "user".
            message (str, optional): The message content. Defaults to "".
        """
        if model_provider == "gemini":
            self.message = self.__generate_for_gemini(role, message)
    

    def get_message(self):
        """
        Gets the message content.

        Returns:
            dict: A dictionary containing message information.
        """
        return self.message
        
    
    def __generate_for_gemini(self, role, message):
        """
        Generates a message for the Gemini model.

        Args:
            role (str): The role of the chat message.
            message (str): The message content.

        Returns:
            dict: A dictionary containing message information.
        """
        return {
            "role": role,
            "parts": [
                {
                    "text": message
                }
            ]
        }
        

class Model:
    """
    A class representing a generative model.
    """

    def __init__(self) -> None:
        """
        Initializes the Model object.

        Initializes Reddit and the generative model.
        """
        self.reddit = Reddit()
        self.model = genai.GenerativeModel(
            model_name= config.MODEL_NAME,
            generation_config=config.GENERATION_CONFIG
        )

    
    def __generate_prompt(self, query, comments: list[dict]):
        """
        Generates a prompt for the generative model.

        Args:
            query (str): The query to generate a response for.
            comments (list[dict]): A list of comments to include in the prompt.

        Returns:
            list: A list containing the prompt messages.
        """
        comments = "\n".join([f"{comment['body'].strip()} : {comment['score']} : {comment['url']}" for comment in comments])
        model_message = ChatMessage(
            role="model",
            message=f"""Generate a response for the question: "{query}" by using knowledge from the provided comments.\nEach comment is in the format: <text : upvotes : url : post_title>. """
        )
        user_message = ChatMessage(
            role="user",
            message="""COMMENTS BEGIN
                        {}
                        COMMENTS END""".format(comments)
        )
        prompt = [
            model_message.get_message(),
            user_message.get_message()
        ]
        
        return prompt
    

    def generate(self, query):
        """
        Generates a response for the given query.

        Args:
            query (str): The query to generate a response for.
        """
        try:
            top_comments = self.reddit.search(query)
            prompt = self.__generate_prompt(query, top_comments)
            response = self.model.generate_content(contents=prompt).text
        except Exception as e:
            print("Some error occurred", e)
            response = "Unable to answer that question, it might be inappropiate."
        return response
