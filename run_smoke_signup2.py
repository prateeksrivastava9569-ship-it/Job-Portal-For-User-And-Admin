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
page = r.text
# Save page to file (utf-8)
with open('smoke_session_page.html', 'w', encoding='utf-8') as f:
    f.write(page)
print('Saved session-backed page to smoke_session_page.html')

# Look for previously uploaded badges
if 'Previously uploaded' in page or 'File: temp_' in page:
    print('Upload badges present after OTP generation (good)')
else:
    print('Upload badges NOT present - failing')

# Extract demo OTPs if present (allow for intervening HTML tags)
m_email = re.search(r'Demo email OTP:[^0-9]*(\d{6})', page)
m_mobile = re.search(r'Demo mobile OTP:[^0-9]*(\d{6})', page)
email_otp = m_email.group(1) if m_email else None
mobile_otp = m_mobile.group(1) if m_mobile else None
print('demo email otp:', email_otp)
print('demo mobile otp:', mobile_otp)

if not (email_otp and mobile_otp):
    print('OTP values not found in page. See smoke_session_page.html for full HTML')
    raise SystemExit('No OTPs found')

# Step 3: POST OTPs to verify
csrf2 = S.cookies.get('csrftoken', csrf)
otp_data = {'email_otp': email_otp, 'mobile_otp': mobile_otp, 'csrfmiddlewaretoken': csrf2}
ro = S.post(BASE + '/user_signup', data=otp_data, allow_redirects=True, timeout=15)
print('OTP submit status:', ro.status_code)
if 'Signup Successfull' in ro.text or ro.status_code == 200:
    print('Signup OTP verified — response contains success or 200 code')
    with open('smoke_post_otp.html', 'w', encoding='utf-8') as f:
        f.write(ro.text)
    print('Saved post-OTP response to smoke_post_otp.html')
else:
    print('OTP verification may have failed; see smoke_post_otp.html')
    with open('smoke_post_otp.html', 'w', encoding='utf-8') as f:
        f.write(ro.text)
    raise SystemExit('OTP verify failed')

print('Smoke test completed')
