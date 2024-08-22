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
from fastapi.staticfiles import StaticFiles

import mkey


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

async def get_mkey(platform: Optional[str] = None, month: Optional[int] = None, day: Optional[int] = None, inquiry: Optional[str] = None, aux: Optional[str] = None) -> int:
    generator = mkey.mkey_generator(debug=False)

    if platform not in ["RVL", "TWL", "CTR", "WUP", "HAC"]:
        raise mkey.InvalidInputError(f"{platform} is an invalid platform.")
    master_key = None
    try:
        master_key = generator.generate(inquiry=inquiry, month=month, day=day, device=platform, aux=aux)
    except mkey.InvalidInputError as e:
        raise mkey.InvalidInputError(str(e))
    except ValueError as e:
        raise ValueError(str(e))
    return str(master_key)


@app.get("/api")
async def api(platform: Optional[str] = None, month: Optional[int] = None, day: Optional[int] = None, inquiry: Optional[str] = None, aux: Optional[str] = None):
    try:
        ret = await get_mkey(platform, month, day, inquiry, aux)
    except mkey.InvalidInputError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"key": int(ret)}


@app.get("/", include_in_schema=False)
async def webpage(platform: Optional[str] = None, month: Optional[int] = None, day: Optional[int] = None, inquiry: Optional[str] = None, aux: Optional[str] = None):
    if all(i is None for i in [platform, month, day, inquiry, aux]):
        with open("index.html", 'r') as f:
            return HTMLResponse(f.read())

    with open("index.html", 'r') as f:
        try:
            ret = await get_mkey(platform, month, day, inquiry, aux)
        except ValueError as e:
            return HTMLResponse(f.read().replace("<h4>DSi/ 3DS / Wii / Wii U / Switch parental controls master key generator.<br>", f"<h3>Error: {str(e)}</h3>"))
        return HTMLResponse(f.read().replace("<h4>DSi/ 3DS / Wii / Wii U / Switch parental controls master key generator.<br>", f"<h3>Your key is {ret}.</h3>"))
