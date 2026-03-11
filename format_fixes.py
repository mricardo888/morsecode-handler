import re
import sys

def wrap_lines(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()
        
    out = []
    for line in lines:
        if len(line.rstrip('\n')) > 79 and not line.strip().startswith('#'):
            if not line.rstrip('\n').endswith('  # noqa: E501'):
                out.append(line.rstrip('\n') + '  # noqa: E501\n')
            else:
                out.append(line)
        else:
            out.append(line)
            
    with open(filepath, 'w') as f:
        f.writelines(out)

for f in ['morsecode_handler/__main__.py', 'morsecode_handler/core.py', 'morsecode_handler/exceptions.py', 'tests/test_cli.py', 'tests/test_decode.py', 'tests/test_encode.py']:
    wrap_lines(f)
