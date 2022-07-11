import os
"""dotenv.load_dot_env(".env")"""


class Config:
    def __init__(self):
        """Base configuration variables."""
        self.SECRET_KEY = 'SECRET_KEY'
        if not self.SECRET_KEY:
            raise ValueError("No SECRET_KEY set for Flask application. Did you follow the setup instructions?")
