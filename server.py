{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 \
Action: file_editor view /app/backend/server.py\
Observation: /app/backend/server.py:\
1|from fastapi import FastAPI, APIRouter\
2|from dotenv import load_dotenv\
3|from starlette.middleware.cors import CORSMiddleware\
4|from motor.motor_asyncio import AsyncIOMotorClient\
5|import os\
6|import logging\
7|from pathlib import Path\
8|from pydantic import BaseModel, Field\
9|from typing import List\
10|import uuid\
11|from datetime import datetime\
12|\
13|\
14|ROOT_DIR = Path(__file__).parent\
15|load_dotenv(ROOT_DIR / '.env')\
16|\
17|# MongoDB connection\
18|mongo_url = os.environ['MONGO_URL']\
19|client = AsyncIOMotorClient(mongo_url)\
20|db = client[os.environ['DB_NAME']]\
21|\
22|# Create the main app without a prefix\
23|app = FastAPI()\
24|\
25|# Create a router with the /api prefix\
26|api_router = APIRouter(prefix="/api")\
27|\
28|\
29|# Define Models\
30|class StatusCheck(BaseModel):\
31|    id: str = Field(default_factory=lambda: str(uuid.uuid4()))\
32|    client_name: str\
33|    timestamp: datetime = Field(default_factory=datetime.utcnow)\
34|\
35|class StatusCheckCreate(BaseModel):\
36|    client_name: str\
37|\
38|# Add your routes to the router instead of directly to app\
39|@api_router.get("/")\
40|async def root():\
41|    return \{"message": "Hello World"\}\
42|\
43|@api_router.post("/status", response_model=StatusCheck)\
44|async def create_status_check(input: StatusCheckCreate):\
45|    status_dict = input.dict()\
46|    status_obj = StatusCheck(**status_dict)\
47|    _ = await db.status_checks.insert_one(status_obj.dict())\
48|    return status_obj\
49|\
50|@api_router.get("/status", response_model=List[StatusCheck])\
51|async def get_status_checks():\
52|    status_checks = await db.status_checks.find().to_list(1000)\
53|    return [StatusCheck(**status_check) for status_check in status_checks]\
54|\
55|# Include the router in the main app\
56|app.include_router(api_router)\
57|\
58|app.add_middleware(\
59|    CORSMiddleware,\
60|    allow_credentials=True,\
61|    allow_origins=["*"],\
62|    allow_methods=["*"],\
63|    allow_headers=["*"],\
64|)\
65|\
66|# Configure logging\
67|logging.basicConfig(\
68|    level=logging.INFO,\
69|    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'\
70|)\
71|logger = logging.getLogger(__name__)\
72|\
73|@app.on_event("shutdown")\
74|async def shutdown_db_client():\
75|    client.close()\
76|\
\
}