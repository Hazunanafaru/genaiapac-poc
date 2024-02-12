from api import init_api
from dotenv import load_dotenv

def main():
    """
    Main function
    Run load environment variable from .env and init flask api
    """
    load_dotenv()
    init_api()

if __name__ == '__main__':
    main()
