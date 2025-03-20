from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated, Optional, Literal
from pydantic import BaseModel, Field

load_dotenv()

model = ChatOpenAI(model='gpt-4o')

# schema
json_schema = {
  "title": "Review",
  "type": "object",
  "properties": {
    "key_themes": {
      "type": "array",
      "items": {
        "type": "string"
      },
      "description": "Write down all the key themes discussed in the review in a list"
    },
    "summary": {
      "type": "string",
      "description": "A brief summary of the review"
    },
    "sentiment": {
      "type": "string",
      "enum": ["pos", "neg"],
      "description": "Return sentiment of the review either negative, positive or neutral"
    },
    "pros": {
      "type": ["array", "null"],
      "items": {
        "type": "string"
      },
      "description": "Write down all the pros inside a list"
    },
    "cons": {
      "type": ["array", "null"],
      "items": {
        "type": "string"
      },
      "description": "Write down all the cons inside a list"
    },
    "name": {
      "type": ["string", "null"],
      "description": "Write the name of the reviewer"
    }
  },
  "required": ["key_themes", "summary", "sentiment"]
}
    

structured_model = model.with_structured_output(json_schema)
# this is a real review from amazon of iphone 16 pro max
result = structured_model.invoke("""This is my 1st iPhone and I switched from samsung S20 FE. I’m writing this review/observations after the usage of 1 month.

After paying 1.3 lac you will get
1. A Palm Heater. You just start using the camera even for short duration it will get heated significantly. Or You do something intensive task like insta reel edit/upload, erase object from photos (when i used this feature phone got crashed and rebooted). I was in impression that okay it will feel warm before purchasing. But it’s a heater that will be felt at frame as well as back.
2. A genius camera button jisko apni existance kyun hai, Pata nahi. I used this button only when i need to shoot immediately but while shooting in portrait display mode it will zoom in/out accidentally because of this button touch sensitivity which results in quality of photo.
3.Ceramic glass is kachchi kali for scratches. It got so many scratches in 1 month usage not major but i was taking care but still it got.
4. Glitches in UI. Okay android companies making so many products in so may have difficulty to maintain bug free UI. But my samsung phone was superior in UI management.
5. Placements of volume and lock buttons. So many times it has taken screenshots while operating volume buttons as other this lock button will get pressed to hold/generate the pressure.

My desires for a phone was the great camera system and in that it’s performing well but expectations versus reality m kahin na kahin maza nahi aaya.
                                 
Review by Ram meena
""")

result= dict(result)
print(result)