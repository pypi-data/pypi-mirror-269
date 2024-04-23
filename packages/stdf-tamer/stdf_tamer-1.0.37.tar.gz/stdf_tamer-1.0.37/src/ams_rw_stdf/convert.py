"""stdfconvert

Usage:
  stdfconvert end2end <inglob> <outdir> <format>
  stdfconvert pickle2format <outfile> <format>
  stdfconvert stdf2pickle


"""
import os
import rich
import rich.progress
import subprocess
from rich.progress import Progress
import time
import glob
import pathlib
import sys
import ams_rw_stdf
import collections
import pickle
import threading
import queue
from docopt import docopt
import toml
import sys
import ams_rw_stdf
import collections
import pickle
import threading
import queue
import shutil
from rich.console import Console
error_console = Console(stderr=True, style="bold red")
import base64
import logging


logging.basicConfig(level=logging.INFO)
_min_version = "1.0.21"
_base64_marker = "base64://"


def convert_list_of_files(fileGlob, outdir, format="parquet"):
    if isinstance(fileGlob, str):
        flist = glob.iglob(fileGlob)
    else:
        flist = fileGlob
    if format == "pickle":
        pass
    elif format in {"parquet", "xlsx", "feather", "ipc"}:
       try:
           import polars as pl
           import pyarrow
       except ImportError:
            logging.error(f"""Conversion to {format} impossible due to missing dependencies. Please install stdftamers optional dependancies.

in case of the usage of pdm.:
pdm add stdf-tamer[fileformats]

in case of usage of pipx
pipx inject stdf-tamer stdf-tamer[fileformats]

""")
            sys.exit(1)

    stdf_to_pickle_cmd   = f""""{sys.executable}" -m  ams_rw_stdf.convert stdf2pickle"""
    typical7zLocations = ["7z", "7Z", f"{os.getenv('ProgramFiles(x86)')}/7-Zip/7z.exe", f"{os.getenv('ProgramFiles')}/7-Zip/7z.exe"]
    sevenZLocations = [shutil.which(item) for item in typical7zLocations]
    sevenZLocations = [item for item in sevenZLocations if item is not None]
    if sevenZLocations:
        sevenZ = sevenZLocations[0]
        gzip_handler = f"\"{sevenZ}\" e -tgzip -si -so"
        bzip_handler = f"\"{sevenZ}\" e -tbzip -si -so"
        xz_handler = f"\"{sevenZ}\" e -txz -si -so"
    else:
        gzip_handler         = shutil.which("zcat")
        bzip_handler         = shutil.which("bzcat")
        xz_handler           = shutil.which("unxz")
    
    max_running_conversions = os.cpu_count()/2
    for configfile in ["/etc/stdf-tamer.toml", pathlib.Path(os.path.expanduser("~")) / ".config/stdf-tamer.toml"]:
        try:
            config = toml.load(configfile)
            if "max_running_conversions" in config["converter"]:
                max_running_conversions   = config["converter"]["max_running_conversions"]
            if "stdf_to_pickle_cmd" in config["converter"]:
                stdf_to_pickle_cmd   = config["converter"]["stdf_to_pickle_cmd"]
            if "zcat" in config["converter"]:
                 gzip_handler = config["converter"]["zcat"]
            if "bzcat" in config["converter"]:
                 bzip_handler = config["converter"]["bzcat"]
            if "unxz" in config["converter"]:
                 xz_handler = config["converter"]["unxz"]
        except FileNotFoundError as e:
            logging.info(f"config file not found: {e} if this is intentionall... dont worry..")
            pass
        except KeyError:
            logging.error(f"error accessing config object... this should not happen! {e}")
        except Exception as e:
            logging.error(f"Unexpected error loading configuration... this should not happen! {e}")
    
    logging.info(f"""Configuration loaded.:
stdf_to_pickle_cmd:      {stdf_to_pickle_cmd}
gzip_handler:            {gzip_handler}
bzip_handler:            {bzip_handler}
xz_handler:              {xz_handler }
max_running_conversions: {max_running_conversions}
""")

    picke_to_parquet_cmd = f""""{sys.executable}" -m  ams_rw_stdf.convert pickle2format"""

    if not xz_handler:
        error_console.print("Unable to find xz decompression tool. Please install/configure 7z/unxz")
    if not bzip_handler:
        error_console.print("Unable to find bzip2 decompression tool. Please install/configure 7z/bzcat")
    if not gzip_handler:
        error_console.print("Unable to find gz decompression tool. Please install/configure 7z/zcat")

    if not flist:
        error_console.print("No files to convert")
    with Progress(rich.progress.TimeElapsedColumn(),
                  rich.progress.DownloadColumn(), rich.progress.BarColumn(),
                  rich.progress.TransferSpeedColumn(),
                  rich.progress.TimeRemainingColumn(),
                  rich.progress.TextColumn("[progress.description][red]{task.description}")) as progress:

        def get_file_size(item):
            return os.stat(item).st_size

        def _worker(outdir, flist):
            outdir = pathlib.Path(outdir).resolve()
            for fname in flist:
                file = open(fname, "rb")
                task = progress.add_task(f"{pathlib.Path(fname).name}", total=os.stat(fname).st_size)
                fnameShort = pathlib.Path(fname).name
                if fname.endswith(".stdf.xz"):
                    ofname = outdir / f"{fnameShort[:-8]}"
                    oFilePath = _base64_marker + base64.b64encode(str(pathlib.Path(f"{ofname}.{format}").absolute()).encode()).decode()
                    yield (file, f"""{xz_handler}  | {stdf_to_pickle_cmd} | {picke_to_parquet_cmd} "{oFilePath}" {format}""", task)
                elif fname.endswith(".stdf.gz"):
                    ofname = outdir / f"{fnameShort[:-8]}"
                    oFilePath = _base64_marker + base64.b64encode(str(pathlib.Path(f"{ofname}.{format}").absolute()).encode()).decode()
                    yield (file, f"""{gzip_handler}  | {stdf_to_pickle_cmd} | {picke_to_parquet_cmd} {oFilePath}  {format}""", task)
                elif fname.endswith(".stdf") or fname.endswith(".std"):
                    ofname = outdir / f"{fnameShort[:-5]}"
                    oFilePath = _base64_marker + base64.b64encode(str(pathlib.Path(f"{ofname}.{format}").absolute()).encode()).decode()
                    yield (file, f"""{stdf_to_pickle_cmd} | {picke_to_parquet_cmd} "{oFilePath}" {format}""", task)
                elif fname.endswith(".stdf.bz"):
                    ofname = outdir / f"{fnameShort[:-8]}"
                    oFilePath = _base64_marker + base64.b64encode(str(pathlib.Path(f"{ofname}.{format}").absolute()).encode()).decode()
                    yield (file, f"""{bzip_handler}  | {stdf_to_pickle_cmd} | {picke_to_parquet_cmd} "{oFilePath}" {format}""", task)

        processes2run = _worker(outdir, flist)
        running_processes = []

        for (file, cmd, task) in processes2run:
            running_processes.append((file, subprocess.Popen(cmd, shell=True, stdin=file, stdout=subprocess.PIPE, stderr=subprocess.STDOUT), task))
            while len(running_processes) >= max_running_conversions:
                time.sleep(0.01)
                running_processes = list(work_process_conversion_process(running_processes, progress))

        while running_processes:
            time.sleep(0.01)
            running_processes = list(work_process_conversion_process(running_processes, progress))

