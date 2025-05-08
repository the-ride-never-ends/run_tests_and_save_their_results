"""
Utility function to scan for corner-cutting indicators in code.
"""
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Set


def run_command(configs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Scan codebase for corner-cutting indicators.
    
    Args:
        configs: Configuration dictionary
        
    Returns:
        Dict: A dictionary with scan results containing:
            - total_files_scanned: The number of files scanned
            - issues: List of detected issues
    """
    # Get lazy words and phrases from JSON file
    lazy_words_file = Path(__file__).parent.parent.parent.parent / "reports" / "services" / "lazy_words_and_phrases.json"
    
    if not lazy_words_file.exists():
        raise FileNotFoundError(f"Lazy words file not found at {lazy_words_file}")
    
    with open(lazy_words_file, 'r') as f:
        lazy_words_data = json.load(f)
    
    # Extract patterns to search for
    patterns = lazy_words_data.get('patterns', {})
    
    # Get project root directory
    project_dir = Path(configs.test_dir).parent.resolve()
    
    # Prepare result
    result = {
        "total_files_scanned": 0,
        "issues": []
    }
    
    # Scan files
    for root, _, files in os.walk(project_dir):
        root_path = Path(root)
        
        # Skip directories like venv, __pycache__, etc.
        if any(part.startswith('.') or part == 'venv' or part == '__pycache__' for part in root_path.parts):
            continue
        
        for file in files:
            # Only scan Python files
            if not file.endswith('.py'):
                continue
                
            file_path = root_path / file
            
            # Check if file should be ignored
            if configs.respect_gitignore and configs.gitignore_spec:
                from utils.common.should_ignore_file import should_ignore_file
                if should_ignore_file(str(file_path), configs.gitignore_spec):
                    continue
            
            # Scan the file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                result["total_files_scanned"] += 1
                
                # Check for each pattern
                for category, category_patterns in patterns.items():
                    for pattern_info in category_patterns:
                        pattern = pattern_info['pattern']
                        description = pattern_info['description']
                        
                        # Search for pattern in the file content
                        for i, line in enumerate(content.split('\n')):
                            if re.search(pattern, line, re.IGNORECASE):
                                result["issues"].append({
                                    "file": str(file_path.relative_to(project_dir)),
                                    "line": i + 1,
                                    "category": category,
                                    "pattern": pattern,
                                    "message": description,
                                    "snippet": line.strip()
                                })
            except Exception as e:
                # Log error but continue scanning
                print(f"Error scanning {file_path}: {e}")
    
    return result