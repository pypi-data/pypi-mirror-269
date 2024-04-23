"""
A small helper to execute XMLRPC requests against a given Odoo server and
database.
"""
import xmlrpc.client
from typing import List, Dict


class OdooRPCHelper:
    """
    A class to help with various CRUD operations on an Odoo database via
    XMLRPC.
    """

    def __init__(self, database: str, username: str, password: str, url: str =
                 'http://localhost:8069'):
        """
        Initialize the helper and authenticate with the Odoo server

        :param db: The name of the Odoo database to access
        :param username: The username of the user to execute XMLRPC requests as
        :param password: The password of the user to execute XMLRPC requests as
        :param url: The URL of the Odoo server
        """
        self.database = database
        self.password = password
        self.common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        self.uid = self.common.authenticate(database, username, password, {})
        self.models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')

    def execute_kw(self, *args, **kwargs):
        """
        Wrapper around self.models.execute_kw, to save effort on rewriting
        arguments. Simply omit the database, uid and password arguments as they
        will be populated from instance variables.
        """
        return self.models.execute_kw(
            self.database,
            self.uid,
            self.password,
            *args,
            **kwargs,
        )

    def create(self, model: str, fields: Dict) -> int:
        """
        Wrapper for execute_kw create. Create a single record.

        :param model: The model of which to create a record.
        :param fields: The fields to assign during creation.

        :return: The ID of the created record

        """
        return self.execute_kw(
            model,
            'create',
            [[fields]],
        )

    def create_multi(self, model: str, fields_list: List[Dict]) -> List[int]:
        """
        Wrapper for execute_kw create. Create one or more records.
        Exactly like calling model.create with a list of dicts in Odoo.

        :param model: The model of which to create a record.
        :param fields_list: The list of dictionaries of fields to assign.

        :return: The ID(s) of the created record(s)

        """
        return self.execute_kw(
            model,
            'create',
            [fields_list],
        )

    def search(self, model: str, domain: List[List], **kwargs) -> List[int]:
        """
        Wrapper for execute_kw search on a model.

        :param model: The Odoo model to search.
        :param domain: The regular Odoo-style domain. This function wraps
                       it for the XMLRPC call.
        :return: The list of record IDs found in the search
        """
        return self.execute_kw(
            model,
            'search',
            [domain],
            kwargs
        )

    def search_read(
        self,
        model: str,
        domain: List[List],
        fields: List[str],
        **kwargs
    ) -> List[int]:
        """
        Wrapper for execute_kw search on a model.

        :param model: The Odoo model to search.
        :param domain: The regular Odoo-style domain. This function wraps
                       it for the XMLRPC call.
        :param fields: The fields to be loaded. All fields loaded by default.
        :return: A list of dictionaries containing the loaded record fields.
        """
        kwargs.update({'fields': fields})
        return self.execute_kw(
            model,
            'search_read',
            [domain],
            kwargs
        )

    def read(
        self,
        model: str,
        res_ids: List[int],
        fields: List[str],
    ) -> List[Dict]:
        """ Wrapper for calling read on a model.

            :param model: The Odoo model to browse
            :param res_ids: The IDs of the records to browse
            :param fields: The fields to be read
            :return: Dict

        """
        return self.execute_kw(
            model,
            'read',
            res_ids,
            {'fields': fields}
        )

    def write(
        self,
        model: str,
        res_ids: List[int],
        fields: Dict
    ) -> List[Dict]:
        """ Wrapper for calling write on a model.

            :param model: Model to write to.
            :param res_ids: Record IDs to write to.
            :param fields: Fields to write
        """
        return self.execute_kw(
            model,
            'write',
            [res_ids, fields,],
        )

    def unlink(
        self,
        model: str,
        res_ids: List[int],
    ):
        """
        Wrapper for calling unlink on a model.

        :param model: Model to call unlink on.
        :param res_ids: Record IDs to unlink.
        """
        return self.execute_kw(
            model,
            'unlink',
            res_ids,
        )
