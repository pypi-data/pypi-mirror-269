__version__ = "0.0.8"
__short_desc__ = """The Swarmauri Developer Assistant is part of the swarmaURI framework and is designed to enable developers to rapidly develop with the Swarmauri Sdk.. This tool is designed to enhance software development workflows by integrating an advanced AI with pretrained vectorizers and document retrieval. The assistant features a web gui with chatbot, file explorer and editor, and code interpreter."""
__long_desc__ = """# Swarmauri Developer Assistant

## Overview
The Swarmauri Developer Assistant is part of the swarmaURI framework and is designed to enable developers to rapidly develop with the Swarmauri Sdk.. This tool is designed to enhance software development workflows by integrating an advanced AI with pretrained vectorizers and document retrieval. The assistant features a web gui with chatbot, file explorer and editor, and code interpreter.

## Features
- **AI-Powered Coding Assistance:** Utilize OpenAI's models for real-time coding help and documentation.
- **File Management Interface:** Navigate and manage your project files within a robust Gradio interface.
- **Code Execution Environment:** Execute Python code snippets directly from the interface.
- **Database Integration:** Automatically log interactions in a SQLite database for analysis or record-keeping.
- **Vector Store Integration:** Efficiently handle and retrieve data using the MLMVectorStore component.
"""
__cdn__ = f"https://cdn.swarmauri.com/assets/developer_assistant/{__version__.replace('.', '_')}_vector_store_data.zip"
__default_vector_store_path__ = "vector_store_data"
