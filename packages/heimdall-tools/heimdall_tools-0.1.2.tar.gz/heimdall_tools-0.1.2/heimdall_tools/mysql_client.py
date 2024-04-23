import mysql.connector
from typing import List, Tuple

"""""
@dataclass
class mysql:
    username: String
    password: String
    host: String
    database_name: String
    raise_on_warnings: Bool
"""""
class MYSQL_DB_CLIENT:
    def __init__(self, username, password, hostname, database_name, raise_on_warnings = True) -> None:
        self.username = username
        self.password =password
        self.hostname = hostname
        self.database_name = database_name
        self.raise_on_warnings = raise_on_warnings
        self.cursor = None 

    def db_connect(self) -> None:
        self.connection = mysql.connector.connect(
                        user = self.username,
                        password = self.password,
                        host = self.hostname,
                        database = self.database_name,
                        raise_on_warnings = self.raise_on_warnings
                    )
        self.cursor = self.connection.cursor()

    def db_execute_query(self, query) -> None:
        self.cursor.execute(query)
        print(f"In DB CLass execute query {query}")
        #self.connection.commit()

    def db_read_result(self) -> List[Tuple]:
        result = self.cursor.fetchall()
        print(f'Read Result {result}')
        return result

    def db_read_sensor_id_from_heimdall_memory(self, customer_name, site_name, building_name, floor_position, type_id, sensor_name) -> int:
        query =  """
        SELECT sensors.sensor_id
        FROM sensors
        JOIN floors ON sensors.floor_id = floors.floor_id
        JOIN buildings ON floors.building_id = buildings.building_id
        JOIN sites ON buildings.site_id = sites.site_id
        JOIN customers ON sites.customer_id = customers.customer_id
        JOIN sensor_type ON sensors.type_id = sensor_type.type_id
        WHERE customers.customer_name = %s
        AND sites.site_name = %s
        AND buildings.building_name = %s
        AND floors.floor_position = %s
        AND sensor_type.type_id = %s
        AND sensors.sensor_name = %s
        """
        # Execute the query
        self.cursor.execute(query, (customer_name, site_name, building_name, floor_position, type_id, sensor_name))
        result = self.cursor.fetchone()
        if result:
            print(f"MYSQL LOGS: Result --> {result}")
            #sensor_id = result['sensor_id']
        
        return result
