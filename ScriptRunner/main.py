from client import app
from config import DEBUG_DASH_APP

if __name__ == "__main__":
    app.run_server(debug=DEBUG_DASH_APP)
