from fastapi import FastAPI
from starlette.responses import HTMLResponse

from app.routes import quiz_router, score_router, question_router

app = FastAPI()

# Include the quiz and leaderboard routers
app.include_router(quiz_router.router)
app.include_router(score_router.router)
app.include_router(question_router.router)


@app.get("/")
async def get():
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)
