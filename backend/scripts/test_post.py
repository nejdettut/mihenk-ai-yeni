import requests
from pathlib import Path

file_path = Path(__file__).resolve().parents[1] / 'tmp' / 'test.png'
url = 'http://127.0.0.1:8000/api/v1/analyze/full-analysis'
files = {'file': open(file_path, 'rb')}
data = {'exam_id': 'test-exam-id', 'student_id': 'test-student'}
print('Posting file:', file_path)
resp = requests.post(url, files=files, data=data, timeout=120)
print('Status:', resp.status_code)
print('Body:', resp.text)
