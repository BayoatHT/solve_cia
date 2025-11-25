#!/usr/bin/env python3
"""
Script to add return_original parameter to all parser functions.
This version properly handles indentation.
"""
import os
import re
import glob
import ast

def get_indentation(line):
    """Get the indentation of a line."""
    return len(line) - len(line.lstrip())

def add_return_original_to_file(filepath):
    """Add return_original parameter to parser functions in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    content = ''.join(lines)

    # Check if return_original is already in the file
    if 'return_original' in content:
        print(f"  SKIP (already has return_original): {filepath}")
        return False

    modified = False
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Check for function definition
        func_match = re.match(r'^(\s*)def\s+(parse_\w+)\s*\(', line)
        if func_match:
            indent = func_match.group(1)
            func_name = func_match.group(2)

            # Collect the full function signature (may span multiple lines)
            func_lines = [line]
            paren_count = line.count('(') - line.count(')')
            j = i + 1
            while paren_count > 0 and j < len(lines):
                func_lines.append(lines[j])
                paren_count += lines[j].count('(') - lines[j].count(')')
                j += 1

            func_sig = ''.join(func_lines)

            # Add return_original parameter before the closing paren
            # Find the last ) before the :
            new_func_sig = re.sub(
                r'\)\s*((?:->\s*\w+(?:\[.*?\])?\s*)?:)',
                r', return_original: bool = False)\1',
                func_sig
            )

            if new_func_sig != func_sig:
                # Add the modified function signature
                new_lines.append(new_func_sig)
                modified = True
                i = j

                # Now find where to add the return_original check
                # First, skip docstring if present
                body_indent = indent + '    '
                docstring_end = i

                # Check for docstring
                while i < len(lines):
                    stripped = lines[i].strip()
                    if stripped.startswith('"""') or stripped.startswith("'''"):
                        # Docstring found
                        quote = stripped[:3]
                        if stripped.count(quote) >= 2 and len(stripped) > 6:
                            # Single line docstring
                            new_lines.append(lines[i])
                            i += 1
                            break
                        else:
                            # Multi-line docstring
                            new_lines.append(lines[i])
                            i += 1
                            while i < len(lines) and quote not in lines[i]:
                                new_lines.append(lines[i])
                                i += 1
                            if i < len(lines):
                                new_lines.append(lines[i])
                                i += 1
                            break
                    elif stripped == '' or stripped.startswith('#'):
                        new_lines.append(lines[i])
                        i += 1
                    else:
                        break

                # Now we're past the docstring, look for the data parameter
                # For OLD style: the first parameter is the data
                # For NEW style: data is loaded via load_country_data

                # Find the data parameter name from the function signature
                old_style_match = re.search(r'def\s+parse_\w+\s*\(\s*(\w+)', func_sig)
                data_param = old_style_match.group(1) if old_style_match else None

                # Check if this is OLD style (data param) or NEW style (iso3Code first)
                is_new_style = data_param and data_param.lower() == 'iso3code'

                if is_new_style:
                    # NEW style - need to find where section data is extracted
                    # Look for pattern: xxx_data = section.get('...', {})
                    inserted = False
                    while i < len(lines) and not inserted:
                        current_line = lines[i]
                        # Look for the section data extraction
                        section_get_match = re.match(
                            r'^(\s*)(\w+)\s*=\s*\w+_section\.get\([\'"][^\'"]+[\'"]\s*,\s*\{\}\)',
                            current_line
                        )
                        if section_get_match:
                            data_var = section_get_match.group(2)
                            line_indent = section_get_match.group(1)
                            new_lines.append(current_line)
                            # Add the return_original check after this line
                            new_lines.append('\n')
                            new_lines.append(f'{line_indent}if return_original:\n')
                            new_lines.append(f'{line_indent}    return {data_var}\n')
                            new_lines.append('\n')
                            i += 1
                            inserted = True
                        else:
                            new_lines.append(current_line)
                            i += 1

                    # If not inserted yet, try a more lenient pattern
                    if not inserted:
                        # Continue without inserting (will be handled later)
                        pass
                else:
                    # OLD style - add return_original check at the start of function body
                    # Insert right after docstring
                    new_lines.append(f'{body_indent}if return_original:\n')
                    new_lines.append(f'{body_indent}    return {data_param}\n')
                    new_lines.append('\n')

                continue

        new_lines.append(line)
        i += 1

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

        # Verify syntax
        try:
            with open(filepath, 'r') as f:
                compile(f.read(), filepath, 'exec')
            print(f"  MODIFIED: {filepath}")
            return True
        except SyntaxError as e:
            print(f"  ERROR (syntax): {filepath} - {e}")
            return False
    else:
        print(f"  NO CHANGE: {filepath}")
        return False


def main():
    """Process all parser files."""
    categories = [
        'c_02_geography',
        'c_03_society',
        'c_04_environment',
        'c_05_government',
        'c_06_economy',
        'c_07_energy',
        'c_08_communications',
        'c_09_transportation',
        'c_10_military',
        'c_11_space',
        'c_12_terrorism',
        'c_13_issues'
    ]

    base_path = '/home/user/solve_cia/proj_004_cia'
    total_modified = 0
    total_files = 0
    errors = []

    for category in categories:
        pattern = f'{base_path}/{category}/helper/utils/parse_*.py'
        files = glob.glob(pattern)
        print(f"\n=== {category} ({len(files)} files) ===")

        for filepath in sorted(files):
            total_files += 1
            try:
                if add_return_original_to_file(filepath):
                    total_modified += 1
            except Exception as e:
                errors.append(f"{filepath}: {e}")
                print(f"  ERROR: {filepath} - {e}")

    print(f"\n{'='*60}")
    print(f"Total files processed: {total_files}")
    print(f"Total files modified: {total_modified}")
    if errors:
        print(f"Errors: {len(errors)}")


if __name__ == '__main__':
    main()
