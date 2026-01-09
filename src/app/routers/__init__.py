from .start import router as start_router
from .translate import router as translate_router
from .errors import router as errors_router

all_routers = [errors_router, start_router, translate_router]

