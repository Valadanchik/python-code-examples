import io
import os
import uuid
import pandas as pd


from fastapi.responses import StreamingResponse  # Add to Top

from fastapi import Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse

from starlette.responses import RedirectResponse

from reader import get_text_from_image
from reader import get_barcode_from_image

from config import UPLOAD_DIR, csv_file_path
from config import system_prompt_ingredients, system_prompt_energy
from extensions import app, templates

from csv_operations import read_csv, csv_to_html_table, append_to_csv

from gpt_utils import ask_question


@app.get("/", response_class=HTMLResponse)
async def get_upload_form(request: Request):
    return templates.TemplateResponse("upload_form.html", context={"request": request})


@app.post("/uploadfile/")
async def create_upload_file(request: Request, file: UploadFile = File(...)):
    try:
        file.filename = f"{uuid.uuid4()}.jpg"
        contents = await file.read()

        with open(f"{UPLOAD_DIR}{file.filename}", "wb") as f:
            f.write(contents)

            text_from_image = get_text_from_image(f"{UPLOAD_DIR}{file.filename}")
            ingredients = ask_question(text_from_image, system_prompt_ingredients)
            energy = ask_question(text_from_image, system_prompt_energy)
            barcode = get_barcode_from_image(f"{UPLOAD_DIR}{file.filename}")
            append_to_csv(csv_file_path, barcode, ingredients, energy)

        return RedirectResponse(url="/data", status_code=303)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)



@app.get("/data", response_class=HTMLResponse)
async def csv_to_html():
    data = read_csv(csv_file_path)
    table_html = csv_to_html_table(data)
    return f"<html><body>{table_html}</body></html>"





# Replace this with the path to your CSV file
@app.get("/download-data/")
async def download_csv():
    try:
        # Read the CSV file using Pandas
        df = pd.read_csv(csv_file_path, sep='~')  # Assuming the delimiter in the CSV file is ","
        print(df)
        # Convert the DataFrame to CSV data with the specified delimiter (~)
        csv_data = df.to_csv(index=False)
        # Convert the CSV data to bytes
        csv_data_bytes = io.BytesIO(csv_data.encode())

        # Create a StreamingResponse to send the data as a downloadable CSV file
        response = StreamingResponse(iter([csv_data_bytes.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = 'attachment; filename="downloaded.csv"'
        return response
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)
