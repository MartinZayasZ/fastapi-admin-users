from .security import encode_password 
# The simplest solution I found is to set up an event for each table that executes a method after the table is created.

# Database initial data
INITIAL_DATA = {
      'roles': [
            {
                  "name": "Super Admin"
            },
            {
                  "name": "Administrador"
            },
            {
                  "name": "Editor"
            }
      ],
      'users': [
            {
                "firstname": "Admin",
                "lastname": "",
                "email": "admin@admin.com",
                "password": encode_password("password"),
                "role_id": 1
            }
      ]
}

# This method receives a table, a connection and inserts data to that table.
def initialize_table(target, connection, **kw):
    tablename = str(target)
    if tablename in INITIAL_DATA and len(INITIAL_DATA[tablename]) > 0:
        connection.execute(target.insert(), INITIAL_DATA[tablename])