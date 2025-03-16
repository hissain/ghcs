import google.generativeai as genai
import dotenv
import json
import os
import subprocess
import glob
import sys

dotenv.load_dotenv()

def extract_code_with_gemini(directory_path, remark, verbose=False, file_extensions=None):
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        return "Error: GEMINI_API_KEY not found in environment variables."
    
    genai.configure(api_key=gemini_api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    
    if file_extensions is None:
        file_extensions = ['.py', '.js', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.php', '.rb', '.go', '.rs', '.ts']
    
    files_content = {}
    file_count = 0
    total_size = 0
    
    if verbose:
        print(f"Scanning directory: {directory_path}")
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            if file_extensions and not any(file.endswith(ext) for ext in file_extensions):
                if verbose:
                    print(f"Skipping non-code file: {file_path}")
                continue
                
            try:
                file_size = os.path.getsize(file_path)
                if file_size > 1_000_000:  # 1MB
                    if verbose:
                        print(f"Skipping large file ({file_size/1_000_000:.2f}MB): {file_path}")
                    continue
                    
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                    files_content[file_path] = content
                    file_count += 1
                    total_size += len(content)
                    
                    if verbose:
                        print(f"Read file ({len(content)} chars): {file_path}")
            except Exception as e:
                if verbose:
                    print(f"Error reading file {file_path}: {e}")
                files_content[file_path] = f"Error reading file: {e}"
    
    if verbose:
        print(f"Found {file_count} files with total size of {total_size} characters")
    
    if not files_content:
        return "No code files found in the specified directory."
    
    prompt = f"""
    I have the following code files from a project:
    
    {json.dumps(files_content, indent=2)}
    
    Based on this description: "{remark}", please extract the relevant code sections and provide a cleaned-up, functional version of the code that focuses specifically on what was requested.
    
    Format your response as:
    ```python
    # Extracted code here
    ```
    
    Include only the code and very necessary comments, no explanations outside the code block.
    """
    
    try:
        if verbose:
            print(f"Sending request to Gemini API with {len(prompt)} characters...")
        
        token_limit = 30000  # Approximate limit for Gemini
        if len(prompt) > token_limit:
            if verbose:
                print(f"Warning: Prompt size ({len(prompt)} chars) exceeds recommended limit. Truncating files...")
            
            # More sophisticated truncation strategy - keep most important files
            important_files = {}
            current_size = len(prompt) - len(json.dumps(files_content, indent=2))
            sorted_files = sorted(files_content.items(), key=lambda x: len(x[1]))
            
            for file_path, content in sorted_files:
                file_entry = json.dumps({file_path: content}, indent=2)[1:-1]  # Remove outer braces
                if current_size + len(file_entry) + 5 < token_limit:  # 5 for commas and formatting
                    important_files[file_path] = content
                    current_size += len(file_entry) + 5
                else:
                    if verbose:
                        print(f"Skipping file due to token limit: {file_path}")
            
            files_content = important_files

            prompt = f"""
            I have the following code files from a project (note: some files were omitted due to size constraints):
            
            {json.dumps(files_content, indent=2)}
            
            Based on this description: "{remark}", please extract the relevant code sections and provide a cleaned-up, functional version of the code that focuses specifically on what was requested.
            
            Format your response as:
            ```python
            # Extracted code here
            ```
            
            Include only the code and very necessary comments, no explanations outside the code block.
            """
        response = model.generate_content(prompt)
        content = response.text
        
        if "```python" in content and "```" in content.split("```python", 1)[1]:
            extracted_code = content.split("```python", 1)[1].split("```", 1)[0].strip()
        elif "```" in content:
            extracted_code = content.split("```", 2)[1].strip()
        else:
            extracted_code = content
        
        return extracted_code
    
    except Exception as e:
        if verbose:
            print(f"Error calling Gemini API: {e}")
        return f"Error extracting code with Gemini: {e}"

def convert_nb_to_python(directory_path, verbose=False):
    try:
        import nbconvert
        use_subprocess = False
    except ImportError:
        try:
            subprocess.run(['jupyter', 'nbconvert', '--version'], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE, 
                          check=True)
            use_subprocess = True
        except (subprocess.CalledProcessError, FileNotFoundError):
            sys.stderr.write("Error: jupyter nbconvert is not installed. Please install it with:\n")
            sys.stderr.write("pip install nbconvert\n")
            return []
    
    # Find all .ipynb files in the directory and its subdirectories
    notebook_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.ipynb'):
                notebook_files.append(os.path.join(root, file))
    
    if verbose:
        print(f"Found {len(notebook_files)} notebook files to convert")
    
    converted_files = []
    
    for nb_file in notebook_files:
        try:
            if verbose:
                print(f"Converting {nb_file} to Python...")
            
            if use_subprocess:
                result = subprocess.run(
                    ['jupyter', 'nbconvert', '--to', 'python', nb_file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if result.returncode != 0:
                    if verbose:
                        print(f"Error converting {nb_file}: {result.stderr}")
                    continue
            else:
                from nbconvert import PythonExporter
                from nbformat import read

                with open(nb_file, 'r', encoding='utf-8') as f:
                    nb_content = read(f, as_version=4)
                
                python_exporter = PythonExporter()
                
                (python_code, _) = python_exporter.from_notebook_node(nb_content)
                py_file = nb_file.replace('.ipynb', '.py')
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(python_code)
            
            py_file = nb_file.replace('.ipynb', '.py')
            
            if os.path.exists(py_file):
                converted_files.append(py_file)
                os.remove(nb_file)
                if verbose:
                    print(f"Converted and deleted {nb_file}")
            else:
                if verbose:
                    print(f"Python file {py_file} was not created")
                
        except Exception as e:
            if verbose:
                print(f"Error processing {nb_file}: {str(e)}")
    
    if verbose:
        print(f"Successfully converted {len(converted_files)} notebooks to Python files")
    
    return converted_files

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) > 1:
        directory = sys.argv[1]
        if sys.argv[1] == '--convert-notebooks' and len(sys.argv) > 2:
            convert_nb_to_python(sys.argv[2], verbose=True)
        elif len(sys.argv) > 2:
            remark = sys.argv[2]
            result = extract_code_with_gemini(directory, remark, verbose=True)
            print(result)
        else:
            print("Usage: python extract_code.py [--convert-notebooks] <directory_path> [remark]")
    else:
        print("Usage: python extract_code.py [--convert-notebooks] <directory_path> [remark]")