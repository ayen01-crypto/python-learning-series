"""
Template Engine Module
This module implements a simple template engine for the web framework.
"""

import re
from typing import Dict, Any, List, Union
import html


class Template:
    """Represents a template."""

    def __init__(self, template_string: str):
        self.template_string = template_string
        self.parsed_blocks = self._parse_template(template_string)

    def _parse_template(self, template_string: str) -> List[Dict[str, Any]]:
        """Parse template into blocks."""
        blocks = []
        # Pattern to match template tags
        pattern = r'\{\{(.*?)\}\}|\{\%(.+?)\%\}'
        last_pos = 0
        
        for match in re.finditer(pattern, template_string):
            # Add text before the match
            if match.start() > last_pos:
                blocks.append({
                    'type': 'text',
                    'content': template_string[last_pos:match.start()]
                })
            
            # Process the match
            if match.group(1):  # {{ variable }}
                blocks.append({
                    'type': 'variable',
                    'expression': match.group(1).strip()
                })
            elif match.group(2):  # {% tag %}
                tag_content = match.group(2).strip()
                if tag_content.startswith('if '):
                    blocks.append({
                        'type': 'if_start',
                        'condition': tag_content[3:].strip()
                    })
                elif tag_content == 'endif':
                    blocks.append({
                        'type': 'if_end'
                    })
                elif tag_content.startswith('for '):
                    blocks.append({
                        'type': 'for_start',
                        'expression': tag_content[4:].strip()
                    })
                elif tag_content == 'endfor':
                    blocks.append({
                        'type': 'for_end'
                    })
                else:
                    blocks.append({
                        'type': 'unknown',
                        'content': tag_content
                    })
            
            last_pos = match.end()
        
        # Add remaining text
        if last_pos < len(template_string):
            blocks.append({
                'type': 'text',
                'content': template_string[last_pos:]
            })
        
        return blocks

    def render(self, context: Dict[str, Any] = None) -> str:
        """Render the template with the given context."""
        context = context or {}
        output = []
        stack = []
        
        i = 0
        while i < len(self.parsed_blocks):
            block = self.parsed_blocks[i]
            
            if block['type'] == 'text':
                output.append(block['content'])
            elif block['type'] == 'variable':
                value = self._eval_expression(block['expression'], context)
                output.append(str(value))
            elif block['type'] == 'if_start':
                condition_result = self._eval_condition(block['condition'], context)
                stack.append({
                    'type': 'if',
                    'condition_result': condition_result,
                    'output_index': len(output)
                })
            elif block['type'] == 'if_end':
                if stack and stack[-1]['type'] == 'if':
                    stack.pop()
            elif block['type'] == 'for_start':
                var_name, iterable_expr = block['expression'].split(' in ')
                var_name = var_name.strip()
                iterable = self._eval_expression(iterable_expr.strip(), context)
                
                if hasattr(iterable, '__iter__'):
                    stack.append({
                        'type': 'for',
                        'var_name': var_name,
                        'iterable': list(iterable),
                        'index': 0,
                        'start_index': i,
                        'output_index': len(output)
                    })
                else:
                    # Skip to endfor if not iterable
                    loop_depth = 1
                    while i < len(self.parsed_blocks) and loop_depth > 0:
                        i += 1
                        if self.parsed_blocks[i]['type'] == 'for_start':
                            loop_depth += 1
                        elif self.parsed_blocks[i]['type'] == 'for_end':
                            loop_depth -= 1
            elif block['type'] == 'for_end':
                if stack and stack[-1]['type'] == 'for':
                    for_block = stack[-1]
                    for_block['index'] += 1
                    
                    if for_block['index'] < len(for_block['iterable']):
                        # Reset position to reprocess loop
                        i = for_block['start_index']
                        # Update context with current item
                        context[for_block['var_name']] = for_block['iterable'][for_block['index']]
                    else:
                        # Loop finished, pop from stack
                        stack.pop()
            
            i += 1
        
        return ''.join(output)

    def _eval_expression(self, expression: str, context: Dict[str, Any]) -> Any:
        """Evaluate a template expression."""
        try:
            # Handle simple variable access
            if '.' in expression:
                parts = expression.split('.')
                value = context.get(parts[0])
                for part in parts[1:]:
                    if hasattr(value, part):
                        value = getattr(value, part)
                    elif isinstance(value, dict) and part in value:
                        value = value[part]
                    else:
                        return ''
                return value
            else:
                # Simple variable
                return context.get(expression, '')
        except Exception:
            return ''

    def _eval_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a template condition."""
        try:
            # Simple condition evaluation
            if '==' in condition:
                left, right = condition.split('==')
                left_val = self._eval_expression(left.strip(), context)
                right_val = right.strip().strip('"').strip("'")
                return str(left_val) == right_val
            elif '!=' in condition:
                left, right = condition.split('!=')
                left_val = self._eval_expression(left.strip(), context)
                right_val = right.strip().strip('"').strip("'")
                return str(left_val) != right_val
            else:
                # Check if variable is truthy
                value = self._eval_expression(condition, context)
                return bool(value)
        except Exception:
            return False


class TemplateEngine:
    """Main template engine class."""

    def __init__(self, template_dir: str = "templates"):
        self.template_dir = template_dir
        self.templates = {}

    def load_template(self, template_name: str) -> Template:
        """Load a template from file."""
        if template_name in self.templates:
            return self.templates[template_name]
        
        try:
            with open(f"{self.template_dir}/{template_name}", 'r') as f:
                template_content = f.read()
            template = Template(template_content)
            self.templates[template_name] = template
            return template
        except FileNotFoundError:
            raise Exception(f"Template '{template_name}' not found")

    def render_template(self, template_name: str, context: Dict[str, Any] = None) -> str:
        """Render a template with the given context."""
        template = self.load_template(template_name)
        return template.render(context)

    def render_string(self, template_string: str, context: Dict[str, Any] = None) -> str:
        """Render a template from a string."""
        template = Template(template_string)
        return template.render(context)


# Global template engine instance
template_engine = TemplateEngine()


# Convenience functions
def render_template(template_name: str, context: Dict[str, Any] = None) -> str:
    """Render a template."""
    return template_engine.render_template(template_name, context)


def render_string(template_string: str, context: Dict[str, Any] = None) -> str:
    """Render a template string."""
    return template_engine.render_string(template_string, context)


# Example usage:
"""
template_str = '''
<html>
<head><title>{{ title }}</title></head>
<body>
    <h1>{{ heading }}</h1>
    {% if show_list %}
    <ul>
    {% for item in items %}
        <li>{{ item.name }} - {{ item.value }}</li>
    {% endfor %}
    </ul>
    {% endif %}
</body>
</html>
'''

context = {
    'title': 'My Page',
    'heading': 'Welcome',
    'show_list': True,
    'items': [
        {'name': 'Item 1', 'value': 100},
        {'name': 'Item 2', 'value': 200}
    ]
}

template = Template(template_str)
result = template.render(context)
print(result)
"""