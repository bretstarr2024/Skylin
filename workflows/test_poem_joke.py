"""
Test Workflow - Generate Poem & Joke (No LinkedIn)
Just generates a poem and joke from a topic - no LinkedIn posting.
"""

import sys
import os
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from n8n_client import N8nClient


def create_test_workflow():
    """Create a simple test workflow for poem and joke generation."""
    
    n8n = N8nClient()
    
    workflow_data = {
        "name": "TEST - Topic to Poem & Joke",
        "nodes": [
            # Node 1: Manual Trigger
            {
                "parameters": {},
                "type": "n8n-nodes-base.manualTrigger",
                "typeVersion": 1,
                "position": [240, 400],
                "id": str(uuid.uuid4()),
                "name": "Start"
            },
            
            # Node 2: Set the topic
            {
                "parameters": {
                    "assignments": {
                        "assignments": [
                            {
                                "id": str(uuid.uuid4()),
                                "name": "topic",
                                "value": "AI and the future of creativity",
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
                "name": "Set Topic"
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
            
            # Node 5: Format Output
            {
                "parameters": {
                    "jsCode": "// Collect both outputs\nconst topic = $('Set Topic').first().json.topic;\nconst poem = $('Generate Poem').first().json.message?.content || $('Generate Poem').first().json.output || 'No poem generated';\nconst joke = $('Generate Joke').first().json.message?.content || $('Generate Joke').first().json.output || 'No joke generated';\n\nreturn [{\n  json: {\n    topic: topic,\n    poem: poem,\n    joke: joke,\n    summary: `\\n📝 POEM:\\n${poem}\\n\\n😄 JOKE:\\n${joke}`\n  }\n}];"
                },
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [900, 400],
                "id": str(uuid.uuid4()),
                "name": "Show Results"
            }
        ],
        "connections": {
            "Start": {
                "main": [
                    [
                        {
                            "node": "Set Topic",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Set Topic": {
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
                            "node": "Show Results",
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
                            "node": "Show Results",
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
        
        print("✅ Test Workflow Created!")
        print("=" * 60)
        print(f"📋 Name: {result['name']}")
        print(f"🆔 ID: {result['id']}")
        print(f"📦 Nodes: {len(result['nodes'])}")
        print()
        print("🎯 Workflow Structure:")
        print("   1. ▶️  Start - Click to execute")
        print("   2. 📝 Set Topic - Change the topic here")
        print("   3. 🤖 Generate Poem - Creates poem")
        print("   4. 😄 Generate Joke - Creates joke")
        print("   5. 📊 Show Results - Displays both outputs")
        print()
        print("=" * 60)
        print("🔗 Open: https://thestarrconspiracy.app.n8n.cloud/workflow/" + result['id'])
        print()
        print("⚠️  IMPORTANT: You still need to add OpenAI credentials in n8n:")
        print("   1. Open the workflow")
        print("   2. Click on 'Generate Poem' node")
        print("   3. Select or create OpenAI credentials")
        print("   4. Same for 'Generate Joke' node")
        print("   5. Then click 'Execute Workflow'!")
        
        return result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


if __name__ == "__main__":
    create_test_workflow()
