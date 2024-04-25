import os
import gradio as gr
import sys, io
import sqlite3
import asyncio
from functools import wraps
import urllib.request
import zipfile
import tempfile
import shutil
import site
import swarmauri_developer
from swarmauri.standard.models.concrete.OpenAIModel import OpenAIModel
from swarmauri.standard.vector_stores.concrete.MLMVectorStore import MLMVectorStore
from swarmauri.standard.conversations.concrete.LimitedSystemContextConversation import LimitedSystemContextConversation
from swarmauri.standard.agents.concrete.RagAgent import RagAgent

class DeveloperAssistant:
    def __init__(self, api_key, db_path='prompt_responses.db', vector_store_path=None):
        print('Initializing... this will take a moment.')
        self.api_key = api_key
        self.db_path = db_path
        # Set the default path to the vector_store_data directory relative to the location of this script file
        if vector_store_path is None:

            # Get the directory where the current script is located
            base_dir = os.path.dirname(__file__)  

             # Default path to vector store
            self._vector_store_path = os.path.join(base_dir, swarmauri_developer.__default_vector_store_path__)
            
            if not os.path.exists(self._vector_store_path):  # Check if the path does not exist
                self.extract_zip_from_url(swarmauri_developer.__cdn__, base_dir)

        else:
            self._vector_store_path = vector_store_path

        self.conversation = LimitedSystemContextConversation(max_size=36, system_message_content="")
        self.model = OpenAIModel(api_key=self.api_key, model_name="gpt-4-0125-preview")
        self.agent = self.initialize_agent()
        self.css = """
#chat-diaglogue-container {
    min-height: 54vh;
}

#code-block {
    height: 54vh !important;
    overflow-y: scroll !important;
}

footer {
    display: none !important;
}
"""
        self.setup_gradio_interface()


    @property
    def vector_store_path(self):
        return self._vector_store_path

    @vector_store_path.setter
    def vector_store_path(self, value) -> None:
        # First we set the value
        self._vector_store_path = value

        # Then we reload the agent's vector store
        VS = MLMVectorStore()
        VS.load_parts(self.vector_store_path)
        self.agent.vector_store = VS

    def initialize_agent(self):
        VS = MLMVectorStore()
        VS.load_parts(self.vector_store_path)
        agent = RagAgent(name="Rag", model=self.model, conversation=self.conversation, vector_store=VS)
        return agent

    def sql_log(self, prompt, response):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS prompts_responses
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, prompt TEXT, response TEXT)''')
        cursor.execute('''INSERT INTO prompts_responses (prompt, response) VALUES (?, ?)''', (prompt, response))
        conn.commit()
        conn.close()

    async def predict(self, message, history, model_name, top_k=5, temperature=1, max_tokens=10):
        try:
            self.agent.model.model_name = model_name
            response = self.agent.exec(message, top_k=top_k, model_kwargs={'temperature': temperature, 'max_tokens': max_tokens})
            self.sql_log(message, response)
            return response
        except Exception as e:
            return str(e)

    def update_file_explorer(self, path):
        if os.path.isdir(path):
            return gr.FileExplorer(root_dir=path)
        else:
            return "Invalid directory. Please enter a valid path."

    def extract_zip_from_url(self, url, target_folder):
        """
        Extracts a .zip file from the given URL into the specified target folder within site-packages.

        Args:
        url (str): The URL of the .zip file to download and extract.
        target_folder (str): The name of the folder within site-packages to extract the files into.
        """
        # Create a temporary directory to store the downloaded .zip file
        temp_dir = tempfile.mkdtemp()

        try:
            # Download the .zip file
            zip_file_path = os.path.join(temp_dir, os.path.basename(url))
            urllib.request.urlretrieve(url, zip_file_path)

            # Extract the .zip file into the target folder
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(target_folder)

            print("Extraction completed successfully.")
        except Exception as e:
            print("Extraction failed:", e)
        finally:
            # Clean up: Remove the temporary directory
            shutil.rmtree(temp_dir)

    def get_file_name(self, file):
        return file
    
    def get_file_content(self, file):
        return (file,)

    def save_file(self, file_path, file_content):
        try:
            with open(file_path, 'w') as f:
                f.write(file_content)
            return f"File saved successfully at {file_path}"
        except Exception as e:
            return f"Failed to save file: {str(e)}"

    
    def execute_code(self, user_code):
        old_stdout = sys.stdout
        redirected_output = sys.stdout = io.StringIO()

        try:
            exec(user_code, globals())
            sys.stdout = old_stdout
            captured_output = redirected_output.getvalue()
            return str(captured_output)
        except Exception as e:
            sys.stdout = old_stdout
            return f"An error occurred: {str(e)}"

    def setup_gradio_interface(self):
        title = "Developer Assistant"
        description = """
        Unlock the full potential of your software development with our cutting-edge Developer Assistant!
        """
        examples = [
            ['Create a new file in standard/chains/concrete/'],
            ['Create a new file in standard/vectorizers/concrete/'],
            ['Create a new file in standard/vector_stores/concrete/'],
        ]
        
        chatbot = gr.Chatbot(elem_id="chat-diaglogue-container", show_copy_button=True, scale=3, likeable=True, container=True)
        
        additional_inputs = [
            gr.Dropdown(["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4-0125-preview"], value="gpt-4-0125-preview", label="Model", info="Select openai model"),
            gr.Slider(label="Top K", value=20, minimum=0, maximum=100, step=5, interactive=True),
            gr.Slider(label="Temperature", value=1, minimum=0.0, maximum=1.5, step=0.05, interactive=True),
            gr.Slider(label="Max new tokens", value=2048, minimum=256, maximum=4096, step=64, interactive=True)
        ]
        
        chat_interface_stream = gr.ChatInterface(self.predict, 
                                                 title=title, 
                                                 description=description, 
                                                 chatbot=chatbot,
                                                 textbox=gr.Textbox(),
                                                 examples=examples,
                                                 additional_inputs=additional_inputs,
                                                 css=self.css).queue()






        with gr.Blocks(css=self.css) as file_explorer:
            with gr.Group():
                with gr.Row():
                    path_input = gr.Textbox(scale=2, label="Enter Directory Path", value='.')
                    save_path_input = gr.Textbox(scale=2, label="Enter File Path to Save", placeholder="Path/to/your/file.txt")
                    save_button = gr.Button("Save File", scale=1)
                with gr.Row():
                    file = gr.FileExplorer(
                        scale=1,
                        file_count="single",
                        root_dir='.',
                    )
                    file_code = gr.Code(lines=30, scale=2, language="python")
                
            path_input.change(self.update_file_explorer, path_input, file)
            file.change(self.get_file_content, file, file_code)
            file.change(self.get_file_name, file, save_path_input)
            save_button.click(self.save_file, inputs=[save_path_input, file_code], outputs=gr.Textbox(label="Save Status"))


        
        with gr.Blocks(css=self.css) as code_interpreter:
            with gr.Row():
                code_input = gr.Code(language="python", label="Enter your Python code here", elem_id='code-block')
                output = gr.Textbox(label="Output")
            code_input.change(self.execute_code, inputs=code_input, outputs=output)

        self.app = gr.TabbedInterface([chat_interface_stream, file_explorer, code_interpreter], ["Developer Assistant", "File Explorer", "Code Interpreter"], css=self.css)

    def launch(self):
        self.app.launch(share=True)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Swarmauri Developer Assistant Command Line Tool")
    parser.add_argument('-api_key', '--api_key', type=str, help='OPENAI_API_KEY', required=True)
    parser.add_argument('-db_path', '--db_path', type=str, help='path to sqlite3 db', required=False)
    parser.add_argument('-vector_store_path', '--vector_store_path', type=str, help='path to vector store artifacts', required=False)
    args = parser.parse_args()

    api_key = args.api_key
    
    assistant = DeveloperAssistant(api_key=api_key)
    if args.db_path:
        assistant.db_path = args.db_path
    if args.vector_store_path:
        assistant.vector_store_path = args.vector_store_path
    assistant.launch()

if __name__ == "__main__":
    main()