def work_process_conversion_process(running_processes, progress):
    for (file, process, task) in running_processes:
        progress.update(task, completed=file.tell())
        pPoll = process.poll()
        if pPoll == None:
            yield (file, process, task)
        else:
            progress.remove_task(task)
            file.close()
            stdout = process.stdout.read()
            if stdout or process.returncode != 0:
                progress.console.print(f"Abnormality when processing {file.name}")
                if stdout:
                    progress.console.print(f"Unusual stdout:{os.linesep}{stdout.decode()} ")
                if process.returncode != 0:
                    progress.console.print(f"Unusual returncode: {process.returncode} ")

def pickle2X(options):
    try:
        import polars as pl

        schema = [('Test_Nr', pl.UInt32),
                  ('Test_Name', pl.Utf8),
                  ('ULim', pl.Float32),
                  ('LLim', pl.Float32),
                  ('res', pl.Float32),]
    except ImportError as e:
        print('writing parquet failed due to missing dependencies', file=sys.stderr)
        return
    def worker():
        try:
            while True:
                yield pickle.load(sys.stdin.buffer)
        except:
            pass
    worker = worker()
    presented_min_version = next(worker)
    assert _min_version == presented_min_version, f"expected min version {_min_version} received min version {presented_min_version}" 
    (lot_id, test_cod, operator, start_t,  tst_temp, node_nam, job_nam,  sblot_id, floor_id,) = next(worker)

    def worker_():
        for (data, part_id, part_txt, site, head, x, y) in worker:
            df = pl.DataFrame(data, schema=schema)
            df = df.with_columns(pl.lit(part_id).cast(pl.Utf8).alias("part_id"),
                                 pl.lit(part_txt).cast(pl.Utf8).alias("part_txt"),
                                 pl.lit(head).cast(pl.UInt32).alias("head"),
                                 pl.lit(site).cast(pl.UInt32).alias("site"),
                                 pl.lit(x).cast(pl.Int32).alias("X_coord"),
                                 pl.lit(y).cast(pl.Int32).alias("Y_coord"))
            yield df

    df = pl.concat(worker_())
    df = df.with_columns(pl.lit(test_cod).cast(pl.Categorical).alias("TEST_COD"),
                         pl.lit(lot_id).cast(pl.Categorical).alias("lot_id"),
                         pl.lit(operator).cast(pl.Categorical).alias("operator"),
                         pl.lit(start_t).cast(pl.UInt32).alias("START_T"),
                         pl.lit(tst_temp).cast(pl.Categorical).alias("tst_temp"),
                         pl.lit(node_nam).cast(pl.Categorical).alias("node_nam"),
                         pl.lit(job_nam).cast(pl.Categorical).alias("job_nam"),
                         pl.lit(sblot_id).cast(pl.Categorical).alias("sblot_id"),
                         pl.lit(floor_id).cast(pl.Categorical).alias("floor_id"),
                         pl.col("Test_Name").cast(pl.Categorical).alias("Test_Name"),
                         pl.col("part_id").cast(pl.Categorical).alias("part_id"),
                         pl.col("part_txt").cast(pl.Categorical).alias("part_txt"),)

    of = options["<outfile>"]
    if of.startswith(_base64_marker):
        oFile = pathlib.Path(base64.b64decode(of.removeprefix(_base64_marker)).decode())
    else:
        oFile = pathlib.Path(of)
    oFile.parent.mkdir(exist_ok=True)
    
    if options["<format>"] == "xlsx":
        df.write_excel(oFile)
    elif options["<format>"] == "ipc" or options["<format>"] == "feather":
        df.write_ipc(oFile)
    else:
        df.write_parquet(oFile)


