# Swarmauri Developer Assistant

## Overview
The Swarmauri Developer Assistant is part of the swarmaURI framework and is designed to enable developers to rapidly develop with the Swarmauri Sdk.. This tool is designed to enhance software development workflows by integrating an advanced AI with pretrained vectorizers and document retrieval. The assistant features a web gui with chatbot, file explorer and editor, and code interpreter.

## Features
- **AI-Powered Coding Assistance:** Utilize OpenAI's models for real-time coding help and documentation.
- **File Management Interface:** Navigate and manage your project files within a robust Gradio interface.
- **Code Execution Environment:** Execute Python code snippets directly from the interface.
- **Database Integration:** Automatically log interactions in a SQLite database for analysis or record-keeping.
- **Vector Store Integration:** Efficiently handle and retrieve data using the MLMVectorStore component.

## Installation
You can install the Swarmauri Developer Assistant directly via pip:

```bash
pip install swarmauri_developer
```

This command will install the latest version of the Swarmauri Developer Assistant along with its dependencies.

## Usage


### Client-Based Usage
Once installed, you can run the Developer Assistant from the command line:

```bash
developer_assistant --api_key YOUR_OPENAI_API_KEY
```

Optional command line arguments include:
- `--db_path`: Path to the SQLite database file.
- `--vector_store_path`: Path to the vector store data directory.


### Programmatic Usage
```python
from swarmauri_developer import DeveloperAssistant

api_key = "<OPENAI_API_KEY>"
assistant = DeveloperAssistant(api_key)
assistant.launch()
```
These arguments allow you to customize the storage locations used by the Assistant.

## Documentation
Further documentation detailing the functionalities and module descriptions is available on the [GitHub repository](http://github.com/swarmauri/developer_assistant).

## Contributing
We welcome contributions to the Swarmauri Developer Assistant. Please consult the `CONTRIBUTING.md` file for guidelines on how to make contributions.

## License
This project's license is pending status. At present, no license is issued.

## Contact
For more information or support, please contact [corporate@swarmauri.com](mailto:corporate@swarmauri.com).
