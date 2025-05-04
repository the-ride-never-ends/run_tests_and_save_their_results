"""
Script to identify corner cutting in a given file.
Corner cutting is defined as implementation shortcuts, temporary solutions, or placeholders 
that are likely to need improvement or replacement in the future.

Corner cutting is identified programmatically by checking for the presence of certain keywords in the file's comments and docstrings.
"""
import ast
from datetime import datetime
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List

from utils.common.results import Results


class CornerCuttingCollector:


    def __init__(self):
        """Initialize the report."""
        self.name = "corner_cutting"
        self.results: Results = Results(name=self.name)
        self.lazy_words: list[str] = self.load_lazy_words()


    @staticmethod
    def load_lazy_words() -> list[str]:
        """
        Load the list of lazy words and phrases from the JSON file.

        Returns:
            list[str]: A list of words and phrases that indicate corner cutting.
        """
        path = Path(__file__).parent / "lazy_words_and_phrases.json"
    
        with open(path, 'r') as f:
            data = json.load(f)

        return data["lazy_words_and_phrases"]


    @staticmethod
    def _extract_single_line_comments(
        file_content: str, 
        comments_and_docstrings: list
    ) -> list[tuple[str, int]]:
        """
        Extracts single-line comments from Python code.
        This static method parses a file's content line by line to identify single-line
        comments (starting with '#') while properly handling cases where '#' characters
        appear inside string literals.
        Args:
            file_content (str): The content of the Python file as a string.
            comments_and_docstrings (list): A list to which extracted comments will be added.
                Each comment is added as a tuple of (comment_text, line_number).
        Returns:
            list[tuple[str, int]]: A list of tuples containing the comment text and corresponding
                line number, though the function actually modifies the input list in-place.
        Note:
            This method ignores empty lines and only extracts the text that follows the '#' character.
            It properly handles both single and double quoted strings to avoid extracting '#' characters
            that are part of string literals.
        """
        # Extract single-line comments using regex to find them
        for idx, line in enumerate(file_content.split('\n'), start=1):
            # Find comments while ignoring # inside strings
            stripped = line.strip()
            in_string = False
            string_char = None
            pos = 0
            
            # Skip empty lines
            if not stripped:
                continue
                
            # Scan through the line to find comments not in strings
            while pos < len(stripped):
                char = stripped[pos]
                # Toggle string state if quote is found and not escaped
                if char in ['"', "'"]:
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char and (pos == 0 or stripped[pos-1] != '\\'):
                        in_string = False
                # Found a comment outside of a string
                elif char == '#' and not in_string:
                    comment = stripped[pos+1:].strip()
                    comments_and_docstrings.append((comment, idx))
                    break
                pos += 1


    @staticmethod
    def _extract_docstrings_ast(file_content: str, comments_and_docstrings: list):
        """Extract docstrings from Python code using the AST module.
        
        Recursively finds all docstrings in modules, classes, and functions
        in the provided code and adds them to the comments_and_docstrings list.
        
        Args:
            file_content: String containing Python source code to analyze.
            comments_and_docstrings: list to which extracted docstrings will be added
                as (docstring_line, line_number) tuples.
        
        Raises:
            SyntaxError: If the Python code cannot be parsed by the AST module.
        """
        # Parse file content using ast
        parsed_ast = ast.parse(file_content)
        
        # Function to recursively extract docstrings from AST nodes
        def extract_docstrings_from_node(node):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                docstring = ast.get_docstring(node)
                if docstring:
                    # Calculate line number (docstring is after the definition line)
                    line_num = node.lineno
                    if isinstance(node, ast.Module):
                        line_num = 1
                    for ds_line in docstring.split('\n'):
                        comments_and_docstrings.append((ds_line.strip(), line_num))
                        line_num += 1
            
            # Recursively process child nodes
            for child in ast.iter_child_nodes(node):
                extract_docstrings_from_node(child)
        
        extract_docstrings_from_node(parsed_ast)

    @staticmethod
    def _extract_docstrings_regex(file_content: str, comments_and_docstrings: list) -> None:
        """
        Extract docstrings using regex to find them.

        Args:
            file_content (str): The content of the Python file.
            comments_and_docstrings (list): list to store extracted comments and docstrings.
        """
        docstrings = re.finditer(
            r'(?:"""(.*?)""")|(?:\'\'\'(.*?)\'\'\')', file_content, re.DOTALL
        )
        for match in docstrings:
            docstring = match.group(1) or match.group(2)
            if docstring:
                start_position = match.start()
                line_number = file_content[:start_position].count('\n') + 1
                
                docstring_lines = docstring.split('\n')
                for j, ds_line in enumerate(docstring_lines):
                    comments_and_docstrings.append((ds_line.strip(), line_number + j))


    def identify_corner_cutting(self, file_path: str) -> dict[str, list[tuple[str, int]]]:
        """
        Identify instances of corner cutting in a file by checking for 
        lazy words and phrases in comments and docstrings.
        
        Args:
            file_path (str): The path to the file to check.
            
        Returns:
            dict[str, list[tuple[str, int]]]: A dictionary mapping lazy words 
            to lists of tuples containing the context and line number.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return {}

        results = {
            "file_path": file_path,
            "text": "",
            "total_corner_cutting_instances": 0
        }
        comments_and_docstrings = []

        # Get all comments and docstrings with their line numbers.
        self._extract_single_line_comments(content, comments_and_docstrings)
        try:
            self._extract_docstrings_ast(content, comments_and_docstrings)
        except SyntaxError:
            self._extract_docstrings_regex(content, comments_and_docstrings)

        # Check each comment and docstring for lazy words
        for text, line_number in comments_and_docstrings:
            for word in self.lazy_words:
                if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE):
                    if word not in results:
                        results[word] = []
                    results[word].append((text, line_number))
        return results


    # TODO Finish this method
    def generate_markdown_report(self) -> str:
        """
        Generate a Markdown report of the corner cutting instances.
        
        Args:
            report (dict): The corner cutting report.
            
        Returns:
            str: The Markdown report as a string.
        """
        timestamp = datetime.fromisoformat(self.results.timestamp)

        # Build markdown content
        content: list[str] = [
            "# Corner Cutting Report\n"
            f"Generated on: {timestamp.strftime("%Y-%m-%d %H:%M:%S")}\n",
            "## Summary\n",
            f"- **Total corner cutting instances**: {self.results.status.upper()} ({self.results.errors} potential issues)\n",
        ]

        # Add flake8 issues
        if self.results.issues:
            content.append("## Potential Corner Cutting Issues\n")

            # Group issues by file
            files_with_issues: Dict[str, List[Dict[str, Any]]] = {}
            for issue in self.results.issues:
                file_path = issue.get("file", "Unknown file")
                if file_path not in files_with_issues:
                    files_with_issues[file_path] = []
                files_with_issues[file_path].append(issue)

            # Add issues by file
            for file_path, issues in files_with_issues.items():
                content.append(f"### {file_path}\n\n")

                for issue in issues:
                    line = issue.get("line", "")
                    column = issue.get("column", "")
                    message = issue.get("message", "")
                    error_code = issue.get("error_code", "")

                    location = f"Line {line}"
                    if column:
                        location += f", Col {column}"

                    content.append(f"- {location}: {error_code} {message}")

                content.append("")


        output += f"**Total corner cutting instances:** {report['total_corner_cutting_instances']}\n"

        if self.results.total_potential_instances  > 0:
            output += "## Details:\n"
            for word, instances in report['corner_cutting_details'].items():
                output += f"\n### '{word}' appears in:\n"
                for context, line in instances:
                    output += f"- Line {line}: \"{context}\"\n"

        return output

    # TODO Finish this method
    def run(self, target_dir: str) -> dict:
        """
        Generate a report of corner cutting instances in a file.
        
        Args:
            file_path (str): The path to the file to check.
            
        Returns:
            dict: A report containing information about corner cutting instances.
        """
        total_files_scanned = 0
        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith('.py'):

                    self.results.file_path = file_path = os.path.join(root, file)
                    corner_cutting_instances: dict = self.identify_corner_cutting(file_path)
                    total_potential_instances += sum(len(instances) for instances in corner_cutting_instances.values())

                    total_files_scanned += 1

        self.results.total_files_scanned = total_files_scanned
        self.results.total_potential_instances = total_potential_instances
        self.results.timestamp = datetime.now().isoformat()

        report = {
            "file_path": file_path,
            "total_corner_cutting_instances": total_instances,
            "timestamp": corner_cutting_instances
        }
        
        return report
