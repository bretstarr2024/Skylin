"""
n8n API Client
Handles all interactions with the n8n API for workflow management.
"""

import os
import requests
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()


class N8nClient:
    """Client for interacting with n8n API."""
    
    def __init__(self):
        self.api_url = os.getenv("N8N_API_URL")
        self.api_token = os.getenv("N8N_API_TOKEN")
        
        if not self.api_url or not self.api_token:
            raise ValueError("N8N_API_URL and N8N_API_TOKEN must be set in .env file")
        
        self.headers = {
            "X-N8N-API-KEY": self.api_token,
            "Content-Type": "application/json"
        }
    
    def get_workflows(self) -> List[Dict]:
        """Get all workflows from n8n."""
        response = requests.get(
            f"{self.api_url}/workflows",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json().get("data", [])
    
    def get_workflow(self, workflow_id: str) -> Dict:
        """Get a specific workflow by ID."""
        response = requests.get(
            f"{self.api_url}/workflows/{workflow_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def create_workflow(self, workflow_data: Dict) -> Dict:
        """Create a new workflow in n8n."""
        response = requests.post(
            f"{self.api_url}/workflows",
            headers=self.headers,
            json=workflow_data
        )
        response.raise_for_status()
        return response.json()
    
    def update_workflow(self, workflow_id: str, workflow_data: Dict) -> Dict:
        """Update an existing workflow."""
        response = requests.patch(
            f"{self.api_url}/workflows/{workflow_id}",
            headers=self.headers,
            json=workflow_data
        )
        response.raise_for_status()
        return response.json()
    
    def delete_workflow(self, workflow_id: str) -> None:
        """Delete a workflow."""
        response = requests.delete(
            f"{self.api_url}/workflows/{workflow_id}",
            headers=self.headers
        )
        response.raise_for_status()
    
    def activate_workflow(self, workflow_id: str) -> Dict:
        """Activate a workflow."""
        return self.update_workflow(workflow_id, {"active": True})
    
    def deactivate_workflow(self, workflow_id: str) -> Dict:
        """Deactivate a workflow."""
        return self.update_workflow(workflow_id, {"active": False})
    
    def execute_workflow(self, workflow_id: str, data: Optional[Dict] = None) -> Dict:
        """Execute a workflow."""
        response = requests.post(
            f"{self.api_url}/workflows/{workflow_id}/execute",
            headers=self.headers,
            json=data or {}
        )
        response.raise_for_status()
        return response.json()
