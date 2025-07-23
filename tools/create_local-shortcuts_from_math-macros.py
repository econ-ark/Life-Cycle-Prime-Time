import yaml

def generate_files(mapping_file):
    """
    Parses the new mapping-macros.yml file and generates econark-shortcuts.yml
    and econark-shortcuts.sty.
    """
    try:
        with open(mapping_file, 'r') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: '{mapping_file}' not found. Please run the create_macro_map.py script first.")
        return

    macros = data.get('math', {})
    if not macros:
        print("No macros found in the mapping file.")
        return
        
    # --- Generate local-shortcuts.yml (direct copy) ---
    yaml_file = 'tools/local-shortcuts.yml'
    with open(yaml_file, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)
    print(f"Successfully created '{yaml_file}'")

    # --- Generate local-shortcuts.sty ---
    sty_content = "\\ProvidesPackage{local-shortcuts}\n\n"
    for name, definition in macros.items():
        # Ensure macro name doesn't include the backslash for the command
        command_name = name.strip()
        sty_content += f"\\newcommand{{{command_name}}}{{{definition}}}\n"

    sty_file = 'tools/local-shortcuts.sty'
    with open(sty_file, 'w') as f:
        f.write(sty_content)
    print(f"Successfully created '{sty_file}'")


def main():
    """Main function to run the script."""
    mapping_file = 'tools/math-macros.yml'
    generate_files(mapping_file)

if __name__ == "__main__":
    main() 