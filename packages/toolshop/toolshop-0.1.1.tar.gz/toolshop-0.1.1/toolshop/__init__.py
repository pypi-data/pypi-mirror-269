def all_tools():
    from .terminal import Shell, PythonExec, Browse
    from .data import Sql, Histogram
    from .file import make_file_tools
    
    return {
        Shell(),
        PythonExec(),
        Browse(),
        Sql(),
        Histogram(),
        *make_file_tools(),
    }