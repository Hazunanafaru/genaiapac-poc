"""Module providing main initial functionality"""
import logging
from dotenv import load_dotenv
from llama_cpp import os
from api import init_app

def main():
    """
    Main function
    Run load environment variable from .env and init flask api
    """
    load_dotenv()
    logging.basicConfig()
    logging.getLogger().setLevel(logging.WARNING)
    app = init_app()

    if os.environ.get('DEBUG'):
        logging.getLogger().setLevel(logging.DEBUG)
        app.run(debug=True, port=5000)
    else:
        app.run(host="0.0.0.0", debug=False, port=8080)

if __name__ == '__main__':
    main()
