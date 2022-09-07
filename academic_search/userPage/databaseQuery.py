from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

class App:

    def __init__(self):
        uri = "Your neo4j url"
        user = "Your Username"
        password = "Your password"
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def create_friendship(self, person1_name, person2_name):
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name)
            for row in result:
                print("Created friendship between: {p1}, {p2}".format(p1=row['p1'], p2=row['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_Author(self, field_name,query_veriable):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_author, field_name,query_veriable)
            print(result)
            rows=[]
            for row in result:
                print("Found person: {},{},{},{},{}".format(row["id"],row["name"],row["surname"],row["name2"],row["surname2"]))
                rows.append(row)
            return(rows)

    @staticmethod
    def _find_and_return_author(tx, field_name,query_veriable):
        query = (
            "Match(a:Author)-[r:ortak_calısır|yayın_yazarı]->(b:Author)"
            "where a.{} = $field_name  "
            "return id(a), a.name as name, a.surname as surname,b.name as name2, b.surname as surname2"
        ).format(query_veriable)
        result = tx.run(query, field_name=field_name)
        return [{"id": row["id(a)"],"name": row["name"], "surname": row["surname"],"name2": row["name2"], "surname2": row["surname2"]}
                    for row in result]

    def find_author_publications(self, field_name,query_veriable):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_author_publication, field_name,query_veriable)
            print(result)
            rows=[]
            for row in result:
                print("Found person: {},{},{},{},{},{},{}".format(row["id"],row["name"],row["surname"],row["publicationName"],row["year"],row["place"],row["type"]))
                rows.append(row)
            return(rows)

    @staticmethod
    def _find_and_return_author_publication(tx, field_name,query_veriable):
        query = (
            "Match(a:Author)-[r:yayın_yazarı]->(b:Publications),"
            "(b)-[r2:yayınlanır]->(c:Types)"
            "where a.{} = $field_name  "
            "return id(a), a.name as name, a.surname as surname,b.name as publicationName, b.year as year, c.place as place, c.type as type"
        ).format(query_veriable)
        result = tx.run(query, field_name=field_name)
        return [{"id" : row["id(a)"],"name": row["name"], "surname": row["surname"],"publicationName":row["publicationName"],"year": row["year"],"place":row["place"] ,"type": row["type"]}
                    for row in result]

    def find_publications(self, field_name, query_veriable):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_publication, field_name, query_veriable)
            print(result)
            rows=[]
            for row in result:
                print("Found person: {},{},{},{},{},{},{}".format(row["id"],row["name"],row["surname"],row["publicationName"],row["year"],row["place"],row["type"]))
                rows.append(row)
            return(rows)

    @staticmethod
    def _find_and_return_publication(tx, field_name,query_veriable):
        query = (
            "Match(a:Author)-[r:yayın_yazarı]->(b:Publications),"
            "(b)-[r2:yayınlanır]->(c:Types)"
            "where b.{} = $field_name  "
            "return id(a), a.name as name, a.surname as surname,b.name as publicationName, b.year as year, c.place as place, c.type as type"
        ).format(query_veriable)
        print(query)
        result = tx.run(query, field_name=field_name)
        return [{"id" : row["id(a)"],"name": row["name"], "surname": row["surname"],"publicationName":row["publicationName"],"year": row["year"],"place":row["place"] ,"type": row["type"]}
                    for row in result]

    def find_types(self, field_name, query_veriable):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_types, field_name, query_veriable)
            print(result)
            rows=[]
            for row in result:
                print("Found person: {},{},{},{},{},{},{}".format(row["id"],row["name"],row["surname"],row["publicationName"],row["year"],row["place"],row["type"]))
                rows.append(row)
            return(rows)

    @staticmethod
    def _find_and_return_types(tx, field_name,query_veriable):
        query = (
            "Match(a:Author)-[r:yayın_yazarı]->(b:Publications),"
            "(b)-[r2:yayınlanır]->(c:Types)"
            "where c.{} = $field_name  "
            "return id(a), a.name as name, a.surname as surname,b.name as publicationName, b.year as year, c.place as place, c.type as type"
        ).format(query_veriable)
        print(query)
        result = tx.run(query, field_name=field_name)
        return [{"id" : row["id(a)"],"name": row["name"], "surname": row["surname"],"publicationName":row["publicationName"],"year": row["year"],"place":row["place"] ,"type": row["type"]}
                    for row in result]




