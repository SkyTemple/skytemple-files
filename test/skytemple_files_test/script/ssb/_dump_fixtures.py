import os
import shutil
from glob import glob

p = "/home/marco/dev/skytemple/skytemple/__scripts/"
out = os.path.join(os.path.dirname(__file__), "fixtures")
os.makedirs(out, exist_ok=True)


def copy(fname: str):
    without_p = fname.removeprefix(p)
    game_name, level_name, _ = without_p.split("/")
    splits = os.path.basename(fname).split(".")
    script_name, ext = splits[0], splits[-1]
    region = "us"
    if game_name == "SUBS_EXPS":
        game_name = "SUBS_SSB"
    if ext == "ssb":
        print(game_name, level_name, script_name, ext)
        if game_name == "Pichus_fate_script" and not os.path.exists(fname.removesuffix(".ssb") + ".exps"):
            return
        if level_name == "COMMON":
            outname = os.path.join(out, f"{game_name}_{level_name}_{script_name}.{region}.ssb")
        else:
            outname = os.path.join(out, f"{level_name}_{script_name}.{region}.ssb")
        if not os.path.exists(outname):
            shutil.copy(fname, outname)
    if ext == "exps":
        print(game_name, level_name, script_name, ext)
        if level_name == "COMMON":
            outname = os.path.join(out, f"{game_name}_{level_name}_{script_name}.exps")
        else:
            outname = os.path.join(out, f"{level_name}_{script_name}.exps")
        if not os.path.exists(outname):
            shutil.copy(fname, outname)


for fname in glob(os.path.join(p, "**/**/*")):
    copy(fname)
