from fastapi import APIRouter, Depends, HTTPException, Body
import logging
import openai
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Influencer
from app.core.security import get_current_user
from app.db.models import Influencer, Claim

router = APIRouter()

@router.post("/search", tags=["Search"])
def search_and_create_influencer(
    name: str = Body(..., embed=True, example="John Doe"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        if not current_user:
            raise HTTPException(status_code=401, detail="Unauthorized user.")

        if not name.strip():
            logging.warning("Received empty name in request.")
            raise HTTPException(status_code=400, detail="Name cannot be empty.")


        influencer = db.query(Influencer).filter(Influencer.name.ilike(f"%{name}%")).first()
        if influencer:
            return {"message": "Influencer encontrado.", "id": influencer.id}


        prompt = (
            f"Generate a detailed JSON object for an influencer named {name}. "
            "The JSON must include the following keys: Handle, Followers, Description, Category, Claim, ConfidenceScore. "
            "If no information is available, provide a default but meaningful value for each field."
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a bot that generates structured JSON responses."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=200,
                temperature=0.7,
            )
            logging.info(f"OpenAI response: {response}")
        except Exception as e:
            logging.error(f"OpenAI API error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")


        try:
            response_content = response['choices'][0]['message']['content']
            logging.info(f"Raw content from OpenAI: {response_content}")

            import json
            details_dict = json.loads(response_content)


            handle = details_dict.get("Handle", f"@{name.replace(' ', '').lower()}")
            followers_count = int(details_dict.get("Followers", 100))
            description = details_dict.get("Description", f"{name} is a new influencer gaining traction.")
            category = details_dict.get("Category", "General")
            claim_text = details_dict.get("Claim", f"{name} is known for engaging content and authenticity.")
            confidence_score = int(details_dict.get("ConfidenceScore", 75))
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            logging.error(f"Error processing OpenAI response: {str(e)}")

            handle = f"@{name.replace(' ', '').lower()}"
            followers_count = 100
            description = f"{name} is a new influencer gaining traction."
            category = "General"
            claim_text = f"{name} is known for engaging content and authenticity."
            confidence_score = 75

        base_handle = handle
        count = 1
        while db.query(Influencer).filter(Influencer.handle == handle).first():
            handle = f"{base_handle}_{count}"
            count += 1


        influencer = Influencer(
            name=name,
            handle=handle,
            followers_count=followers_count,
            description=description,
            category=category,
        )
        db.add(influencer)
        db.commit()
        db.refresh(influencer)


        claim = Claim(
            claim_text=claim_text,
            confidence_score=confidence_score,
            influencer_id=influencer.id,
        )
        db.add(claim)
        db.commit()

        return {
            "message": "Influencer y claim creados.",
            "influencer_id": influencer.id,
            "claim_id": claim.id,
        }

    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error.")
