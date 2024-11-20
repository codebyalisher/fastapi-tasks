from fastapi import  File, UploadFile
from fastapi.responses import JSONResponse


async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    return JSONResponse(content={"filename": file.filename, "content_type": file.content_type})
