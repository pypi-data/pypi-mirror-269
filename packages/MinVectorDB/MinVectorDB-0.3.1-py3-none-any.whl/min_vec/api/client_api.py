from min_vec.api.http_api import *


def start_server(host='127.0.0.1', port=7637):
    """
    Start the MinVectorDB server.

    Parameters:
        host (str, optional): The host address to bind the server. Defaults to
            '127.0.0.1'.
        port (int, optional): The port number to bind the server. Defaults to 7637.

    """
    app.run(host=host, port=port, debug=True)

    return
