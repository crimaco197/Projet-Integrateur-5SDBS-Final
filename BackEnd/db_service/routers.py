from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from concurrent.futures import ThreadPoolExecutor
from models import blacklist, reliability
from database import get_db
from schemas import reliabilityModel,ReliabilityCreate

router = APIRouter()

def check_in_blacklist(url: str, db: Session= Depends(get_db)):
    """Recherche dans la table blacklist."""
    return db.query(blacklist).filter(blacklist.nom == url).first()

def check_in_reliability(url: str, db: Session= Depends(get_db)):
    """Recherche dans la table rate."""
    return db.query(reliability).filter(reliability.url == url).first()

@router.get("/check/", response_model=reliabilityModel)
def check_blacklist_and_reliability(url: str, db: Session = Depends(get_db)):
    print(f"url:{url}")
    
    blacklist_match = check_in_blacklist(url, db)
    reliability_match = check_in_reliability(url, db)

    # Si trouvé dans blacklist, supprimer de rate
    if blacklist_match:
        #if reliability_match:
            #db.delete(reliability_match)
            #db.commit()
        return {"prediction": "mal", "confidence": 100}

    # Si trouvé dans rate, supprimer de blacklist
    if reliability_match:
        #if blacklist_match:
            #db.delete(blacklist_match)
            #db.commit()
        return {"prediction": reliability_match.prediction, "confidence": reliability_match.confidence}

    # Si l'URL n'est trouvée nulle part
    return {"prediction": "not_found", "confidence": -1}


@router.post("/add/")
def add_reliability(record: ReliabilityCreate, db: Session = Depends(get_db)):
    new_record = reliability(
        url=record.url,
        prediction=record.prediction,
        confidence=record.confidence
    )

    # add new data into database
    db.add(new_record)
    db.commit()
    db.refresh(new_record)  # refresh to get new id auto-incrementing

    return {"id": new_record.id, "message": "Record added successfully"}
