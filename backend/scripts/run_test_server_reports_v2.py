import sys
from pathlib import Path
import os
import importlib
import uvicorn

# Ensure backend path is on sys.path so we can import `app`
backend_root = str(Path(__file__).resolve().parents[1])
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

# Test-mode server (uses TEST_MODE=1 internally)
os.environ['TEST_MODE'] = '1'
os.environ['TEST_MODE_GEN_REPORT'] = '1'

if __name__ == '__main__':
    # Import app module fresh
    if 'app.main' in sys.modules:
        importlib.reload(sys.modules['app.main'])
    app_module = importlib.import_module('app.main')
    app = getattr(app_module, 'app')
    uvicorn.run(app, host='127.0.0.1', port=8003, log_level='info')
