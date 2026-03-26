from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db_session
from app.schemas.uploads import HistoricalDataStatusResponse, UploadResultResponse
from app.services.historical_data_service import get_historical_data_status, save_historical_dataset

router = APIRouter(prefix="/historical-data", tags=["historical-data"])


@router.get("/status", response_model=HistoricalDataStatusResponse)
def historical_data_status(session: Session = Depends(get_db_session)) -> HistoricalDataStatusResponse:
    return HistoricalDataStatusResponse(items=get_historical_data_status(session))


@router.post("/upload", response_model=UploadResultResponse)
async def upload_historical_data(
    dataset_type: str = Form(...),
    file: UploadFile = File(...),
    session: Session = Depends(get_db_session),
) -> UploadResultResponse:
    if dataset_type not in {"batting", "bowling", "fielding"}:
        raise HTTPException(status_code=400, detail="dataset_type must be batting, bowling, or fielding.")

    if not file.filename:
        raise HTTPException(status_code=400, detail="A file is required.")

    file_bytes = await file.read()
    result = save_historical_dataset(session, dataset_type, file.filename, file_bytes)
    return UploadResultResponse(**result)
