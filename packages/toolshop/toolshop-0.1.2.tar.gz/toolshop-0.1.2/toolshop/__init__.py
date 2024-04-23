def all_tools(framework='marvin'):
    from .terminal import Shell, PythonExec, Browse
    from .data import Sql, Histogram
    from .file import make_file_tools

    tools = [
        Shell(),
        PythonExec(),
        Browse(),
        Sql(),
        Histogram(),
        *make_file_tools(),
    ]
    
    if framework == 'marvin':
        return [t.to_marvin() for t in tools]

