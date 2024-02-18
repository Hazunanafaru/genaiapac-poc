"""Module providing main initial functionality"""
import logging
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

    if app.config['DEBUG']:
        logging.getLogger().setLevel(logging.DEBUG)
        app.run(debug=True)

    app.run(host="0.0.0.0", debug=False)

if __name__ == '__main__':
    main()
