"""
Main application entry point for n8n Workflow Manager
"""

from n8n_client import N8nClient
from airtable_client import AirtableClient


def main():
    """Main application function."""
    print("🚀 n8n Workflow Manager with Airtable Integration")
    print("=" * 50)
    
    try:
        # Initialize clients
        print("\n📡 Connecting to n8n API...")
        n8n = N8nClient()
        print("✅ n8n API connected successfully!")
        
        print("\n📊 Connecting to Airtable API...")
        airtable = AirtableClient()
        print("✅ Airtable API connected successfully!")
        
        # Get existing workflows
        print("\n📋 Fetching existing workflows...")
        workflows = n8n.get_workflows()
        print(f"✅ Found {len(workflows)} workflow(s)")
        
        if workflows:
            print("\nExisting workflows:")
            for wf in workflows:
                status = "🟢 Active" if wf.get("active") else "⚪ Inactive"
                print(f"  - {wf.get('name')} (ID: {wf.get('id')}) {status}")
        
        print("\n" + "=" * 50)
        print("✨ Setup complete! Ready to manage workflows.")
        print("\nNext steps:")
        print("1. Run workflows/crazy_daves_workflow.py to create the demo workflow")
        print("2. Check the README.md for more usage examples")
        
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Make sure to add your API tokens to the .env file:")
        print("   - N8N_API_URL")
        print("   - N8N_API_TOKEN")
        print("   - AIRTABLE_API_TOKEN")
        print("   - AIRTABLE_BASE_ID (optional)")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
