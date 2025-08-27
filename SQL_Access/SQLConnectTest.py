def TestHistConnect(SQL_Command):
    import pymssql

    host = host_ip
    database = 'database'
    user = 'dbuser'  # Local SQL server authentication
    password = 'password'  # Local SQL server authentication

    port = '1434'

    try:
        conn = pymssql.connect(
            host=host,
            # port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor(as_dict=True)
        cursor.execute(SQL_Command)
        data = cursor.fetchall()
        cursor.close()

    except pymssql.Error as e:
        print(f"Error: {e}")

    try:
        if data != "":
            return data

    except:
        return ""


# SQL_Test = "SELECT [TechFirstName], [TechLastName], [TrainingTitle], [TrainingDate] FROM dbo.BasicInfo"
SQL_Test = "SELECT * FROM dbo.BCPForms"

print(TestHistConnect(SQL_Test))

