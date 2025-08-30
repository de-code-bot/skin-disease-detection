from typing import Final

from backend.app import create_app

from quart import Quart

def main() -> None:
    app: Final[Quart] = create_app()
    app.run(app.config['HOST'], port=app.config['PORT'], debug=True)

if __name__ == '__main__':
    main()