# SPDX-License-Identifer: CC0-1.0


import os
import shutil
import subprocess
import sys


CVerTitles = [
    "000400db00017102",
    "000400db00017202",
    "000400db00017302",
    "000400db00017502"
]


CVerVersions = [
    7203,
    8196,
    8208,
    9218,
    9264,
    9296,
    9319,
    9328,
    9344,
    9360,
    10240,
    10256,
    10272,
    10288,
    10304,
    10320,
    10336,
    10352,
    11264,
    11280,
    11296,
    11312,
    11328,
    11344,
    11360,
    11376,
    11392,
    11408,
    11424,
    11456,
    11472,
    11488,
    11504,
    11520,
    11536
]


def CVerDownload(tid: str, ver: int):
    print(f"Downloading {tid} v.{ver}...")
    dest = f"{tid}-{ver}"
    nustoolarg = f"nustool -m {tid} -V {ver}"
    with open(os.devnull, "w") as devnull:
        subprocess.run(nustoolarg, stdout=devnull)
    cdnciaarg = f"make_cdn_cia {tid}/{ver} {dest}.cia"
    with open(os.devnull, "w") as devnull:
        subprocess.run(cdnciaarg, stdout=devnull)
    ctrtoolarg = f'ctrtool --romfsdir={dest} {dest}.cia'
    with open(os.devnull, "w") as devnull:
        subprocess.run(ctrtoolarg, stdout=devnull)
    try:
        f = open(f"{dest}/masterkey.bin", "rb")
    except FileNotFoundError:
        print(f"TID {tid} v.{ver} has no masterkey, skipping")
        try:
            shutil.rmtree(dest)
        except FileNotFoundError:
            pass
        try:
            os.remove(f"{dest}.cia")
        except FileNotFoundError:
            pass
        return
    head = f.read(2)
    f.close()
    outfile = f"../data/ctr_{head[0]:02x}_{head[1]:02x}.bin"
    if os.path.exists(outfile):
        print(f"{outfile} already exists! Skipping.")
    else:
        shutil.copyfile(f"{dest}/masterkey.bin", outfile)
    shutil.rmtree(dest)
    os.remove(f"{dest}.cia")
    return


if __name__ == "__main__":
    print("CVerScraper")
    print("Requires make_cdn_cia, nustool, ctrtool")
    print("No args to download all known CVers\nargv[1] = TID, argv[2] = titleversion to download specific CVer\n")

    try:
        os.mkdir("../data")
    except FileExistsError:
        pass

    if len(sys.argv) == 3:
        CVerDownload(sys.argv[1], sys.argv[2])
    else:
        for i in CVerTitles:
            for j in CVerVersions:
                CVerDownload(i, j)
