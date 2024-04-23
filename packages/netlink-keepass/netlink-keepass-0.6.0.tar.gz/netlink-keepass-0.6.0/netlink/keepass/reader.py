import os
import pathlib
import signal

import fastapi
import uvicorn

from netlink.keepass.keepass import KeePass

app = fastapi.FastAPI()


# noinspection PyUnresolvedReferences
@app.get("/{full_path:path}")
async def get_value(full_path: str):
    if full_path.startswith(app.state.shutdown):
        os.kill(os.getpid(), signal.SIGTERM)
        return fastapi.Response(status_code=200, content="Server shutting down...")
    try:
        return app.state.kp.get(full_path)
    except KeyError:
        raise fastapi.HTTPException(status_code=404, detail=f"{full_path} not found")


# noinspection PyUnresolvedReferences
def reader(
        filename: pathlib.Path,
        secret: str,
        keyfile: pathlib.Path = None,
        token: pathlib.Path = None,
        port: int = 8666,
        shutdown: str = "_shutdown",
) -> None:
    """Start REST server to read KeePass

    :param filename: KeePass Database file
    :param secret: Password for KeePass database or Key for Fernet
    :param keyfile: KeePass key file
    :param token: Fernet token file
    :param port: Server port
    :param shutdown: URL path to shutdown server
    """
    app.state.kp = KeePass(
        filename=filename, secret=secret, keyfile=keyfile, token=token
    )
    app.state.shutdown = shutdown
    uvicorn.run(app, port=port, log_level="info")
