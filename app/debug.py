# just a debug wrapper for the app to make it easier to debug in nvim
import uvicorn
from main import app
import debugpy

if __name__ == "__main__":
    debugpy.listen(("localhost", 5678))
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
