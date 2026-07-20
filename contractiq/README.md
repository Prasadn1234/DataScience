# ContractIQ

Streamlit app that lets a user paste contract text and get a structured AI
analysis: parties, key dates, obligations, risky clauses, and a summary.

## Running in Google Colab

Streamlit apps must be launched via the `streamlit run` CLI, not imported and
called directly — running `app.main()` (or `!python app.py`) inside the
notebook kernel produces a `missing ScriptRunContext!` warning and won't
serve a UI. Colab also doesn't expose localhost ports directly, so the
Streamlit server needs to be tunneled out.

```python
# 1. Install deps
!pip install -q streamlit pyngrok

import os
from pyngrok import ngrok

# 2. Set ngrok auth token (from Colab Secrets, or paste directly)
NGROK_AUTH_TOKEN = os.environ.get("NGROK_AUTH_TOKEN")
if not NGROK_AUTH_TOKEN:
    print("NGROK_AUTH_TOKEN not found in environment variables. Please set it in Colab Secrets or define it directly.")
    # ngrok.set_auth_token("YOUR_AUTHTOKEN")
else:
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# 3. Launch Streamlit as a background process (not imported/called directly)
!streamlit run contractiq/app.py --server.port 8501 &> logs.txt &

# 4. Expose the port (Colab doesn't let you hit localhost directly)
public_url = ngrok.connect(8501)
print(public_url)
```

Get an ngrok authtoken (free account) at
https://dashboard.ngrok.com/get-started/your-authtoken. Prefer not to sign up
for ngrok? Use `localtunnel` instead, no account required:

```python
!streamlit run contractiq/app.py --server.port 8501 &> logs.txt &
!npx --yes localtunnel --port 8501
```
