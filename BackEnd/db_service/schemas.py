from pydantic import BaseModel
#from typing import List, Optional

# Request to add rate
#class addRate(BaseModel):
 #   url: str
  #  rate: str

class reliabilityModel(BaseModel):
    prediction: str
    confidence: int

class ReliabilityCreate(BaseModel):
    url: str
    prediction: str
    confidence: int

# Model type Pydantic pour recuperer les reponse de requetes
#class BlacklistSiteResponse(BaseModel):
 #   id: int
  #  nom: str
   # categorie: str

    #class Config:
     #   orm_mode = True


