from typing import List

from fastapi import Depends, APIRouter, HTTPException, Body

from database.orm import BusinessClient
from database.repository import BusinessClientRepository
from schema.request import CreateBusinessClientRequest
from schema.response import BusinessClientListSchema, BusinessClientSchema, UpdateBusinessClientSchema

router = APIRouter(prefix="/businessClient")

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
        request: CreateBusinessClientRequest,
        client_repo : BusinessClientRepository = Depends()
):

    business_client : BusinessClient = BusinessClient.create(request=request)
    business_client: BusinessClient = client_repo.create_business_client(businessClient=business_client)

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
