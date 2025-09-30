# n8n Workflow Manager with Airtable Integration

A Python-based project for programmatically managing n8n workflows with Airtable integration.

## Features

- Connect to n8n API for workflow management
- Integrate with Airtable for data operations
- Create, update, and manage workflows programmatically
- Version control workflows with Git

## Setup

### Prerequisites

- Python 3.8 or higher
- n8n instance with API access
- Airtable account with API token

### Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd Skylin
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Copy `.env` file and add your tokens:
     - `N8N_API_URL`: Your n8n instance API URL
     - `N8N_API_TOKEN`: Your n8n API token
     - `AIRTABLE_API_TOKEN`: Your Airtable API token
     - `AIRTABLE_BASE_ID`: Your Airtable base ID

## Usage

### Running the Workflow Manager

```bash
python main.py
```

### Creating Workflows

```bash
python workflows/crazy_daves_workflow.py
```

## Project Structure

```
Skylin/
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── main.py               # Main application entry point
├── n8n_client.py         # n8n API client
├── airtable_client.py    # Airtable API client
└── workflows/            # Workflow definitions
    └── crazy_daves_workflow.py
```

## API Documentation

- [n8n API Documentation](https://docs.n8n.io/api/)
- [Airtable API Documentation](https://airtable.com/developers/web/api/introduction)

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

MIT License
