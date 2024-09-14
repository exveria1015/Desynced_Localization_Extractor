import os
import re
import json
import zipfile
import argparse
from io import TextIOWrapper

def clean_string(s):
    s = re.sub(r'<[^>]+>', '', s)
    s = re.sub(r'%[scdfu]', '', s)
    s = re.sub(r'\w+\.\w+\.\w+', '', s)
    s = re.sub(r'<img id=|"/>|>|">', '', s)
    return s.strip()


def is_valid_string(s):
    cleaned = clean_string(s)
    return cleaned and not cleaned.isdigit() and not all(c in '{}[]().,;:!?' for c in cleaned) and len(cleaned) > 1

def extract_strings_from_content(content):
    strings = set()

    l_func_matches = re.findall(r'L\((.*?)\)', content, re.DOTALL)
    for match in l_func_matches:
        for s in re.findall(r'"([^"]*)"', match):
            if is_valid_string(s):
                strings.add(clean_string(s))
    
    ui_layout_matches = re.findall(r'UI\.AddLayout\((.*?)\)', content, re.DOTALL)
    for match in ui_layout_matches:
        for _, s in re.findall(r'(ok_text|cancel_text)=\'([^\']*)\'', match):
            if is_valid_string(s):
                strings.add(clean_string(s))
    
    table_matches = re.findall(r'\{([^}]*)\}', content, re.DOTALL)
    for match in table_matches:
        for _, s in re.findall(r'(name|text|label|desc|category)\s*=\s*"([^"]*)"', match):
            if is_valid_string(s):
                strings.add(clean_string(s))
    
    for s in re.findall(r'"([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"', content):
        if is_valid_string(s):
            strings.add(clean_string(s))
    
    args_matches = re.findall(r'args\s*=\s*\{([^}]*)\}', content, re.DOTALL)
    for match in args_matches:
        for s in re.findall(r'"([^"]*)"', match):
            if is_valid_string(s):
                strings.add(clean_string(s))
    
    return strings

def get_mod_id(zip_ref):
    try:
        with zip_ref.open('def.json') as def_file:
            def_data = json.load(def_file)
            return def_data.get('id', None)
    except KeyError:
        return None

def extract_strings_from_zip(zip_path):
    strings = {}
    mod_id = None
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        mod_id = get_mod_id(zip_ref) or os.path.basename(zip_path)
        for file_info in zip_ref.infolist():
            if file_info.filename.endswith('.lua'):
                with zip_ref.open(file_info.filename) as file:
                    content = TextIOWrapper(file, encoding='utf-8').read()
                    extracted_strings = extract_strings_from_content(content)
                    if extracted_strings:
                        full_path = f"{mod_id}/{file_info.filename}"
                        strings[full_path] = {s: "" for s in extracted_strings}
    return mod_id, strings

def load_jsonc(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove comments
    content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    # Handle trailing commas
    content = re.sub(r',\s*}', '}', content)
    content = re.sub(r',\s*]', ']', content)
    # Parse JSON
    return json.loads(content)

def write_jsonc(all_strings, output_file, base_lang_entries):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("{\n")
        written_keys = set()
        for mod_id, strings in all_strings.items():
            mod_entries = []
            for file_path, file_strings in strings.items():
                file_entries = []
                for key in file_strings:
                    if isinstance(key, tuple):
                        cleaned_key = key[1]
                    else:
                        cleaned_key = key.split(',')[-1].strip().strip("'")
                    if cleaned_key and cleaned_key not in written_keys and cleaned_key not in base_lang_entries:
                        file_entries.append(f'\t"{cleaned_key}": "",\n')
                        written_keys.add(cleaned_key)
                if file_entries:
                    mod_entries.append(f'\n\t// FILE: {file_path}\n\n')
                    mod_entries.extend(file_entries)
                    mod_entries.append('\n')
            if mod_entries:
                f.write(f'\n\t// {mod_id}\n')
                f.writelines(mod_entries)
        f.write("}\n")

def main():
    parser = argparse.ArgumentParser(description='Extract strings from MOD ZIP file(s) and create language file')
    parser.add_argument('zip_files', nargs='+', help='Path(s) to the MOD ZIP file(s)')
    parser.add_argument('--base_lang', help='Path to the base language JSON file')
    parser.add_argument('--lang', default='en', help='Output language code (default: en)')
    args = parser.parse_args()

    output_file = f"{args.lang}.jsonc"
    all_strings = {}

    base_lang_entries = set()
    if args.base_lang:
        base_lang_data = load_jsonc(args.base_lang)
        base_lang_entries = set(base_lang_data.keys())

    for zip_file in args.zip_files:
        mod_id, strings = extract_strings_from_zip(zip_file)
        all_strings[mod_id] = strings

    write_jsonc(all_strings, output_file, base_lang_entries)

    print(f"Translation file created: {output_file}")

if __name__ == "__main__":
    main()