from fastapi import FastAPI

app = FastAPI(
    title="Code Analyzer AI",
    description="A code analyzer AI that analyzes code and provides insights",
    version="1.0.0",
    
)

@app.get("/")
def root():
    return {"message": "Code Analyzer API is running"}