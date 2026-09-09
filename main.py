import os
import sys
import time
import urllib.request
import subprocess
from pathlib import Path

try:
    from pyngrok import ngrok
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"pyngrok not installed: {exc}. Run: python -m pip install pyngrok")

BASE_DIR = Path(__file__).resolve().parent


def wait_for_http(url: str, timeout: int = 30):
    deadline = time.time() + timeout
    last_error = None
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                return response.status < 500
        except Exception as exc:  # pragma: no cover
            last_error = exc
            time.sleep(1)
    raise RuntimeError(f"Site did not start in time at {url}: {last_error}")


def port_is_open(host: str = '127.0.0.1', port: int = 8000):
    try:
        with urllib.request.urlopen(f'http://{host}:{port}', timeout=2):
            return True
    except Exception:
        return False


def start_django_server():
    if port_is_open():
        return None
    env = os.environ.copy()
    cmd = [sys.executable, 'manage.py', 'runserver', '0.0.0.0:8000']
    proc = subprocess.Popen(cmd, cwd=str(BASE_DIR), env=env)
    wait_for_http('http://127.0.0.1:8000')
    return proc


def main():
    token = os.environ.get('NGROK_AUTHTOKEN')
    if not token:
        raise SystemExit('NGROK_AUTHTOKEN is required. Example: $env:NGROK_AUTHTOKEN="..."; python main.py')

    ngrok.set_auth_token(token)
    server = start_django_server()
    tunnel = ngrok.connect(8000, 'http', bind_tls=True)
    print(f'Public URL: {tunnel.public_url}')
    if server is not None:
        print('Django server PID:', server.pid)
    try:
        if server is not None:
            server.wait()
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        print('Stopping server and tunnel...')
        if server is not None:
            server.terminate()
        ngrok.kill()


if __name__ == '__main__':
    main()
