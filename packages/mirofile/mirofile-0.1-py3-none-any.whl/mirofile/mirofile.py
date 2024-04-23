import gzip
import builtins
from pathlib import Path
import traceback
from typing import Literal
from datetime import datetime
from tqdm import tqdm

mcp_columns = ["PH"+str(i) for i in range(7,-1,-1)] + ["PL"+str(i) for i in range(0,8)]
timestamp_columns = ["ts_recv", "ts_sent"]

class _FilePos:
    """ A helper class which tracks the position in a file. """
    def __init__(self):
        self._dict = {"line": None,
                      "line_num": 0}
    def __setitem__(self, key, item):
            if key not in self._dict:
                raise KeyError("FilePos only contains 'line' and 'line_num' keys.")
            self._dict[key] = item
    def __getitem__(self, key):
        return self._dict[key]
    def reset(self):
        self.__init__()

class _FileLikeObj:
    """ A template file-like object implementing standard file methods.
    Some methods are intentionally not implemented and left to the inheriting
    classes to implement. """
    def __init__(self, compression, output_delimiter):
        self._curr_fileobj = None
        self._curr_pos = _FilePos()
        if not compression:
            self._compression = False
        else:
            self._compression = compression
        self._delim = output_delimiter
        self._isopen = False
    
    def __iter__(self):
        line = self.readline()
        while line:
            yield line
            line = self.readline()
    
    def next(self) -> str:
        line = self.readline()
        if not line:
            raise StopIteration
        else:
            return line
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
    
    def close(self):
        self._isopen = False
        self._curr_fileobj.close()
    
    def reset(self):
        self.close()
        self._start()
    
    def read(self, size: int=None, *args, **kwargs) -> str:
        output_bytes = str()
        try:
            if not size:
                while True:
                    output_bytes += self.next()
            else:
                while len(output_bytes) <= size:
                    output_bytes += self.next()
        except StopIteration:
            pass
        finally:
            if not size:
                return output_bytes
            else:
                return output_bytes[:size]

    def readline(self, size: int=None, delim: str=None) -> str:
        if not delim:
            delim = self._delim
        parsed_list = self._advance(parse_ts=False)
        if not parsed_list:
            return ""
        else:
            output_line = delim.join(parsed_list)+"\n"
            if not size or size >= len(output_line):
                return output_line
            else:
                return output_line[:size]
    
    def readlists(self, size: int, parse_ts: bool=False, progress_bar: bool=False) -> list:
        lines = []
        pb = None
        for _ in range(size):
            l = self.readlist(parse_ts=parse_ts)
            if not l:
                break
            else:
                lines.append(l)
                if progress_bar:
                    if not pb:
                        pb = tqdm(total=size, miniters=100)
                    pb.update()
        if progress_bar and pb:
            pb.close()        
        return lines

    def readlist(self, parse_ts: bool=False) -> list:
        return self._advance(parse_ts=parse_ts)

    def _start(self):
        """ Needs to be overriden in an inheriting class. """
        raise NotImplementedError

    def _advance(self, parse_ts: bool=False):
        """ Needs to be overriden in an inheriting class. """
        raise NotImplementedError

class MiroRawFileList(_FileLikeObj):
    """ A wrapper for multiple MIROSLAV files that enables processing them as one. 
    Builds heavily on top of the single file wrapper class, MiroRawFile. """
    def __init__(self, fnamelist: list[str | Path], compression, output_delimiter=";"):
        super().__init__(compression=compression, output_delimiter=output_delimiter)
        self.fnames = sorted([ Path(p).absolute() for p in fnamelist ])
        if not all([ f.exists() for f in self.fnames ]):
            raise FileNotFoundError("One or more files don't exist!")
        self._start()
        self.n_cols = len(self.readlist())
        self.n_mcps = int((self.n_cols-2)/16) # subtract two timestamp columns, the rest is 16 bits/columns per one MCP23017 chip
        self.reset()
    
    def _start(self):
        self._curr_fileobj = MiroRawFile(self.fnames[0], self._compression, self._delim)
        self._curr_pos = self._curr_fileobj._curr_pos

    def _advance(self, parse_ts: bool=False) -> list:
        parsed_list: list = self._curr_fileobj._advance(parse_ts=parse_ts)
        while not parsed_list:
            try:
                self._open_next_file()
            except EOFError:
                parsed_list = []
                break
            else:
                parsed_list: list = self._curr_fileobj._advance(parse_ts=parse_ts)
        self._curr_pos = self._curr_fileobj._curr_pos
        return parsed_list
    
    def _open_next_file(self):
        next_index = self.fnames.index(self._curr_fileobj.fname)+1
        if next_index >= len(self.fnames):
            raise EOFError
        else:
            self.close()
            self._curr_fileobj = MiroRawFile(self.fnames[next_index], self._compression, self._delim)
            self._isopen = self._curr_fileobj._isopen
            self._curr_pos = self._curr_fileobj._curr_pos
            return

