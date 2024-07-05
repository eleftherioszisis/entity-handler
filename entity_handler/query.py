from entity_management.nexus import sparql_query


LIMIT = 10000


def _query(query):
    return [result["id"]["value"] for result in sparql_query(query)["results"]["bindings"]]


def by_type(resource_type, limit=LIMIT):
    return _query(f'''
        PREFIX bmo: <https://bbp.epfl.ch/ontologies/core/bmo/>
        PREFIX nxv: <https://bluebrain.github.io/nexus/vocabulary/>

        SELECT ?id
        WHERE {{
            GRAPH ?g {{
            ?id a bmo:{resource_type} ;
                nxv:deprecated   false .
            }}
        }}
        LIMIT {LIMIT}
    ''')

