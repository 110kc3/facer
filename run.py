#! /usr/bin/env python
import os
from app import app
app.run(debug=True, host="localhost", port=int(os.environ.get("PORT", 5000)))
