from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

click_count = 0

@app.get("/message")
def get_message():
    global click_count
    click_count += 1
    return {"message": f"Hello from FastAPI! Click count: {click_count}"}
