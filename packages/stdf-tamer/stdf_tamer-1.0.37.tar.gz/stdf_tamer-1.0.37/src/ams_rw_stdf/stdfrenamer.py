"""Renames stdf based on MIR conntent

This has the full power of python fstring formating...


Usage:
  stdfrenamer <stdf_file_name_in>  --format="{MIR_LOT_ID}_{MIR_PART_TYP}.stdf" [--check-convention] [--ignore-last-chars=0]

Options:
  -h --help               Show this screen.
  --format="fmt string"   A python fstring type format string. The modules datetime, zoneinfo, uuid and random are available
  --check-convention      dont rename just check if the name is in compliance
  --ignore-last-chars=0  Only relevant when checking the convention. Decides how many of the last characters shall be ignored on comparison. 
  stdf_file_name_in       python globs are allowed to select multiple input files (https://docs.python.org/3/library/glob.html)

"""



import ams_rw_stdf
from docopt import docopt
from ams_rw_stdf._opener_collection import _opener
import pathlib
import shutil
import glob
import datetime
import zoneinfo
import uuid
import random
import rich
from rich.console import Console
error_console = Console(stderr=True, style="bold red")
console = Console()


def worker(iFilename, fmt, check_compliance, ignoreLastDigits):
    ftype = pathlib.Path(iFilename).suffix
    dest = None
    globals_for_eval = {"datetime": datetime,
                        "zoneinfo": zoneinfo,
                        "uuid": uuid,
                        "random": random}
    with _opener[ftype](iFilename, "rb") as f:
        parser = ams_rw_stdf.compileable_RECORD.compile()
        while True:
             b = ams_rw_stdf.get_record_bytes(f)
             c = parser.parse(b)
             if c.REC_TYP == 1 and c.REC_SUB == 10:
                globals_for_eval = globals_for_eval | {f"MIR_{key}": value for key, value in dict(c.PL).items()}
                break
    filename = eval(fmt, globals_for_eval)
    if check_compliance:
        if not iFilename[:-1*ignoreLastDigits].endswith(filename[:-1*ignoreLastDigits]):
            error_console.print(f"rules violated: {iFilename}/{filename}")
        else:
            console.print(f"{iFilename} OK")
    else:
        dest = pathlib.Path(filename).expanduser().absolute()
        dest.parents[0].mkdir(parents=True, exist_ok=True)
        shutil.copy(iFilename, dest)


def main():
    arguments = docopt(__doc__)
    fmt = arguments["--format"]
    fmt = f'f"{fmt}"'
    for item in glob.iglob(arguments["<stdf_file_name_in>"], recursive=True):
        worker(item, fmt, arguments["--check-convention"], int(arguments["ignore-last-chars"]))
        

if __name__ == '__main__':
    main()

