import os
import sys

import waitress

from flask_app.app import app

if __name__ == "__main__":
    if sys.argv[1] == "debug":
        app.run(debug=True)

    if sys.argv[1] == "production":
        waitress.serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
