from typing import Tuple, List

import sqlalchemy as sa

from .base import Tool


class Sql(Tool):
    def call(self, sql_query: str, database_uri: str) -> str:
        """Runs the sql query and returns result set as a CSV string. Always try 
        this tool for running sql queries first before trying other methods.
        
        Args:
            database_uri (str): The database connection string which is passed 
                to sqlachemy.create_engine().
            sql_query (str): The sql query to run
        """
        engine = sa.create_engine(database_uri)

        # Execute the query and fetch results
        result = engine.execute(sql_query)
        column_names = result.keys()
        output = (','.join(column_names))

        # Iterate over rows and print them as CSV
        for row in result:
            output += '\n' + ','.join([str(value) for value in row])

        return output


class Histogram(Tool):
    def call(self, title: str, data: List[Tuple]) -> str:
        """
        Draws an ascii histogram of the data.  Accepts a list of tuples representing
        histogram bucket values. The first value of each tuple is the bucket name
        and the second value is the histogram value of the bucket.  When user asks
        for a histogram, always use this tool.

        Example: 
        
        ascii_histogram(
            title="Chart Tile", 
            data=[('p0', 0), ('p25', 100), ('p50', 200), ('p75', 300), ('p75', 400)]
        )
        
        Chart Tile
        ###############################################################################
                                                                                0  p0 
        █████████████████                                                      100  p25
        ██████████████████████████████████                                     200  p50
        ███████████████████████████████████████████████████                    300  p75
        █████████████████████████████████████████████████████████████████████  400  p75
        """
        
        # Check if ascii_graph is installed, since it is an optional dependency.
        try:
            from ascii_graph import Pyasciigraph
        except ImportError:
            raise ImportError(
                "ascii_graph is not installed. Please install it using 'pip install ascii_graph'."
            )

        graph = Pyasciigraph()
        
        output = ""
        for line in graph.graph(title, data):
            output += line
            output += "\n"
        
        return output

