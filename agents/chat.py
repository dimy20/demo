#! venv/bin/python3

from openai import OpenAI
from typing import Dict, List
from dotenv import load_dotenv
import redis
from pydantic import BaseModel
import json
import uuid
import config
import os

class MessageT(BaseModel):
    role: str
    content: str

class Model:
    def __init__(self, system_prompt_fname: str = "system_prompt2.txt"):
        self.client = OpenAI()
        self.r = redis.Redis(host=os.getenv("REDIS_SERVICE"), port=6379, db=0)

        with open(system_prompt_fname, "r") as f:
            self.system_prompt = f.read()

    def get_session_history(self, session_id: str):
        session = json.loads(self.r.get(session_id))
        return [MessageT.parse_obj(msg) for msg in session["history"]]

    def update_history(self, msg: MessageT, session_id):
        session = json.loads(self.r.get(session_id))
        session["history"].append(msg.dict())
        self.r.set(session_id, json.dumps(session))

    def create_new_session(self) -> str:
        system_msg = MessageT(role="system", content=self.system_prompt)
        session_id = str(uuid.uuid4())
        self.r.set(session_id, json.dumps({"history" : [system_msg.dict()]}))
        return session_id
        
    #Format messages following api spec.
    def messages_as_gpt_spec(self, msg_history: List[MessageT]):
        api_messages = []

        for msg in msg_history:
            entry = {
                "role" : msg.role,
                "content": msg.content
            }
            api_messages.append(entry)
            
        return api_messages

    def __call__(self, text: str, session_id : str):
        if session_id != "":
            new_user_msg = MessageT(role="user", content=text)
            self.update_history(new_user_msg, session_id)

            #Convert dict stored in redis to MessageT list
            api_messages = self.messages_as_gpt_spec(self.get_session_history(session_id))

            response = self.client.chat.completions.create(
                model= config.GPT_MODEL,
                messages=api_messages,
                temperature=0.7,
                max_tokens=2048,
                top_p=1
            )

            msg = response.choices[0].message
            assert len(response.choices) > 0
            
            ai_reply_msg = MessageT(role=msg.role, content=msg.content)
            self.update_history(ai_reply_msg, session_id)

            return response


