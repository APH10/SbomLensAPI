import subprocess, time, pytest
@pytest.fixture(scope='session')
def api_base_url():
    proc = subprocess.Popen(['python','tests/mock_server.py'])
    time.sleep(1.5)
    try:
        yield 'http://127.0.0.1:5000/api'
    finally:
        proc.terminate(); proc.wait()
