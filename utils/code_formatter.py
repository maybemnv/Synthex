from typing import Optional
import black
import autopep8
import re
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, Python3Lexer

class CodeFormatter:
    """Utility class for code formatting across Synthex application"""
    
    SUPPORTED_LANGUAGES = {
        "python": "python",
        "javascript": "javascript",
        "typescript": "typescript",
        "java": "java",
        "cpp": "cpp",
        "csharp": "csharp"
    }

    def __init__(self):
        self.html_formatter = HtmlFormatter(
            style='monokai',
            linenos=True,
            cssclass="source"
        )

    def format_code(self, code: str, language: str, max_length: int = 88) -> str:
        """Format code according to language-specific standards"""
        if not code.strip():
            return ""

        language = language.lower()
        
        try:
            if language == "python":
                return self._format_python(code, max_length)
            else:
                # For other languages, just ensure consistent indentation
                return self._format_generic(code)
        except Exception as e:
            print(f"Formatting error: {str(e)}")
            return code  # Return original code if formatting fails

    def _format_python(self, code: str, max_length: int) -> str:
        """Format Python code using black and autopep8"""
        try:
            # First pass with autopep8 for basic PEP8 compliance
            code = autopep8.fix_code(
                code,
                options={'max_line_length': max_length}
            )
            
            # Second pass with black for consistent styling
            code = black.format_str(
                code,
                mode=black.FileMode(
                    line_length=max_length
                )
            )
            return code
        except Exception:
            return self._format_generic(code)

    def _format_generic(self, code: str) -> str:
        """Basic formatting for any programming language"""
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            # Remove trailing whitespace
            stripped = line.rstrip()
            
            # Adjust indent level based on brackets
            if re.search(r'[{}]\s*$', stripped):
                formatted_lines.append('    ' * indent_level + stripped)
                indent_level += 1
            elif stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)
                formatted_lines.append('    ' * indent_level + stripped)
            else:
                formatted_lines.append('    ' * indent_level + stripped)
                
        return '\n'.join(formatted_lines)

    def highlight_code(self, code: str, language: str) -> str:
        """Convert code to HTML with syntax highlighting"""
        try:
            lexer = get_lexer_by_name(
                self.SUPPORTED_LANGUAGES.get(language.lower(), 'text')
            )
            return highlight(code, lexer, self.html_formatter)
        except Exception:
            # Fallback to Python highlighting if language not supported
            return highlight(code, Python3Lexer(), self.html_formatter)

    def get_css_styles(self) -> str:
        """Return CSS styles for syntax highlighting"""
        return self.html_formatter.get_style_defs('.source')

    def clean_code(self, code: str) -> str:
        """Remove unnecessary whitespace and normalize line endings"""
        if not code:
            return ""
            
        # Normalize line endings
        code = code.replace('\r\n', '\n')
        
        # Remove trailing whitespace from each line
        lines = [line.rstrip() for line in code.split('\n')]
        
        # Remove multiple blank lines
        formatted_lines = []
        prev_empty = False
        
        for line in lines:
            if not line.strip():
                if not prev_empty:
                    formatted_lines.append('')
                prev_empty = True
            else:
                formatted_lines.append(line)
                prev_empty = False
                
        return '\n'.join(formatted_lines).strip()

# Example usage:
if __name__ == "__main__":
    formatter = CodeFormatter()
    
    # Test Python code formatting
    test_code = """
    def hello_world(name):
        print("Hello, "    +     name)
        return None
    """
    
    formatted = formatter.format_code(test_code, "python")
    print("Formatted Python code:")
    print(formatted)
    
    # Test syntax highlighting
    highlighted = formatter.highlight_code(formatted, "python")
    print("\nHTML with syntax highlighting:")
    print(highlighted)