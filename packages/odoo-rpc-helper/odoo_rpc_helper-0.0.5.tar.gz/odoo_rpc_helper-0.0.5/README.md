# Odoo XMLRPC Helper Functions

A small set of wrapper functions for facilitating CRUD operations in Odoo via
XMLRPC.

## Getting Started

### Installing via pip

    pip install odoo_rpc_helper

### A Simple Connection

```python
from odoo_rpc_helpers import OdooRPCHelper

DB = "test"  # Set this to your database name
USERNAME = "admin"  # Set this to a real username on the DB
PASSWORD = "admin"  # Set this to the password for user above
URL = "http://localhost:8069"  # Set this to the server URL

odoo = OdooRPCHelper(DB, USERNAME, PASSWORD, URL)

partner_id = odoo.create("res.partner", {"name": "Test Partner"})[0]
odoo.write("res.partner", [partner_id], {"phone": "+1 (123) 456-7890"})
partner = odoo.search_read(
  "res.partner",
  [['id', '=', partner_id]],
  ['name', 'phone']
)[0]
print(f"We have a partner with ID {partner['id']} named {partner['name']} "
      f" with phone {partner['phone']}")
odoo.unlink("res.partner", [partner_id])
```

## OdooRPCHelper Class

A class to help with various CRUD operations on an Odoo database via XMLRPC.

### Methods

#### __init__
`__init__(self, database: str, username: str, password: str, url: str = 'http://localhost:8069')`
Initialize the helper and authenticate with the Odoo server.
- **Parameters**:
  - `database`: The name of the Odoo database to access
  - `username`: The username of the user to execute XMLRPC requests as
  - `password`: The password of the user to execute XMLRPC requests as
  - `url`: The URL of the Odoo server

#### execute_kw
`execute_kw(self)`
Wrapper around `self.models.execute_kw`, to save effort on rewriting arguments. Simply omit the database, uid, and password arguments as they will be populated from instance variables.

#### create
`create(self, model: str, fields: Dict)`
Wrapper for `execute_kw create`. Create a single record.
- **Parameters**:
  - `model`: The model of which to create a record.
  - `fields`: The fields to assign during creation.
- **Return**: The ID of the created record.

#### create_multi
`create_multi(self, model: str, fields_list: List[Dict])`
Wrapper for `execute_kw create`. Create one or more records. Exactly like calling `model.create` with a list of dicts in Odoo.
- **Parameters**:
  - `model`: The model of which to create a record.
  - `fields_list`: The list of dictionaries of fields to assign.
- **Return**: The ID(s) of the created record(s).

#### search
`search(self, model: str, domain: List)`
Wrapper for `execute_kw search` on a model.
- **Parameters**:
  - `model`: The Odoo model to search.
  - `domain`: The regular Odoo-style domain. This function wraps it for the XMLRPC call.
- **Return**: The list of record IDs found in the search.

#### search_read
`search_read(self, model: str, domain: List, fields: List[str] = None)`
Wrapper for `execute_kw search_read` on a model.
- **Parameters**:
  - `model`: The Odoo model to search.
  - `domain`: The regular Odoo-style domain.
  - `fields`: The fields to be loaded. All fields loaded by default.
- **Return**: A list of dictionaries containing the loaded record fields.

#### read
`read(self, model: str, res_ids: List[int], fields: List[str])`
Wrapper for calling read on a model.
- **Parameters**:
  - `model`: The Odoo model to browse.
  - `res_ids`: The IDs of the records to browse.
  - `fields`: The fields to be read.
- **Return**: List of dictionaries with the requested fields.

#### write
`write(self, model: str, res_ids: List[int], fields: Dict)`
Wrapper for calling write on a model.
- **Parameters**:
  - `model`: Model to write to.
  - `res_ids`: Record IDs to write to.
  - `fields`: Fields to write.

#### unlink
`unlink(self, model: str, res_ids: List[int])`
Wrapper for calling unlink on a model.
- **Parameters**:
  - `model`: Model to call unlink on.
  - `res_ids`: Record IDs to unlink.
