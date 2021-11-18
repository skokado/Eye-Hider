from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app import eye_hider
from app import schemas

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def hello():
    return {'msg': 'it works'}


@app.post('/hide-eyes')
async def hide(request: Request):
    request_body: bytes = await request.body()
    try:
        masked_image: bytes = eye_hider.main_handle(request_body)
        return Response(content=masked_image)
    except AssertionError:
        return Response(content=b'', status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
