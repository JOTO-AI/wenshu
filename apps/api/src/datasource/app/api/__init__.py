from fastapi import APIRouter
from .v1 import api_router as v1_router

router = APIRouter()

# 包含v1版本的API
router.include_router(v1_router, prefix="/v1")

# 默认版本指向v1
# router.include_router(v1_router, prefix="")
