"""
Airtable API Client
Handles all interactions with the Airtable API.
"""

import os
from typing import Dict, List, Optional
from pyairtable import Api
from dotenv import load_dotenv

load_dotenv()


class AirtableClient:
    """Client for interacting with Airtable API."""
    
    def __init__(self):
        self.api_token = os.getenv("AIRTABLE_API_TOKEN")
        self.base_id = os.getenv("AIRTABLE_BASE_ID")
        
        if not self.api_token:
            raise ValueError("AIRTABLE_API_TOKEN must be set in .env file")
        
        self.api = Api(self.api_token)
        self.base = None
        
        if self.base_id:
            self.base = self.api.base(self.base_id)
    
    def set_base(self, base_id: str):
        """Set the active Airtable base."""
        self.base_id = base_id
        self.base = self.api.base(base_id)
    
    def get_records(self, table_name: str, **kwargs) -> List[Dict]:
        """Get all records from a table."""
        if not self.base:
            raise ValueError("Base ID not set. Call set_base() first or set AIRTABLE_BASE_ID in .env")
        
        table = self.base.table(table_name)
        return table.all(**kwargs)
    
    def get_record(self, table_name: str, record_id: str) -> Dict:
        """Get a specific record by ID."""
        if not self.base:
            raise ValueError("Base ID not set. Call set_base() first or set AIRTABLE_BASE_ID in .env")
        
        table = self.base.table(table_name)
        return table.get(record_id)
    
    def create_record(self, table_name: str, fields: Dict) -> Dict:
        """Create a new record in a table."""
        if not self.base:
            raise ValueError("Base ID not set. Call set_base() first or set AIRTABLE_BASE_ID in .env")
        
        table = self.base.table(table_name)
        return table.create(fields)
    
    def update_record(self, table_name: str, record_id: str, fields: Dict) -> Dict:
        """Update an existing record."""
        if not self.base:
            raise ValueError("Base ID not set. Call set_base() first or set AIRTABLE_BASE_ID in .env")
        
        table = self.base.table(table_name)
        return table.update(record_id, fields)
    
    def delete_record(self, table_name: str, record_id: str) -> Dict:
        """Delete a record."""
        if not self.base:
            raise ValueError("Base ID not set. Call set_base() first or set AIRTABLE_BASE_ID in .env")
        
        table = self.base.table(table_name)
        return table.delete(record_id)
    
    def batch_create(self, table_name: str, records: List[Dict]) -> List[Dict]:
        """Create multiple records at once."""
        if not self.base:
            raise ValueError("Base ID not set. Call set_base() first or set AIRTABLE_BASE_ID in .env")
        
        table = self.base.table(table_name)
        return table.batch_create(records)
    
    def batch_update(self, table_name: str, records: List[Dict]) -> List[Dict]:
        """Update multiple records at once."""
        if not self.base:
            raise ValueError("Base ID not set. Call set_base() first or set AIRTABLE_BASE_ID in .env")
        
        table = self.base.table(table_name)
        return table.batch_update(records)
