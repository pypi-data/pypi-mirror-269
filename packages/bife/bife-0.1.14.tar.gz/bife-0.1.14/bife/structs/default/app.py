from libs.api.api_handler import ApiHandler
from libs.bootstrap.bootstrap import Bootstrap

app = ApiHandler()
Bootstrap().setup_fastapi_app(app)
