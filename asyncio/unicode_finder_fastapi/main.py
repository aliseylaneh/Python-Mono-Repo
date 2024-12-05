from pathlib import Path
from unicodedata import name


from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import CharName

from services import InvertedIndex

STATIC_PATH = Path(__file__).parent.absolute() / "template"
app = FastAPI(
    title="Mojifinder Web", description="Search for unicode character by name"
)


def init(app):
    app.state.index = InvertedIndex()
    app.state.form = (STATIC_PATH / "form.html").read_text()


init(app=app)


@app.get("/search", response_model=list[CharName])
async def search(q: str):
    chars = sorted(app.state.index.search(q))
    return (CharName(char=c, name=name(c)) for c in chars)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def form():
    return app.state.form
