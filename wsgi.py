#!/usr/bin/env python
import os
from app import schedule_app as application
import app

if __name__ == "__main__":
  app.sanity_checks()
  application.run(debug=True)