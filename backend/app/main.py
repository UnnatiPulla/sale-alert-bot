from fastapi import FastAPI

app = FastAPI(title="Sale Alert Bot")

@app.get("/")
def root():
    return {"message": "Sale Alert Bot API is running"}