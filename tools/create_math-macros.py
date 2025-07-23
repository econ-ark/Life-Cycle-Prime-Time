import re
import yaml
import os

def parse_myst_macros(file_path):
    """Parses a myst.yml file and extracts math macros."""
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return data.get('project', {}).get('math', {})
    except (FileNotFoundError, yaml.YAMLError):
        return {}

def parse_latex_macros(file_path):
    """Parses a .tex file and extracts \\newcommand and \\renewcommand definitions."""
    macros = {}
    pattern = re.compile(r'\\(?:newcommand|renewcommand)\s*\{\s*\\([a-zA-Z]+)\s*\}\s*\{(.*?)\}')
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except FileNotFoundError:
        return {}
    
    content_no_comments = re.sub(r'%.*$', '', content, flags=re.MULTILINE)
    matches = pattern.findall(content_no_comments)
    for match in matches:
        macros[f"\\{match[0]}"] = match[1].strip()
    return macros

def find_tex_files():
    """Finds all .tex files in the current directory and subdirectories."""
    tex_files = []
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.tex'):
                tex_files.append(os.path.join(root, file))
    return tex_files

def main():
    """Main function to generate the macro mapping file."""
    myst_file = '../myst.yml'
    
    # Use myst macros as the base
    final_macros = parse_myst_macros(myst_file)
    if not final_macros:
        final_macros = {}

    # Find and parse all latex files
    tex_files = find_tex_files()
    
    print("Checking for conflicts and merging macros...")
    for tex_file in tex_files:
        latex_macros = parse_latex_macros(tex_file)
        for name, definition in latex_macros.items():
            if name in final_macros:
                # Conflict: macro exists in myst.yml
                if final_macros[name] != definition:
                    print(f"Conflict: Macro '{name}' in '{tex_file}' has a different definition than in '{myst_file}'. Using definition from '{myst_file}'.")
            else:
                # No conflict, add it
                final_macros[name] = definition
    
    # Prepare data for YAML output in the desired format
    output_data = {'math': final_macros}

    # Write to YAML file
    output_file = 'math-macros.yml'
    with open(output_file, 'w') as f:
        yaml.dump(output_data, f, default_flow_style=False, sort_keys=False, indent=2)

    print(f"\nSuccessfully created '{output_file}' with the new simplified macro map.")

if __name__ == "__main__":
    main() 