def _worker(q):
    b = sys.stdout.buffer
    while True:
            b.write(pickle.dumps(q.get()))
            q.task_done()


def stdf2pickle():
    data =  collections.defaultdict(lambda : [])
    q = queue.Queue(maxsize=20)
    threading.Thread(target=_worker, daemon=True, args=(q,)).start()

    try:
        q.put(_min_version)
        for c in ams_rw_stdf.records_no_length_simplified():
            c = dict(c)
            type_and_subtyp = (c["REC_TYP"], c["REC_SUB"],)
            PL = c["PL"]
            if type_and_subtyp == (15, 10,):
                PL = dict(PL)
                key = (PL["HEAD_NUM"],  PL["SITE_NUM"],)
                data[key].append((PL["TEST_NUM"], PL["TEST_TXT"], PL["HI_LIMIT"], PL["LO_LIMIT"], PL["RESULT"],))
            elif type_and_subtyp == (5, 20,):
                PL = dict(PL)
                key = (PL["HEAD_NUM"], PL["SITE_NUM"])
                data[key].append((None, "SBIN_from_prr_record", None, None, PL["SOFT_BIN"],))
                res = (data[key], PL["PART_ID"], PL["PART_TXT"], PL["SITE_NUM"], PL["HEAD_NUM"], PL["X_COORD"], PL["Y_COORD"])
                q.put(res)
                data[key] = []
            elif type_and_subtyp == (1, 10,):
                PL = dict(PL)
                test_cod = PL["TEST_COD"]
                lot_id   = PL["LOT_ID"]
                operator = PL["OPER_NAM"]
                start_t = PL["START_T"]
                try:
                    floor_id = PL["FLOOR_ID"]
                except:
                    floor_id = "NA"
                try:
                    tst_temp = PL["TST_TEMP"]
                except:
                    tst_temp = "NA"
                    
                q.put((lot_id, test_cod, operator, start_t, tst_temp, PL["NODE_NAM"], PL["JOB_NAM"], PL["SBLOT_ID"], floor_id, ))
            elif type_and_subtyp == (1, 20,):
                q.join()
                exit(0)
    except Exception as e:
        q.join()
        sys.exit(f"unexpected end of stdf (exception: {e})")


def main():
    options = docopt(__doc__)
    if options["stdf2pickle"]:
        stdf2pickle()
    elif options["pickle2format"]:
        pickle2X(options)
    elif options["end2end"]:
        convert_list_of_files(options["<inglob>"], options["<outdir>"], options["<format>"])


if __name__ == "__main__":
    main()
