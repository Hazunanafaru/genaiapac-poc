"""Module providing main initial functionality"""
import os, logging
from dotenv import load_dotenv
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
        app.run(debug=True, port=8080)
    else:
        app.run(host="0.0.0.0", debug=False, port=8080)

if __name__ == '__main__':
    main()
