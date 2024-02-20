from desktop_wrapper import BaseApp
from api.v1 import api_blueprint
from api.db_engine import Engine

app: BaseApp = BaseApp(
    '',
    __name__,
    static_folder='./assets',
    template_folder='./templates'
)

app.register_blueprint(api_blueprint)

app.config['ENGINE'] = Engine()


if __name__ == '__main__':
    app.start(gui=False, debug=True, port="4000", host="0.0.0.0")
