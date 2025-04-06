from pathlib import Path
from datetime import datetime

def write_to_markdown(file_path, test_case_name, content):
    """
    Write formatted markdown content to a file with timestamped filename.
    Creates the file and directories if they don't exist.
    
    Args:
        file_path (str): Path to the directory where the file will be created
        test_case_name (str): Name of the test case
        content (str|dict): Content to write
    """
    # Create timestamp and filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_case_name}_{timestamp}.md"
    
    # Create full path (more explicit way)
    path = Path(file_path).joinpath(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    #print(f" {path}")
    # Format content with test case name
    if (content is None) or (content == ""):
        print("No content to write.")
        return
    formatted_content = format_markdown(content, level=2)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(formatted_content)

    return path

def format_markdown(content, level=2):
    """
    Format content as markdown with proper heading levels.
    
    Args:
        content (str|dict): Content to format
        level (int): Heading level for sections
    
    Returns:
        str: Formatted markdown content
    """
    if not content:
        return ""
        
    formatted = []
    
    if isinstance(content, dict):
        for key, value in content.items():
            formatted.append(f"{'#' * level} {key}\n{value}")
    else:
        # Handle string or other content types directly
        formatted.append(str(content))
    
    return "\n\n".join(formatted)

def append_to_markdown(fpath, content):

    try:
        # Convert Path object to string if file_path is a Path object
        if isinstance(fpath, Path):
            fpath = str(fpath)
        
        # Check if the file path is valid (not None and is a string)
        if fpath is None or not isinstance(fpath, str):
            print("Invalid file path:", fpath)
            return
    
        with open(Path(fpath), 'a', encoding='utf-8') as file:
            file.write(content + "\n")  # Append the formatted text with a new line
        print(f"Text successfully appended to {fpath}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    # Example with string content
    text_content = "This is a test entry with **bold** and *italic* text."
    append_to_markdown("test_output.md", text_content)
    
    # Example with dictionary content
    dict_content = {
        "Response": "This is the model response",
        "Parameters": "temperature=0.7, max_tokens=100"
    }
    append_to_markdown("test_output.md", dict_content)
