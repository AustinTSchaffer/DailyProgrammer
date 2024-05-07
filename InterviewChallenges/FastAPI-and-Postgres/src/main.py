from . import constants

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.app:app",
        host="0.0.0.0",
        port=constants.APP_PORT,
        reload=constants.APP_RELOAD,
    )
