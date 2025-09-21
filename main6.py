from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse


app = FastAPI()

@app.post("/file")
async def upload_file(uploaded_file: UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(f"1_{filename}", "wb") as buffer:
        buffer.write(file.read())

@app.post("/multiple_file")
async def upload_file(uploaded_file: list[UploadFile]):
    for uploaded_file in uploaded_file:
        file = uploaded_file.file
        filename = uploaded_file.filename
        with open(f"1_{filename}", "wb") as buffer:
            buffer.write(file.read())

@app.get("/files/{filename}")
async def get_file(filename: str):
    return FileResponse(filename)


def interfaile(filename: str):
    with open(filename, "rb") as buffer:
        while chunk := buffer.read(1024 * 1024):
            yield chunk

@app.get("/files/streaming/{filename}")
async def get_streaming_file(filename: str):
    return StreamingResponse(interfaile(filename), media_type="text/txt")