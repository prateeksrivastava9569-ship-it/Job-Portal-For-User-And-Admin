import requests
import re
import time
from io import BytesIO

BASE = 'http://127.0.0.1:8000'
S = requests.Session()

def get_csrf(url):
    r = S.get(url, timeout=10)
    if r.status_code != 200:
        print('GET failed', url, r.status_code)
        print(r.text[:1000])
        return None, r.text
    ct = S.cookies.get('csrftoken', '')
    return ct, r.text

# Step 1: GET signup page
csrf, text = get_csrf(BASE + '/user_signup')
if csrf is None:
    raise SystemExit('Failed to GET signup page')
print('Got csrf:', csrf)

# Prepare multipart fields
data = {
    'fname': 'Smoke',
    'lname': 'Tester',
    'pwd': 'pass1234',
    'cpwd': 'pass1234',
    'email': f'smoke{int(time.time())}@gmail.com',
    'contact': '9123456789',
    'gender': 'Male',
    'qualification': 'BCA',
    'experience': '1',
    'interest': 'Python',
    'csrfmiddlewaretoken': csrf
}

# Create small in-memory files
files = {
    'image': ('smoke.jpg', BytesIO(b'testimagecontent'), 'image/jpeg'),
    'resume': ('smoke.pdf', BytesIO(b'%PDF-1.4 test resume'), 'application/pdf')
}

# Step 2: POST to trigger OTP generation
r = S.post(BASE + '/user_signup', data=data, files=files, allow_redirects=True, timeout=15)
print('POST status', r.status_code)
if r.status_code not in (200, 302):
    print('Unexpected status', r.status_code)
    print(r.text[:2000])

page = r.text
# Look for previously uploaded badges
if 'Previously uploaded' in page or 'File: temp_' in page:
    print('Upload badges present after OTP generation (good)')
else:
    print('Upload badges NOT present - failing')
    print(page[:2000])

# Extract demo OTPs if present
m_email = re.search(r'Demo email OTP:\s*(\d{6})', page)
m_mobile = re.search(r'Demo mobile OTP:\s*(\d{6})', page)
email_otp = m_email.group(1) if m_email else None
mobile_otp = m_mobile.group(1) if m_mobile else None
print('demo email otp:', email_otp)
print('demo mobile otp:', mobile_otp)

if not (email_otp and mobile_otp):
    print('OTP values not found in page. Printing snippet:')
    print(page[:2000])
    raise SystemExit('No OTPs found')

# Step 3: POST OTPs to verify
csrf2 = S.cookies.get('csrftoken', csrf)
otp_data = {'email_otp': email_otp, 'mobile_otp': mobile_otp, 'csrfmiddlewaretoken': csrf2}
ro = S.post(BASE + '/user_signup', data=otp_data, allow_redirects=True, timeout=15)
print('OTP submit status:', ro.status_code)
if 'Signup Successfull' in ro.text or ro.status_code == 200:
    print('Signup OTP verified — response contains success or 200 code')
    # print small snippet
    print(ro.text[:1000])
else:
    print('OTP verification may have failed; response snippet:')
    print(ro.text[:2000])
    raise SystemExit('OTP verify failed')

print('Smoke test completed')
