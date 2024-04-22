# SharedKernel
this a shared kernel package

# Create Package
    py -m pip install --upgrade build
    py -m build
    cd dist
    py -m pip install --upgrade twine
    py -m twine upload dist/*

# Pypi
pip install sharedkernel==1.0.0
# Sample Code
```python 
    from fastapi import FastAPI,Depends

    from sharedkernel import jwt_service
    from sharedkernel.objects import JwtModel
    from sharedkernel import config
    app = FastAPI(title="Sample Apis",dependencies=[Depends(jwt_service.JWTBearer(JwtModel(secret_key=config.JWT_SECRETKEY,
                                                                                        algorithms=config.JWT_ALGORITHM,
                                                                                        audience=config.JWT_AUDIENCE,
                                                                                        issuer=config.JWT_ISSURE)))])
```