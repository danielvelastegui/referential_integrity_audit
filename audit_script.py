import pyodbc


def check_integrity_referential(cursor):
    """
    Revisa 3 puntos de la integridad referencial y devuelve la cantidad de resultados encontrados
    """
    results = {}
    # Punto 1: Identificación automática de las relaciones
    relationships = []
    query = "SELECT OBJECT_NAME(constraint_object_id) as ConstraintName, " \
            "OBJECT_NAME(parent_object_id) as TableName, " \
            "COL_NAME(parent_object_id, parent_column_id) as ColumnName, " \
            "OBJECT_NAME(referenced_object_id) as ReferenceTable, " \
            "COL_NAME(referenced_object_id, referenced_column_id) as ReferenceColumn " \
            "FROM sys.foreign_key_columns"
    cursor.execute(query)
    for row in cursor.fetchall():
        relationships.append((row[0], row[1], row[2], row[3], row[4]))

    # Escribimos la cantidad de relaciones
    results['relations'] = len(relationships)

    with open("relaciones.txt", "w") as file:
        file.write("Relaciones existentes:\n")
        for rel in relationships:
            file.write("Constraint: {}\nTabla: {}\nColumna: {}\nTabla referencia: {}\n"
                       "Columna referencia: {}\n\n".format(rel[0], rel[1], rel[2], rel[3], rel[4]))

    # Punto 2: Chequeo automático de anomalías en la integridad referencial
    anomalies = []
    query = "SELECT name, is_disabled" \
            " FROM sys.foreign_keys;"
    cursor.execute(query)
    for constraint in cursor.fetchall():
        if constraint[1] == 1:
            anomalies.append("{}".format(constraint[0]))

    # Escribimos la cantidad de anomalias de definicion encontradas
    results['definition_anomalies'] = len(anomalies)

    with open("anomalias_definicion.txt", "w") as file:
        file.write("Anomalias en la integridad referencial - Constraints deshabilitados:\n")
        for anomaly in anomalies:
            file.write("- {}\n".format(anomaly))

    # Punto 3: Chequeo automático de anomalías en los datos
    anomalies = []
    cursor.execute("DBCC CHECKCONSTRAINTS WITH ALL_CONSTRAINTS;")
    # Si la consulta esta vacia el fetchall devuelve error
    try:
        for result in cursor.fetchall():
            anomalies.append((result[0], result[1], result[2]))
    except:
        pass

    # Escribimos la cantidad de anomalias de datos encontradas
    results['data_anomalies'] = len(anomalies)

    with open("anomalias_datos.txt", "w") as file:
        file.write("Anomalias en los datos:\n\n")
        for anomaly in anomalies:
            file.write("Tabla: {}\nConstraint: {}\nAnomalia: {}\n\n".format(anomaly[0], anomaly[1], anomaly[2]))
    
    return results

if __name__ == '__main__':
    database_name = input("Ingrese el nombre de la base de datos: ")
    # Conectar a SQL Server
    server_name = "localhost"
    username = "audit"
    password = "audit"
    conn = pyodbc.connect("Driver=ODBC Driver 17 for SQL Server;Server=%s;Database=%s;UID=%s;PWD=%s"
    % (server_name, database_name, username, password))
    cursor = conn.cursor()
    # Revisar integridad referencial
    audit_results = check_integrity_referential(cursor)
    print("\nResultado de auditoría")
    print("\nRelaciones: {}".format(audit_results.get("relations", 0)))
    print("Anomalías de definición: {}".format(audit_results.get("definition_anomalies", 0)))
    print("Anomalías de data: {}\n".format(audit_results.get("data_anomalies", 0)))
    print("Para una información más detallada revisar los archivos generados.\n")
    # Cerrar conexion
    cursor.close()
    conn.close()

