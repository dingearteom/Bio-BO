from compare.visualization.dash_server.app import app
from compare.visualization.dash_server.comparison_call_backs import *


if __name__ == '__main__':
    app.run_server(debug=True)