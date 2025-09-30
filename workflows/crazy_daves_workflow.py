"""
Crazy Dave's Workflow
A demo workflow that integrates n8n with Airtable.
"""

import sys
import os

# Add parent directory to path to import clients
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from n8n_client import N8nClient
from airtable_client import AirtableClient


def create_crazy_daves_workflow():
    """
    Create Crazy Dave's workflow in n8n.
    
    This workflow demonstrates:
    1. Webhook trigger to receive data
    2. Processing the data
    3. Storing results in Airtable
    """
    
    # Initialize n8n client
    n8n = N8nClient()
    
    # Define the workflow structure
    workflow_data = {
        "name": "Crazy Dave's Workflow",
        "active": False,
        "nodes": [
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "crazy-dave-webhook",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [250, 300],
                "webhookId": ""
            },
            {
                "parameters": {
                    "functionCode": "// Process the incoming data\nconst incomingData = items[0].json;\n\n// Crazy Dave's special processing\nconst processedData = {\n  ...incomingData,\n  processedBy: 'Crazy Dave',\n  processedAt: new Date().toISOString(),\n  crazyFactor: Math.random() * 100,\n  message: `Crazy Dave says: This is ${incomingData.title || 'awesome'}!`\n};\n\nreturn [{\n  json: processedData\n}];"
                },
                "name": "Process Data",
                "type": "n8n-nodes-base.function",
                "typeVersion": 1,
                "position": [450, 300]
            },
            {
                "parameters": {
                    "operation": "append",
                    "application": "{{ $env.AIRTABLE_BASE_ID }}",
                    "table": "Workflows",
                    "options": {}
                },
                "name": "Save to Airtable",
                "type": "n8n-nodes-base.airtable",
                "typeVersion": 1,
                "position": [650, 300],
                "credentials": {
                    "airtableApi": {
                        "id": "1",
                        "name": "Airtable API"
                    }
                }
            },
            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{ $json }}",
                    "options": {}
                },
                "name": "Respond to Webhook",
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1,
                "position": [850, 300]
            }
        ],
        "connections": {
            "Webhook": {
                "main": [
                    [
                        {
                            "node": "Process Data",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Process Data": {
                "main": [
                    [
                        {
                            "node": "Save to Airtable",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Save to Airtable": {
                "main": [
                    [
                        {
                            "node": "Respond to Webhook",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "settings": {
            "saveDataErrorExecution": "all",
            "saveDataSuccessExecution": "all",
            "saveManualExecutions": True,
            "callerPolicy": "workflowsFromSameOwner"
        }
    }
    
    try:
        print("🎨 Creating Crazy Dave's Workflow...")
        print("=" * 50)
        
        # Create the workflow
        result = n8n.create_workflow(workflow_data)
        
        print(f"✅ Workflow created successfully!")
        print(f"\n📋 Workflow Details:")
        print(f"   Name: {result.get('name')}")
        print(f"   ID: {result.get('id')}")
        print(f"   Active: {result.get('active')}")
        print(f"   Nodes: {len(result.get('nodes', []))}")
        
        print("\n🎯 Workflow Components:")
        print("   1. 🪝 Webhook - Receives incoming data")
        print("   2. ⚙️  Process Data - Crazy Dave's special processing")
        print("   3. 💾 Save to Airtable - Stores results")
        print("   4. 📤 Respond to Webhook - Sends response back")
        
        print("\n" + "=" * 50)
        print("🎉 Crazy Dave's Workflow is ready!")
        print("\n💡 Next steps:")
        print("   1. Activate the workflow in n8n UI or use:")
        print(f"      n8n.activate_workflow('{result.get('id')}')")
        print("   2. Configure your Airtable credentials in n8n")
        print("   3. Test the webhook endpoint")
        
        return result
        
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function to run the workflow creation."""
    print("\n🚀 Crazy Dave's Workflow Creator")
    print("=" * 50)
    
    try:
        workflow = create_crazy_daves_workflow()
        
        if workflow:
            print("\n✨ All done! Check your n8n instance to see the workflow.")
        else:
            print("\n❌ Failed to create workflow. Check the error messages above.")
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n💡 Make sure to:")
        print("   1. Copy .env.example to .env")
        print("   2. Add your N8N_API_URL and N8N_API_TOKEN to .env")
        print("   3. Run: pip install -r requirements.txt")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
