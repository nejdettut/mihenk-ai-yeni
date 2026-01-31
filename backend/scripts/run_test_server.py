import sys
import os
from pathlib import Path
import uvicorn
import importlib

# Ensure backend path is on sys.path so we can import `app`
backend_root = str(Path(__file__).resolve().parents[1])
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

# Test-mode server (uses TEST_MODE=1 internally)
os.environ['TEST_MODE'] = '1'

if __name__ == '__main__':
    # load app module directly to avoid import path issues
    app_module = importlib.import_module('app.main')
    app = getattr(app_module, 'app')
    uvicorn.run(app, host='127.0.0.1', port=8001, log_level='info')
