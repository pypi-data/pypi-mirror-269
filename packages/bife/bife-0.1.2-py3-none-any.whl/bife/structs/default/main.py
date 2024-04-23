import uvicorn
from config import get_config

if __name__ == '__main__':
    config = get_config()
    uvicorn.run(
        'app:app',
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True,
    )
