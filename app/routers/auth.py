from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
)

@router.post('/login')
def login(user_credintials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credintials.username).first() # type: ignore

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credintials')
    
    if not utils.verify_password(user_credintials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid Credintials')
    
    #create token
    access_token = oauth2.create_access_token( data = {'user_id': user.id})
    #return token
    return {"access_token" : access_token, "token_type": "bearer"}
