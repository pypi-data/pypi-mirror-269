'''
Description: Neo4j
Version: 0.0.1
Author: aka.zhp
Date: 2024-01-04 11:17:59
LastEditTime: 2024-01-04 11:24:40
'''
from py2neo import Graph
from typing import List, Optional, Tuple, Dict

class Neo4jHelper:
    def __init__(self,
                    host,
                    user,
                    password
                    ):
        self.graph = Graph(host, auth=(user, password))#name属性？

    def query(
        self,
        cypher_query: str
    ) -> List[Dict[str, str]]:
        g = self.graph.run(cypher_query).data()
        return g

