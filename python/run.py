from base.config import settings

if __name__ == "__main__":
    import uvicorn
    import multiprocessing
    import platform

    if platform.system().lower() == "windows":
        multiprocessing.freeze_support()

    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, workers=settings.WORKERS)
