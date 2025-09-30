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
    1. Manual trigger to start
    2. Processing data with Crazy Dave's special logic
    3. Output results
    """
    
    # Initialize n8n client
    n8n = N8nClient()
    
    # Define a simple workflow structure that matches n8n's format
    workflow_data = {
        "name": "Crazy Dave's Workflow",
        "nodes": [
            {
                "parameters": {},
                "type": "n8n-nodes-base.manualTrigger",
                "typeVersion": 1,
                "position": [240, 300],
                "id": "crazy-dave-trigger-001",
                "name": "When clicking 'Execute workflow'"
            },
            {
                "parameters": {
                    "jsCode": "// ====================================\n// 🎨 CRAZY DAVE'S SPECIAL PROCESSING 🎨\n// ====================================\n\n// Generate some crazy data\nconst crazyIdeas = [\n  'Build a rocket ship',\n  'Teach AI to dance',\n  'Create a time machine',\n  'Invent flying pizza',\n  'Make robots laugh'\n];\n\nconst crazyColors = ['purple', 'neon green', 'electric blue', 'hot pink', 'golden'];\n\nfunction getCrazyness() {\n  return Math.floor(Math.random() * 100) + 1;\n}\n\n// Crazy Dave's output\nconst output = {\n  processedBy: 'Crazy Dave',\n  timestamp: new Date().toISOString(),\n  crazynessLevel: getCrazyness(),\n  idea: crazyIdeas[Math.floor(Math.random() * crazyIdeas.length)],\n  color: crazyColors[Math.floor(Math.random() * crazyColors.length)],\n  message: 'Crazy Dave says: Let\\'s make something AWESOME! 🚀',\n  enthusiasm: '🎉'.repeat(Math.floor(Math.random() * 5) + 1)\n};\n\nreturn [{ json: output }];"
                },
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [460, 300],
                "id": "crazy-dave-processor-001",
                "name": "Crazy Dave's Processor"
            },
            {
                "parameters": {
                    "modelId": {
                        "__rl": True,
                        "value": "gpt-4o",
                        "mode": "list"
                    },
                    "messages": {
                        "values": [
                            {
                                "content": "=Analyze this crazy data and give me insights:\n\n{{ JSON.stringify($json, null, 2) }}\n\nProvide a fun commentary on Crazy Dave's output!"
                            }
                        ]
                    },
                    "options": {}
                },
                "type": "@n8n/n8n-nodes-langchain.openAi",
                "typeVersion": 1.8,
                "position": [680, 300],
                "id": "crazy-dave-ai-001",
                "name": "Analyze with AI"
            }
        ],
        "connections": {
            "When clicking 'Execute workflow'": {
                "main": [
                    [
                        {
                            "node": "Crazy Dave's Processor",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Crazy Dave's Processor": {
                "main": [
                    [
                        {
                            "node": "Analyze with AI",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "settings": {}
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
        print("   1. ▶️  When clicking 'Execute workflow' - Manual trigger")
        print("   2. ⚙️  Crazy Dave's Processor - Generates random crazy data")
        print("   3. 🤖 Analyze with AI - OpenAI analyzes the output")
        
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
