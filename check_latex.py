import re
import sys

def check_balance(text, open_char, close_char, open_name, close_name):
    stack = []
    for i, ch in enumerate(text):
        if ch == open_char:
            stack.append((ch, i))
        elif ch == close_char:
            if not stack:
                return f"Unmatched {close_name} at position {i}"
            stack.pop()
    if stack:
        return f"Unmatched {open_name} at position {stack[0][1]}"
    return None

def check_begin_end(text):
    # Find all \begin{...} and \end{...}
    begin_pattern = r'\\begin{([^}]*)}'
    end_pattern = r'\\end{([^}]*)}'
    begins = [(m.start(), m.group(1)) for m in re.finditer(begin_pattern, text)]
    ends = [(m.start(), m.group(1)) for m in re.finditer(end_pattern, text)]
    # We'll use a stack for environments
    stack = []
    for pos, env in begins:
        stack.append((env, pos))
    for pos, env in ends:
        if not stack:
            return f"Unmatched \\end{{{env}}} at position {pos}"
        start_env, start_pos = stack.pop()
        if start_env != env:
            return f"Mismatched \\end{{{env}}} for \\begin{{{start_env}}} at position {start_pos}"
    if stack:
        env, pos = stack[0]
        return f"Unmatched \\begin{{{env}}} at position {pos}"
    return None

def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'main.tex'
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    # Check braces
    res = check_balance(text, '{', '}', 'brace', 'brace')
    if res:
        print(res)
        return 1
    # Check brackets
    res = check_balance(text, '[', ']', 'bracket', 'bracket')
    if res:
        print(res)
        return 1
    # Check dollar signs (for math mode)
    res = check_balance(text, '$', '$', 'dollar', 'dollar')
    if res:
        print(res)
        return 1
    # Check \begin and \end
    res = check_begin_end(text)
    if res:
        print(res)
        return 1
    print("All basic checks passed")
    return 0

if __name__ == '__main__':
    sys.exit(main())
