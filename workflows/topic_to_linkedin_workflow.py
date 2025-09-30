"""
Topic to LinkedIn Workflow
Takes a topic, generates a poem and joke using OpenAI, and posts to LinkedIn.
"""

import sys
import os
import uuid

# Add parent directory to path to import clients
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from n8n_client import N8nClient


def create_topic_to_linkedin_workflow():
    """
    Create a workflow that:
    1. Accepts a topic input
    2. Generates a poem using OpenAI
    3. Generates a joke using OpenAI
    4. Posts both to LinkedIn
    """
    
    # Initialize n8n client
    n8n = N8nClient()
    
    # Define the workflow structure
    workflow_data = {
        "name": "Topic to LinkedIn - Poem & Joke",
        "nodes": [
            # Node 1: Manual Trigger with topic input
            {
                "parameters": {},
                "type": "n8n-nodes-base.manualTrigger",
                "typeVersion": 1,
                "position": [240, 400],
                "id": str(uuid.uuid4()),
                "name": "Start - Enter Topic"
            },
            
            # Node 2: Set the topic variable
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
            
            # Node 3: OpenAI - Generate Poem
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
                                "content": "=Write a creative and inspiring poem about: {{ $json.topic }}\n\nThe poem should be:\n- 4-8 lines long\n- Professional and LinkedIn-appropriate\n- Thoughtful and engaging\n- Include relevant hashtags at the end\n\nReturn only the poem text, nothing else."
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
            
            # Node 4: OpenAI - Generate Joke
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
                                "content": "=Write a clever, professional joke about: {{ $json.topic }}\n\nThe joke should be:\n- Workplace-appropriate\n- Smart and witty\n- Relatable to professionals\n- Include relevant hashtags at the end\n\nReturn only the joke, nothing else."
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
            
            # Node 5: Merge poem and joke data
            {
                "parameters": {
                    "mode": "combine",
                    "combinationMode": "mergeByPosition",
                    "options": {}
                },
                "type": "n8n-nodes-base.merge",
                "typeVersion": 3.2,
                "position": [900, 400],
                "id": str(uuid.uuid4()),
                "name": "Merge Results"
            },
            
            # Node 6: Format for LinkedIn - Poem
            {
                "parameters": {
                    "jsCode": "// Format the poem for LinkedIn posting\nconst topic = $('Set Topic').first().json.topic;\nconst poem = $('Generate Poem').first().json.message?.content || $('Generate Poem').first().json.output || '';\n\nconst formattedPost = `📝 A Poem About: ${topic}\\n\\n${poem}\\n\\n---\\nGenerated with AI ✨`;\n\nreturn [{\n  json: {\n    topic: topic,\n    content: poem,\n    formatted_post: formattedPost,\n    type: 'poem'\n  }\n}];"
                },
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [1120, 300],
                "id": str(uuid.uuid4()),
                "name": "Format Poem Post"
            },
            
            # Node 7: Format for LinkedIn - Joke
            {
                "parameters": {
                    "jsCode": "// Format the joke for LinkedIn posting\nconst topic = $('Set Topic').first().json.topic;\nconst joke = $('Generate Joke').first().json.message?.content || $('Generate Joke').first().json.output || '';\n\nconst formattedPost = `😄 Here's a little humor about: ${topic}\\n\\n${joke}\\n\\n---\\nGenerated with AI ✨`;\n\nreturn [{\n  json: {\n    topic: topic,\n    content: joke,\n    formatted_post: formattedPost,\n    type: 'joke'\n  }\n}];"
                },
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [1120, 500],
                "id": str(uuid.uuid4()),
                "name": "Format Joke Post"
            },
            
            # Node 8: LinkedIn - Post Poem
            {
                "parameters": {
                    "resource": "post",
                    "text": "={{ $json.formatted_post }}",
                    "options": {}
                },
                "type": "n8n-nodes-base.linkedIn",
                "typeVersion": 1,
                "position": [1340, 300],
                "id": str(uuid.uuid4()),
                "name": "Post Poem to LinkedIn"
            },
            
            # Node 9: LinkedIn - Post Joke
            {
                "parameters": {
                    "resource": "post",
                    "text": "={{ $json.formatted_post }}",
                    "options": {}
                },
                "type": "n8n-nodes-base.linkedIn",
                "typeVersion": 1,
                "position": [1340, 500],
                "id": str(uuid.uuid4()),
                "name": "Post Joke to LinkedIn"
            }
        ],
        "connections": {
            "Start - Enter Topic": {
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
                            "node": "Merge Results",
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
                            "node": "Merge Results",
                            "type": "main",
                            "index": 1
                        }
                    ]
                ]
            },
            "Merge Results": {
                "main": [
                    [
                        {
                            "node": "Format Poem Post",
                            "type": "main",
                            "index": 0
                        },
                        {
                            "node": "Format Joke Post",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Format Poem Post": {
                "main": [
                    [
                        {
                            "node": "Post Poem to LinkedIn",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            },
            "Format Joke Post": {
                "main": [
                    [
                        {
                            "node": "Post Joke to LinkedIn",
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
        print("🚀 Creating 'Topic to LinkedIn - Poem & Joke' Workflow...")
        print("=" * 60)
        
        # Create the workflow
        result = n8n.create_workflow(workflow_data)
        
        print(f"✅ Workflow created successfully!")
        print(f"\n📋 Workflow Details:")
        print(f"   Name: {result.get('name')}")
        print(f"   ID: {result.get('id')}")
        print(f"   Nodes: {len(result.get('nodes', []))}")
        
        print("\n🎯 Workflow Structure:")
        print("   1. 🎬 Start - Enter Topic (manual trigger)")
        print("   2. 📝 Set Topic (configure your topic here)")
        print("   3. 🤖 Generate Poem (OpenAI)")
        print("   4. 😄 Generate Joke (OpenAI)")
        print("   5. 🔀 Merge Results (combine data)")
        print("   6. 📄 Format Poem Post (prepare for LinkedIn)")
        print("   7. 📄 Format Joke Post (prepare for LinkedIn)")
        print("   8. 📤 Post Poem to LinkedIn")
        print("   9. 📤 Post Joke to LinkedIn")
        
        print("\n" + "=" * 60)
        print("🎉 Workflow scaffolding is ready!")
        print("\n💡 Next steps:")
        print("   1. Open the workflow in your n8n UI")
        print("   2. Add your OpenAI API credentials")
        print("   3. Add your LinkedIn API credentials")
        print("   4. Edit the 'Set Topic' node to change the default topic")
        print("   5. Test the workflow!")
        
        return result
        
    except Exception as e:
        print(f"❌ Error creating workflow: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main function to run the workflow creation."""
    print("\n🎨 Topic to LinkedIn Workflow Creator")
    print("=" * 60)
    
    try:
        workflow = create_topic_to_linkedin_workflow()
        
        if workflow:
            print("\n✨ All done! Check your n8n instance to see the workflow.")
            print(f"\n🔗 Direct link: https://thestarrconspiracy.app.n8n.cloud/workflow/{workflow.get('id')}")
        else:
            print("\n❌ Failed to create workflow. Check the error messages above.")
            
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\n💡 Make sure your N8N_API_URL and N8N_API_TOKEN are set in .env")
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
