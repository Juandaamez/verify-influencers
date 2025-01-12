from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.claim_processing import extract_claims, remove_duplicates, verify_claim
from app.core.security import get_current_user

class ClaimRequest(BaseModel):
    text: str

router = APIRouter()

@router.post("/process", tags=["Claims"])
def process_claims(
    request: ClaimRequest,
    current_user: dict = Depends(get_current_user)
):

    try:

        raw_claims = extract_claims(request.text)
        

        unique_claims = remove_duplicates(raw_claims)
        

        verified_claims = []
        for claim in unique_claims:
            verification_result = verify_claim(claim)
            verified_claims.append({"claim": claim, "verification": verification_result})

        return {"processed_claims": verified_claims}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
