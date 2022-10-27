#!/usr/bin/python3

#
# mkey API wrapper
#
# SPDX-License-Identifier: CC0-1.0
#
# mkey is licensed AGPL 3.0.
#

from fastapi import FastAPI, HTTPException

import mkey


app = FastAPI()


@app.get("/{platform}/{inquiry}/{month}/{day}")
async def get_mkey(platform: str, month: int, day: int, inquiry: str, aux: str = ""):

    generator = mkey.mkey_generator(debug=False)

    if platform not in ["RVL", "TWL", "CTR", "WUP", "HAC"]:
        raise HTTPException(status_code=400, detail=f"{platform} is an invalid platform.")
    master_key = None
    try:
        master_key = generator.generate(inquiry=inquiry, month=month, day=day, device=platform, aux=aux)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {"key": master_key}
