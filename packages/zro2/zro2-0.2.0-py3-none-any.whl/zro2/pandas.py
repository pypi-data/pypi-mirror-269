from collections import Counter
import io
import os
from typing import overload
import pandas as pd

from zro2.typing import bind_overload

@overload
def read_markdown_table(string : str) -> pd.DataFrame | None:
    ...

@overload
def read_markdown_table(file : str | io.IOBase, start : str |None = None, end : str | None = None) -> pd.DataFrame | None:
    ...

def read_markdown_table(*args, **kwargs): # type: ignore
    data = bind_overload(read_markdown_table, *args, **kwargs)
    if not data:
        # wrong arguments
        raise ValueError("Invalid arguments")

    if "string" in data:
        string = data.pop("string")
        if os.path.exists(string):
            file = string
            string = None
    else:
        file = data.pop("file")
        string = None

    if not string:
        if isinstance(file, str):
            started = False
            lastline = None
            start = data.get("start", None)
            end = data.get("end", None)

            with open(file) as f:
                string = ""
                for line in f.readlines():

                    if started:
                        pass
                    elif start is not None and line.startswith(start):
                        started = True

                    # if start is None and only contains - or |
                    
                    elif start is None:
                        counterkeys = list(Counter(line.replace(" ","").strip()).keys())
                        if len(counterkeys) == 2 and "-" in counterkeys and "|" in counterkeys:
                            started = True
                            assert lastline
                            string += lastline

                    if end is not None and line.startswith(end) and started:
                        break
                    
                    if end is None and not line.startswith("|") and started:
                        break

                    if started:
                        string += line 

                    lastline = line

    assert isinstance(string, str)

    # Convert Markdown table to CSV format by removing "|", "-", and trimming extra spaces
    csv_string = '\n'.join([' '.join(line.split('|')[1:-1]).strip() for line in string.strip().split('\n')])
    csv_list = csv_string.split('\n')
    csv_string = "\n".join(csv_list[:1]) + "\n" + "\n".join(csv_list[2:])

    # Use StringIO to simulate a file-like object for reading into pandas DataFrame
    df = pd.read_csv(io.StringIO(csv_string), sep='\\s{2,}', engine='python')

    return df