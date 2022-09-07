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

    def create_author(self, name, surname):
        resultString = ""
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_author, name, surname)
            for row in result:
                print(row)
                print("Araştırmacı eklendi: {}, {}".format(row['a'], row['b']))
                resultString = "Araştırmacı eklendi: {}, {}".format(row['a'], row['b'])
        return resultString 

    @staticmethod
    def _create_and_return_author(tx, name, surname):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (a:Author { name: $name, surname: $surname}) RETURN a"
        )
        result = tx.run(query, name=name, surname=surname)
        try:
            return [{"a": row["a"]["name"], "b": row["a"]["surname"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise


    def create_type(self, type, place):
        resultString = ""
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_type, type, place)
            for row in result:
                print(row)
                print("Tür eklendi: {}, {}".format(row['a'], row['b']))
                resultString = "Tür eklendi: {}, {}".format(row['a'], row['b'])
        return resultString 

    @staticmethod
    def _create_and_return_type(tx, type, place):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "CREATE (t:Types { type: $type, place: $place}) RETURN t"
        )
        result = tx.run(query, type=type, place=place)
        try:
            return [{"a": row["t"]["type"], "b": row["t"]["place"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_coauthor_relationship(self, authorName, authorSurname, coauthorName, coauthorSurname):
        resultString = ""
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_coauthor_relationship, authorName, authorSurname, coauthorName, coauthorSurname)
            for row in result:
                print(row)
                print("İlişki oluşturuldu: {}, {}".format(row['a'], row['b']))
                resultString = "İlişki oluşturuldu: {}, {}".format(row['a'], row['b'])
        return resultString 

    @staticmethod
    def _create_and_return_coauthor_relationship(tx, authorName, authorSurname, coauthorName, coauthorSurname):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "MATCH "
            "(a:Author), "
            "(b:Author) "
            "WHERE a.name = $authorName AND a.surname = $authorSurname and b.name = $coauthorName and b.surname = $coauthorSurname "
            "CREATE (a)-[r:ortak_calısır{ authorID:id(b) }]->(b), (b)-[r2:ortak_calısır{ authorID:id(a) }]->(a) "
            "RETURN type(r),type(r2)"
        )
        result = tx.run(query, authorName=authorName, authorSurname=authorSurname, coauthorName=coauthorName, coauthorSurname=coauthorSurname)
        try:
            return [{"a": row["type(r)"], "b": row["type(r2)"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_type_relationship(self,name,place,type):
        resultString = ""
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_type_relationship, name,place,type)
            for row in result:
                print(row)
                print("İlişki oluşturuldu: {}".format(row['a']))
                resultString = "İlişki oluşturuldu: {}".format(row['a'])
        return resultString 

    @staticmethod
    def _create_and_return_type_relationship(tx,name,place,type):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "MATCH "
            "(a:Publications), "
            "(b:Types) "
            "WHERE a.name = $name AND b.type = $type and b.place = $place  "
            "CREATE (a)-[r:yayınlanır{ typeID:id(b) }]->(b)  "
            "RETURN type(r)"
        )
        result = tx.run(query, name=name, type=type, place=place)
        try:
            return [{"a": row["type(r)"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def find_publication(self, name):
        resultString = ""
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_publication, name)
            print(result)
            rows=[]
            for row in result:
                print("{}".format(row["count"]))
            resultString = "{}".format(row["count"])
        return resultString 
    @staticmethod
    def _find_and_return_publication(tx, name):
        query = (
            "Match (b:Publications)"
            "where b.name= $name  "
            "return count(b.name)"
        )
        print(query)
        result = tx.run(query, name=name)
        return [{"count": row["count(b.name)"]}
                    for row in result]

    def find_type(self, type,place):
        resultString = ""
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_type, type,place)
            print(result)
            rows=[]
            for row in result:
                print("{}".format(row["count"]))
            resultString = "{}".format(row["count"])
        return resultString 
    @staticmethod
    def _find_and_return_type(tx, type,place):
        query = (
            "Match (b:Types)"
            "where b.type= $type and b.place = $place  "
            "return count(b.type)"
        )
        print(query)
        result = tx.run(query, type=type, place=place)
        return [{"count": row["count(b.type)"]}
                    for row in result]


    def create_publication_new(self, authorName,authorSurname,journalName,journalDate,journalPlace,journalType):
        resultString = ""
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_publication_new, authorName,authorSurname,journalName,journalDate,journalPlace,journalType)
            for row in result:
                print(row)
                print("Yayın eklendi: {}".format(row['a']))
                resultString = "Yayın eklendi: {}".format(row['a'])
        return resultString 

    @staticmethod
    def _create_and_return_publication_new(tx, authorName,authorSurname,journalName,journalDate,journalPlace,journalType):
        query = (
            "MATCH "
            "(a:Author),  (b:Types) "
            "where a.name = $authorName and a.surname = $authorSurname and b.type = $journalType and b.place = $journalPlace "
            "Create(p:Publications{ name: $journalName ,year: $journalDate } ) "
            "Create(a)-[r:yayın_yazarı{ typeID:id(p) }]->(p) "
            "CREATE(p)-[r2:yayınlanır{ typeID:id(b) }]->(b) "
            "Return p"
        )
        result = tx.run(query, authorName=authorName,authorSurname=authorSurname,journalName=journalName,journalDate=journalDate,journalPlace=journalPlace,journalType=journalType)
        try:
            return [{"a": row["p"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def create_publication(self, authorName,authorSurname,journalName,journalDate,journalPlace,journalType):
        resultString = ""
        with self.driver.session() as session:
            # Write transactions allow the driver to handle retries and transient errors
            result = session.write_transaction(
                self._create_and_return_publication, authorName,authorSurname,journalName,journalDate,journalPlace,journalType)
            for row in result:
                print(row)
                print("Yayın eklendi: {}".format(row['a']))
                resultString = "Yayın eklendi: {}".format(row['a'])
        return resultString 

    @staticmethod
    def _create_and_return_publication(tx, authorName,authorSurname,journalName,journalDate,journalPlace,journalType):
        print("dene")
        query = (
            "MATCH "
            "(a:Author),  (b:Types), (c:Publications) "
            "where c.name = $journalName and a.name = $authorName and a.surname = $authorSurname and b.type = $journalType and b.place = $journalPlace "
            "CREATE (a)-[r:yayın_yazarı{ publicationID:id(c) }]->(c) "
            "CREATE(c)-[r2:yayınlanır{ typeID:id(b) }]->(b) "
            "Return c"
        )
        result = tx.run(query, authorName=authorName,authorSurname=authorSurname,journalName=journalName,journalDate=journalDate,journalPlace=journalPlace,journalType=journalType)
        try:
            return [{"a": row["c"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise




  



