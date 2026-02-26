from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from schemas import BirthDataRequest
from engine.astrology import calculate_chart
from engine.interpretations import build_report_content
from engine.pdf_builder import generate_pdf

app = FastAPI(title="Astrology PDF Generator API")

@app.post("/generate-report")
async def generate_astrology_report(request: BirthDataRequest):
    try:
        # 1. Calculate the placements deterministically
        chart_data = calculate_chart(
            dob=request.date_of_birth,
            tob=request.time_of_birth,
            city=request.city,
            country=request.country
        )

        # 2. Map placements to pre-written interpretations
        report_content = build_report_content(chart_data)

        # 3. Generate the PDF byte stream
        pdf_stream = generate_pdf(request.dict(), chart_data, report_content)

        # 4. Return PDF as a downloadable file stream
        headers = {
            'Content-Disposition': f'attachment; filename="Astrology_Report_{request.full_name.replace(" ", "_")}.pdf"'
        }
        return StreamingResponse(pdf_stream, media_type="application/pdf", headers=headers)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# To run locally: uvicorn main:app --reload