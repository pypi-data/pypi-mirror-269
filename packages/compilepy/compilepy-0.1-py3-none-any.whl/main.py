"""main.py"""
import uvicorn
from configuration import Configuration

cf = Configuration()

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=cf.server_port, reload=cf.reload)