class MiroRawFile(_FileLikeObj):
    """Wrapper for raw MIROSLAV files that produces CSV-like output.
    
    The main method is _advance() which reads a new line and runs _parse_line()
    on it, which creates a parsed list of standard MIROSLAV fields.
    readline() outputs this as a string with the specified delimiter.
    """
    def __init__(self, fname: str | Path, compression=None, output_delimiter=";"):
        super().__init__(compression=compression, output_delimiter=output_delimiter)
        self.fname = Path(fname)
        if not self.fname.exists():
            raise FileNotFoundError
        self.fname = fname
        self._start()
        self.n_cols = len(self.readlist())
        self.n_mcps = int((self.n_cols-2)/16) # subtract two timestamp columns, the rest is 16 bits/columns per one MCP23017 chip
        self.reset()
    
    def _start(self):
        if not self._compression:
            self._curr_fileobj = builtins.open(self.fname)
        elif self._compression in ["gzip", "gz"]:
            self._curr_fileobj = gzip.open(self.fname, "rt")
        self._isopen = True
        self._curr_pos.reset()    

    def _advance(self, parse_ts: bool=False) -> list:
        line: str = self._curr_fileobj.readline()
        if not line:
            return []
        self._curr_pos["line"] = line
        self._curr_pos["line_num"] += 1
        parsed_line = self._parse_line(line, parse_ts=parse_ts)
        # print(self.fname.name, self._curr_pos["line_num"], line, parsed_line)
        return parsed_line
    
    def _parse_line(self, line: str, parse_ts: bool=False) -> list:
        # remove trailing whitespace
        line = line.rstrip()
        fields = []
        # Line sanity check:
        #   All of the queried indexes contain characters that should never change,
        # such as time, date and other separators, thus providing a fixed format
        # for each line that can be evaluated. Building a string using only the
        # characters at these indexes should always yield '"--T::.";"START -- ::., END"'
        # If the line is malformed, or an index is out of range, a KeyError is raised.

        # Pre-check:
        #   There is only one situation where the above isn't true, but the line is still valid,
        # and that is if the timestamp falls precisely at .000000 microseconds. If this is
        # the case, the timestamp is missing the entire decimal part. We re-add it, and then
        # perform the standard check as outlined above
        #if f"{line[0]}{line[5]}{line[8]}{line[11]}{line[14]}{line[17]}{line[20:29]}" == '"--T::";"START ':
            #line = f"{line[:20]}.000000{line[20:]}"
        line_list = line[1:].split('";"START ', 1)
        try:
            if len(line_list) != 2:
                raise ValueError
            ts_recv = line_list[0]
            if parse_ts:
                ts_recv = datetime.fromisoformat(line_list[0])
            line_list = line_list[1].split(',')
            if line_list.pop() != ' END"':
                raise ValueError
            ts_sent = line_list.pop(0)
            ts_sent = "".join([ts_sent[:20], ts_sent[20:].zfill(6)])
            if parse_ts:
                ts_sent = datetime.fromisoformat(ts_sent)
            sensor_blocks = line_list
        except KeyError:
            self.__err_malformed_file()
        except ValueError:
            self.__err_malformed_file()
        # remove static characters from start and end
        #line = line[1:-6]
        # start splitting into fields - first is ts_recv
        #fields.append(line[:26])
        # remove ts_recv and split (by comma) into ts_sent and data fields
        #line = line[35:].split(",")
        # sanity check: length of each data field (skip first element because that's ts_sent)
        if any(len(data_field) != 16 for data_field in fields):
            self.__err_malformed_file()
        # get ts_sent from line and reformat it:
        # ts_sent is formed from 3 elements: date, time, microseconds
        # delimited by "T" (ISO 8601) and "." respectively
        # While we're at it, left-fill microseconds.
        # This is because older MIROSLAVs send microseconds as an integer
        # in its own right, and not as the decimal part of seconds.
        # So, "19:19:57.20228" is actually read as two fields,
        # "19:19:57" and "20228", and corresponds to "19:19:57.020228".
        #ts_sent = line.pop(0)
        #ts_sent = f"{ts_sent[:10]}T{ts_sent[11:19]}.{ts_sent[20:].zfill(6)}"
        #fields.append(ts_sent)
        #if parse_ts:
            # convert timestamps to pandas datetime objects
            #fields[0] = datetime.fromisoformat(fields[0])
            #fields[1] = datetime.fromisoformat(fields[1])
        fields = [ts_recv, ts_sent]
        # add each sensor reading as one item to the fields list
        for b in sensor_blocks:
            fields += list(b)
        # return all fields as a list
        return fields
    
    def __err_malformed_file(self):
        print("[ERROR] Cannot parse line "+str(self._curr_pos["line_num"])+" in MIROSLAV file: "+self.fname+"\n\n -> "+self._curr_pos["line"]+"\n")
        raise KeyError("Malformed MIROSLAV file!")

def open(fname: str | list, *args, **kwargs) -> MiroRawFile | MiroRawFile:
    if type(fname) is str:
        return MiroRawFile(fname, *args, **kwargs)
    elif type(fname) is list:
        return MiroRawFileList(fname, *args, **kwargs)
    else:
        return ValueError("Unrecognized input file parameter")

def open_experiment(exp_name: str, dev_name: str, output_delimiter: str=";", compression: Literal[None, "gz", "gzip"]=None, path: str | Path="."):
    p = Path(path)
    log_type = "pir"
    log_prefix = "-".join([exp_name, log_type, dev_name])+"."
    logfiles = [x for x in p.iterdir() if (not x.is_dir()) and x.name.startswith(log_prefix) and len(x.suffixes) == 2 and len(x.suffixes[0]) == 27]
    return MiroRawFileList(logfiles, compression=compression, output_delimiter=output_delimiter)

#def parse_and_merge(logfiles: list[str], infile_compression=None):
    #exp_name = set()

    # for lf in logfiles:
