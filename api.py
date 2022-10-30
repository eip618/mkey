#!/usr/bin/python3

#
# mkey API wrapper
#
# SPDX-License-Identifier: CC0-1.0
#
# mkey is licensed AGPL 3.0.
#

from typing import Optional, Union
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

import mkey


app = FastAPI()


@app.get("/")
async def get_mkey(request: Request, platform: Optional[str] = None, month: Optional[int] = None, day: Optional[int] = None, inquiry: Optional[str] = None, aux: Optional[str] = None):
    if all(i is None for i in [platform, month, day, inquiry, aux]):
        with open("index.html", 'r') as f:
            return HTMLResponse(f.read())


    generator = mkey.mkey_generator(debug=False)

    if platform not in ["RVL", "TWL", "CTR", "WUP", "HAC"]:
        raise HTTPException(status_code=400, detail=f"{platform} is an invalid platform.")
    master_key = None
    try:
        master_key = generator.generate(inquiry=inquiry, month=month, day=day, device=platform, aux=aux)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


    contenttype = request.headers.get("Content-Type")
    if contenttype == "application/json":
        return {"key": master_key}
    else:
        with open("index.html", 'r') as f:
            return HTMLResponse(f.read().replace("<h4>DSi/ 3DS / Wii / Wii U / Switch parental controls master key generator.<br>", f"<h3>Your key is {master_key}.</h3>"))
