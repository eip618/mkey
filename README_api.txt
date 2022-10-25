1. Run `pip install -r requirements.txt`
    - might be `pip3` depending on OS
2. Run `python3 -m uvicorn api:app --port=<a port of your choice> --host=<ip of your choice>`
    - `--host` is not required, unless you need to host on an IP that is not the same as localhost
    - `--port` is not required, and is 8000 by default. If 8000 is used already, pick another port.
    - you'll want to do this in the background, in any way you prefer, systemd or otherwise
3. Reverse proxy to said host:port

The API is accessed by requesting GET to `http://example.com/<platform>/<inquiry>/<month>/<day>`.
