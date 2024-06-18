#! venv/bin/python3

from fastapi import FastAPI, APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from openai import OpenAI

api_router = APIRouter(prefix="/api")
client = OpenAI()
counter = 0

import mail

from pydantic import BaseModel, EmailStr
from datetime import datetime
from dotenv import load_dotenv
import json
from chat import Model

load_dotenv()
model = Model()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Session(BaseModel):
    id: str
    timestamp: datetime

class AIMessage(BaseModel):
    user: str
    message: str
    timestamp: datetime
    session_id: str

class APIChatMessage(BaseModel):
    user: str
    prompt: str
    session_id: str

class SiemAlert(BaseModel):
    content: str
    user: EmailStr

def make_analysis_summary(analysis_content) -> str:
    model = Model(system_prompt_fname="system_prompt.txt")
    session_id =model.create_new_session()
    res = model(analysis_content, session_id=session_id)
    return res.choices[0].message.content

#This endpoint will receive a fake alert from splunk
@api_router.post("/webhook")
async def receive_alert(request: Request):
    payload = await request.json()
    print(f"Received alert:\n {json.dumps(payload, indent=4)}")

    #Send alert to chatgpt
    prompt = f"Alert: \n f{payload}"
    session_id = model.create_new_session()
    res = model(prompt, session_id=session_id)
    content = res.choices[0].message.content

    #Make summary of the analysis made by chatgpt
    print("Making summary...")
    summary = make_analysis_summary(content)

    user="enzowstm@gmail.com"
    username = user.split("@")[0]

    session_url = f"http://localhost:5173/{session_id}"

    html = mail.build_mail(username=username, content=summary, session_url=session_url)
    mail.send_mail(user, html, "html", asunto="SIEM ALERT URGENT")
    # Process the alert here (e.g., log it, take an action, etc.)

    msg = f"Email sent successfully to {user}"
    return JSONResponse(status_code=200, 
                        content={"message": msg})

#This endpoint creates a new session id
@api_router.post("/chat/session")
async def get_new_id():
    session_id =model.create_new_session()
    session = Session(id=session_id, timestamp=datetime.now())
    return {"session": session}

@api_router.post("/chat/message")
async def receive_user_message(message: APIChatMessage, response_model=AIMessage):
    res = model(message.prompt, session_id=message.session_id)

    ai_message = AIMessage(
        user=message.user,
        message=res.choices[0].message.content,
        timestamp= datetime.now(),
        session_id=message.session_id
    )

    return ai_message


async def generate_response(ws: WebSocket, user_prompt: str):
    messages = [
        {"role": "system",
         "content" : "You are a helpful assistant"}
    ]

    messages.append({
        "role" : "user",
        "content" : user_prompt
    })

    res = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1024,
        stream=True
    )
    try:
        for chunk in res:
            if len(chunk.choices) > 0:
                chunk_content = chunk.choices[0].delta.content
                if chunk_content:
                    print(f"sending : {chunk_content} of type : {type(chunk_content)}")
                    await ws.send_text(chunk_content)
    except WebSocketDisconnect:
        print("Websocket Disconnected")


@api_router.websocket("/stream")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    print("Received connection!")
    while True:
        try:
            data = await ws.receive_text()
            await generate_response(ws, data)
        except WebSocketDisconnect:
            print("Client Disconnected")
            break



app.include_router(api_router)