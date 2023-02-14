# Check Referential Integrity

This script checks the referential integrity of a SQL Server database. It does the following three checks:

1. Identifies existing relationships: The script queries the `sys.foreign_key_columns` table and retrieves all the relationships in the database. The relationships are then written to a file called "relaciones.txt".

2. Checks for anomalies in referential integrity: The script queries the `sys.foreign_keys` table and retrieves all the foreign keys in the database. If a foreign key is disabled, the script writes the name of the constraint to a file called "anomalias_integridad.txt".

3. Checks for anomalies in data: The script runs the `DBCC CHECKCONSTRAINTS` command to check for anomalies in the data. Any anomalies found are written to a file called "anomalias_datos.txt".

## Usage

To use this script, you have to install the requirements running the following command:

```
pip install -r requirements.txt
```

Then, run the following command:

```
python audit_script.py
```

The script will prompt you to enter the name of the database that you want to check. Then, it will connect to the database using the specified credentials and perform the three checks described above.

Note: Make sure to update the server name, username, and password in the script to match your environment.
