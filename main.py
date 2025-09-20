# main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from xml_parser import xml_to_json
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uvicorn


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/xmlToJson")
async def xml_to_json_endpoint(file: UploadFile = File(...)):
    if not file.filename.endswith('.xml'):
        raise HTTPException(status_code=400, detail="File must be an XML file.")
    content = await file.read()
    xml_str = content.decode('utf-8')
    try:
        json_dict = xml_to_json(xml_str)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"XML parsing error: {str(e)}")
    return JSONResponse(content=json_dict)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

