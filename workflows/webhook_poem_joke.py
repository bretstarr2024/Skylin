"""
Webhook-based Poem & Joke Generator
Creates a workflow with webhook trigger for web front end integration.
"""

import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from n8n_client import N8nClient


def create_webhook_workflow():
    """Create workflow with webhook trigger for web front end."""
    
    n8n = N8nClient()
    
    workflow_data = {
        "name": "Webhook - Poem & Joke Generator",
        "nodes": [
            # Node 1: Webhook Trigger
            {
                "parameters": {
                    "httpMethod": "POST",
                    "path": "poem-joke-generator",
                    "responseMode": "responseNode",
                    "options": {}
                },
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 2,
                "position": [240, 400],
                "id": str(uuid.uuid4()),
                "name": "Webhook",
                "webhookId": ""
            },
            
            # Node 2: Extract Topic from Request
            {
                "parameters": {
                    "assignments": {
                        "assignments": [
                            {
                                "id": str(uuid.uuid4()),
                                "name": "topic",
                                "value": "={{ $json.body.topic || $json.topic || 'AI and creativity' }}",
                                "type": "string"
                            }
                        ]
                    },
                    "options": {}
                },
                "type": "n8n-nodes-base.set",
                "typeVersion": 3.4,
                "position": [460, 400],
                "id": str(uuid.uuid4()),
                "name": "Extract Topic"
            },
            
            # Node 3: Generate Poem
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
                                "content": "=Write a creative and inspiring poem about: {{ $json.topic }}\n\nThe poem should be:\n- 4-8 lines long\n- Professional and thoughtful\n- Include relevant hashtags at the end\n\nReturn only the poem text."
                            }
                        ]
                    },
                    "options": {}
                },
                "type": "@n8n/n8n-nodes-langchain.openAi",
                "typeVersion": 1.8,
                "position": [680, 300],
                "id": str(uuid.uuid4()),
                "name": "Generate Poem"
            },
            
            # Node 4: Generate Joke
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
                                "content": "=Write a clever, professional joke about: {{ $json.topic }}\n\nThe joke should be:\n- Workplace-appropriate\n- Smart and witty\n- Include relevant hashtags at the end\n\nReturn only the joke."
                            }
                        ]
                    },
                    "options": {}
                },
                "type": "@n8n/n8n-nodes-langchain.openAi",
                "typeVersion": 1.8,
                "position": [680, 500],
                "id": str(uuid.uuid4()),
                "name": "Generate Joke"
            },
            
            # Node 5: Combine Results
            {
                "parameters": {
                    "jsCode": "// Collect both outputs and format response\nconst topic = $('Extract Topic').first().json.topic;\nconst poem = $('Generate Poem').first().json.message?.content || $('Generate Poem').first().json.output || 'Error generating poem';\nconst joke = $('Generate Joke').first().json.message?.content || $('Generate Joke').first().json.output || 'Error generating joke';\n\nreturn [{\n  json: {\n    success: true,\n    topic: topic,\n    poem: poem,\n    joke: joke,\n    timestamp: new Date().toISOString()\n  }\n}];"
                },
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [900, 400],
                "id": str(uuid.uuid4()),
                "name": "Format Response"
            },
            
            # Node 6: Respond to Webhook
            {
                "parameters": {
                    "respondWith": "json",
                    "responseBody": "={{ $json }}",
                    "options": {}
                },
                "type": "n8n-nodes-base.respondToWebhook",
                "typeVersion": 1.1,
                "position": [1120, 400],
                "id": str(uuid.uuid4()),
                "name": "Respond"
            }
        ],
        "connections": {
            "Webhook": {
                "main": [
                    [
                        {
                            "node": "Extract Topic",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Extract Topic": {
                "main": [
                    [
                        {
                            "node": "Generate Poem",
                            "type": "main",
                            "index": 0
                        },
                        {
                            "node": "Generate Joke",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Generate Poem": {
                "main": [
                    [
                        {
                            "node": "Format Response",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Generate Joke": {
                "main": [
                    [
                        {
                            "node": "Format Response",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Format Response": {
                "main": [
                    [
                        {
                            "node": "Respond",
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
        result = n8n.create_workflow(workflow_data)
        
        print("✅ Webhook Workflow Created!")
        print("=" * 70)
        print(f"📋 Name: {result['name']}")
        print(f"🆔 ID: {result['id']}")
        print(f"📦 Nodes: {len(result['nodes'])}")
        print()
        print("🎯 Workflow Structure:")
        print("   1. 🪝 Webhook - Receives POST requests")
        print("   2. 📝 Extract Topic - Gets topic from request")
        print("   3. 🤖 Generate Poem - Creates poem")
        print("   4. 😄 Generate Joke - Creates joke")
        print("   5. 📊 Format Response - Combines results")
        print("   6. 📤 Respond - Sends back to front end")
        print()
        print("=" * 70)
        print("🔗 Open: https://thestarrconspiracy.app.n8n.cloud/workflow/" + result['id'])
        print()
        print("📌 NEXT STEPS:")
        print("   1. Open the workflow and ACTIVATE it")
        print("   2. Add OpenAI credentials to nodes 3 & 4")
        print("   3. Copy the webhook URL (will be shown in the Webhook node)")
        print("   4. Use that URL in the web front end")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    create_webhook_workflow()
