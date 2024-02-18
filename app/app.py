from desktop_wrapper import BaseApp
from api.v1 import api_blueprint

app: BaseApp = BaseApp(
    '',
    __name__,
    static_folder='./assets',
    template_folder='./templates'
)

app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.start(gui=False, debug=True, port="4000")
