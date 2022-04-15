from fastapi import FastAPI

# fast api app
app = FastAPI()


# health check for aws
@app.get("/health-check/")
def health_check():
    return {"message": "OK"}
