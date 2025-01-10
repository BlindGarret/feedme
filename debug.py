# just a debug wrapper for the app
import sys
import uvicorn

sys.path.insert(0, "../app")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=True)
