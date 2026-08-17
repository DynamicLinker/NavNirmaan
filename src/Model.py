from google import genai
from google.genai import types
from pydantic import BaseModel
import json


class StructuredResponse(BaseModel):
    text : str
    code : str

class Model:
    def __init__(self, api_key):
        self.agent = genai.Client(api_key=api_key)
        self.config = types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=StructuredResponse,
            temperature=0.4
        )

    def send_image(self, image):
        return self.agent.files.upload(file=image)
    

    def getResponse(self, image):
        image = self.send_image(image)

        response = self.agent.models.generate_content(
            model = 'gemini-3.1-flash-lite',
            contents = [image, "provide openscad code for the image so i can project it in 3d."],
            config = self.config
        )

        return json.loads(response.text)


