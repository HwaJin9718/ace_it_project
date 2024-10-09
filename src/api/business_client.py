from pathlib import Path
from PIL import Image
from typing import List, Optional

from fastapi import Depends, APIRouter, HTTPException, Body, Form, UploadFile, File

from database.orm import BusinessClient
from database.repository import BusinessClientRepository
from schema.response import BusinessClientListSchema, BusinessClientSchema, UpdateBusinessClientSchema

router = APIRouter(prefix="/businessClient")

LOGO_DIR = Path("logos/")
LOGO_DIR.mkdir(parents=True, exist_ok=True)  # 디렉토리 생성 코드
THUMBNAIL_SIZE = (200, 100)

@router.get("", status_code=200)
def get_business_client(
        client_repo : BusinessClientRepository = Depends()
) -> BusinessClientListSchema:
    business_clients : List[BusinessClient] = client_repo.get_business_client()

    return BusinessClientListSchema(
        business_clients=[
            BusinessClientSchema.model_validate(business_client) for business_client in business_clients
        ]
    )

@router.get("/{client_id}", status_code=200)
def get_business_client(
        client_id: int,
        client_repo : BusinessClientRepository = Depends()
) -> BusinessClientSchema:

    business_client : BusinessClient = client_repo.get_business_client_by_id(client_id)

    if business_client:
        return BusinessClientSchema.model_validate(business_client)

    raise HTTPException(status_code=404, detail="BusinessClient Not Found")

@router.post("", status_code=201)
def create_business_client(
        client_name : str = Form(...),
        client_logo : Optional[UploadFile] = File(None),
        client_repo : BusinessClientRepository = Depends()
):

    business_client : BusinessClient = BusinessClient.create(client_name=client_name)
    business_client = client_repo.create_business_client(businessClient=business_client)

    if client_logo:
        thumbnail_path = LOGO_DIR / f"{business_client.client_id}_thumbnail_{client_logo.filename}"

        with Image.open(client_logo.file) as img:
            img.thumbnail(THUMBNAIL_SIZE)
            img.save(thumbnail_path)

        business_client.client_logo_name = client_logo.filename
        business_client.client_logo_path = str(thumbnail_path)

    business_client: BusinessClient = client_repo.update_business_client(businessClient=business_client)

    return BusinessClientSchema.model_validate(business_client)

@router.patch("/{client_id}", status_code=200)
def update_business_client(
        client_id: int,
        request: UpdateBusinessClientSchema = Body(..., embed=True),
        client_repo : BusinessClientRepository = Depends()
):
    business_client: BusinessClient | None = client_repo.get_business_client_by_id(client_id)

    if business_client:

        business_client.client_name = request.client_name

        update_business_client : BusinessClient = client_repo.update_business_client(business_client)

        return BusinessClientSchema.model_validate(update_business_client)

    raise HTTPException(status_code=404, detail="BusinessClient Not Found")

@router.delete("/{client_id}", status_code=204)
def delete_business_client(
        client_id: int,
        client_repo : BusinessClientRepository = Depends()
):
    business_client: BusinessClient | None = client_repo.get_business_client_by_id(client_id)

    if not business_client:
        raise HTTPException(status_code=404, detail="BusinessClient Not Found")

    client_repo.delete_business_client(client_id)
