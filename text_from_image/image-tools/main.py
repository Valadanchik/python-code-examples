import io
import uuid
import pandas as pd

from fastapi.responses import StreamingResponse

from fastapi import Request
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.responses import FileResponse, JSONResponse

from starlette.responses import RedirectResponse

from reader import get_text_from_image
from reader import get_barcode_from_image

from extensions import app, templates

from config import UPLOAD_DIR, csv_file_path
from config import system_prompt_ingredients, system_prompt_energy, csv_delimiter

from gpt_utils import ask_question

from csv_operations import read_csv, csv_to_html_table, append_to_csv



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

            energy, ingredients, barcode = energy if energy else "Not Found", \
                ingredients if ingredients else "Not Found",\
                barcode if barcode else "Not Found"
            append_to_csv(csv_file_path, barcode, ingredients, energy)

        return RedirectResponse(url="/data", status_code=303)
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


@app.get("/data", response_class=HTMLResponse)
async def csv_to_html():
    data = read_csv(csv_file_path)
    table_html = csv_to_html_table(data)
    return f"<html><body>{table_html}</body></html>"


@app.get("/download-data/")
async def download_csv():
    try:
        df = pd.read_csv(csv_file_path, sep=csv_delimiter)  # Assuming the delimiter in the CSV file is ","

        csv_data = df.to_csv(index=False)

        csv_data_bytes = io.BytesIO(csv_data.encode())

        response = StreamingResponse(iter([csv_data_bytes.getvalue()]), media_type="text/csv")
        response.headers["Content-Disposition"] = 'attachment; filename="downloaded.csv"'
        return response
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


@app.get("/remove_row/{row_index}")
def remove_row(row_index: int):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file_path, sep=csv_delimiter)

    if len(df) == 1:
        empty_df = pd.DataFrame(columns=df.columns)
        empty_df.to_csv(csv_file_path, sep=csv_delimiter, index=False)
        return RedirectResponse(url="/data", status_code=303)
    elif 0 <= row_index:
        df = df.drop(row_index-1)

        df.to_csv(csv_file_path, sep=csv_delimiter, index=False)
        return RedirectResponse(url="/data", status_code=303)
    else:
        return {"error": "Invalid row index."}
