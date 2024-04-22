from fastapi import FastAPI,Depends

from sharedkernel import jwt_service
from sharedkernel.objects import JwtModel
from sharedkernel import config
app = FastAPI(title="Domain Apis",dependencies=[Depends(jwt_service.JWTBearer(JwtModel(secret_key=config.JWT_SECRETKEY,
                                                                                       algorithms=config.JWT_ALGORITHM,
                                                                                       audience=config.JWT_AUDIENCE,
                                                                                       issuer=config.JWT_ISSURE)))])

# history = api_client.bots()
# print("Chat history:", history)