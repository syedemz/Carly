from io import StringIO
from typing import Optional, NoReturn
import logging
import json
import psycopg2
from psycopg2 import sql
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CustomerImporter:
    def __init__(self, dbname: str, user: str, password: str, schema: str, tablename: str, host: Optional[str] = 'localhost', port: Optional[int] = 5400):
        """_summary_

        Args:
            dbname (str): _description_
            user (str): _description_
            password (str): _description_
            schema (str): _description_
            tablename (str): _description_
            host (Optional[str], optional): _description_. Defaults to 'localhost'.
            port (Optional[int], optional): _description_. Defaults to 5400.
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.schema = schema
        self.tablename = tablename

    def connect(self) -> NoReturn:
        """_summary_
        """
        try:
            # Connect to the PostgreSQL server
            self.conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.conn.autocommit = True
            self.cursor = self.conn.cursor()
            logger.info("connected successfully")

        except psycopg2.OperationalError as e:
            logger.error("Unable to connect to the database. Error: %s", e)
        except psycopg2.InternalError as e:
            logger.error("An internal error was encountered trying to connect to the database. Error: %s", e)


    def check_table_exists(self, table_name: str) -> bool:
        """_summary_

        Args:
            table_name (str): _description_

        Returns:
            _type_: _description_
        """
        try:
            # Check if the table exists
            self.cursor.execute(f"SELECT * FROM information_schema.tables WHERE table_schema = '{self.schema}' AND table_name = '{self.tablename}'")
   
            result = self.cursor.fetchone()

            if result:
                print(f"Table {table_name} exists.")
                return True
            
            return False
        except psycopg2.OperationalError as e:
            logger.error("Error checking table existence: %s", e)
            return False
    

    def close_connection(self) -> NoReturn:
        """_summary_
        """
        try:
            # Close the connection
            if self.conn is not None:
                self.conn.close()
                logger.info("Connection closed successfully")

        except psycopg2.OperationalError as e:
            logger.error("Error while closing the connection: %s", e)
    
   
    def create_table(self) -> NoReturn:
        """_summary_
        """               
        try:
            create_table_query = f"""
                CREATE TABLE IF NOT EXISTS {self.schema}.{self.tablename} (
                    email VARCHAR(255),
                    customer_id VARCHAR(255) PRIMARY KEY,
                    country VARCHAR(20),
                    language VARCHAR(20)
                );
            """
            # Execute the query
            self.cursor.execute(create_table_query)

            # Commit the changes
            self.conn.commit()

            logger.info("Table %s.%s created successfully", self.schema, self.tablename)

        except psycopg2.OperationalError as e:
            logger.info("Table %s.%s could not be created", self.schema, self.tablename)
            logger.error("Error while trying to create the table: %s", e)


    def importData(self, customerData: list) -> NoReturn:
        """_summary_

        Args:
            customerData (list): _description_
        """
        
        sql_template = f"COPY {self.schema}.{self.tablename}(email, customer_id, country, language) FROM STDIN WITH CSV HEADER"
        # Use a StringIO object to simulate a file-like object for COPY command
        string_io = StringIO()
        for obj in customerData:
            if set(['email', 'customer_id', 'country', 'language']).issubset(obj.keys()):
                string_io.write(f"{obj['email']},{obj['customer_id']},{obj['country']},{obj['language']}\n")
        string_io.seek(0)
        try:
            self.cursor.copy_expert(sql=sql.SQL(sql_template), file=string_io)
            self.conn.commit()
            logger.info("Bulk load completed successfully")
        except psycopg2.Error as e:
            # Rollback the transaction in case of error
            self.conn.rollback()
            logger.error("Error occured while bulk loading the data %s", e)
    

    def readCustomerFile(self) -> list:
        """_summary_
        """
        customer_info = []
        with open('../customer_export.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                # Parse the JSON object
                try:
                    json_object = json.loads(line)
                    # Process the JSON object as needed
                    customer_info.append(json_object)
                except json.JSONDecodeError as e:
                    logger.error("Error parsing JSON: %s", e)
            return customer_info


if __name__ == "__main__":
    username = 'emad'
    pswd = 'NumiTumi11'
    databaseName = 'carly_customer_base'
    tblname = 'customerinfo'
    Schema = 'customer_schema'


    importer = CustomerImporter(dbname=databaseName, user=username, tablename=tblname, schema=Schema, password=pswd)
    
    try:
        importer.connect()
        tableCheck = importer.check_table_exists(table_name=tblname)
        if (tableCheck is False):
            importer.create_table()
        
        customerinfo = importer.readCustomerFile()
        importer.importData(customerinfo)
        
    except psycopg2.OperationalError as err:
        logger.error("An error occured: %s", err)

    finally:
        importer.close_connection()