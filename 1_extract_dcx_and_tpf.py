import os
import subprocess

def create_yabber_tpf_xml(output_dir, tpf_filename):
    textures = [file for file in os.listdir(output_dir) if file.endswith('.dds')]
    
    xml_content = '''<?xml version="1.0" encoding="utf-8"?>
<tpf>
  <filename>{}</filename>
  <compression>None</compression>
  <encoding>0x01</encoding>
  <flag2>0x03</flag2>
  <textures>'''.format(tpf_filename)
    
    for texture in textures:
        xml_content += '''
    <texture>
      <name>{}</name>
      <format>0x6B</format>
      <flags1>0x00</flags1>
      <flags2>0x00000000</flags2>
    </texture>'''.format(texture)
    
    xml_content += '''
  </textures>
</tpf>'''
    
    xml_file_path = os.path.join(output_dir, '_yabber-tpf.xml')
    with open(xml_file_path, 'w') as xml_file:
        xml_file.write(xml_content)
    
    print(f'Created _yabber-tpf.xml in {output_dir}')
    return xml_file_path

def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=600)
        return result
    except subprocess.CalledProcessError as e:
        return e
    except subprocess.TimeoutExpired as e:
        return e

def extract_file(input_path, yabber_path, bindertool_path, log_file_path, processed_files, use_bindertool_for_menu_load=False):
    if input_path in processed_files:
        print(f'Skipping already processed file: {input_path}')
        return True
    
    try:
        output_dir = os.path.dirname(input_path)
        
        if input_path.lower().endswith('.tpf.dcx'):
            output_dir = input_path[:-4] + '-dcx'
            os.makedirs(output_dir, exist_ok=True)
            command = [bindertool_path, '--extract-tpf', input_path, output_dir]
        
        elif input_path.lower().endswith('.tpf') and 'INTERROOT_ps4' in input_path:
            output_dir = input_path[:-4] + '-tpf'
            os.makedirs(output_dir, exist_ok=True)
            command = [bindertool_path, '--extract-tpf', input_path, output_dir]
        
        elif input_path.lower().endswith('.tpfbdt'):
            command = [bindertool_path, '--extract-bdt', input_path, output_dir]
        
        elif input_path.lower().endswith('.tpfbhd'):
            command = [yabber_path, input_path]
        
        elif use_bindertool_for_menu_load and 'menu_load' in input_path.lower() and input_path.lower().endswith('.tpf'):
            output_dir = input_path[:-4] + '-menu_load'
            os.makedirs(output_dir, exist_ok=True)
            command = [bindertool_path, '--extract-tpf', input_path, output_dir]
        
        else:
            command = [yabber_path, input_path]
        
        print(f'Running command: {" ".join(command)}')
        result = run_command(command)
        
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Output for {input_path}:\n')
            log_file.write(f'STDOUT:\n{result.stdout}\n')
            log_file.write(f'STDERR:\n{result.stderr}\n')
            log_file.write(f'Return Code: {result.returncode}\n')
            log_file.write('\n' + '='*80 + '\n\n')
        
        if result.returncode != 0:
            print(f'Error extracting {input_path}: Return code {result.returncode}')
            return False
        
        if input_path.lower().endswith('.tpf') and 'INTERROOT_ps4' in input_path:
            print(f'Successfully extracted: {input_path} to {output_dir}')
            create_yabber_tpf_xml(output_dir, os.path.basename(input_path))
        
        elif input_path.lower().endswith('.tpfbdt'):
            print(f'Successfully extracted: {input_path}')
            for sub_root, sub_dirs, sub_files in os.walk(output_dir):
                for sub_file in sub_files:
                    if sub_file.lower().endswith('.tpf') and sub_file.startswith('Menu_Load'):
                        tpf_path = os.path.join(sub_root, sub_file)
                        extract_file(tpf_path, yabber_path, bindertool_path, log_file_path, processed_files, use_bindertool_for_menu_load=True)
        
        elif input_path.lower().endswith('.tpfbhd'):
            print(f'Successfully processed with Yabber: {input_path}')
        
        else:
            print(f'Successfully extracted: {input_path}')
        
        processed_files.add(input_path)
        return True

    except subprocess.CalledProcessError as e:
        print(f'Failed to extract: {input_path}')
        print(f'Error: {e.stderr}')
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Failed to extract {input_path}\n')
            log_file.write(f'Error: {e.stderr}\n\n')
        return False

    except subprocess.TimeoutExpired:
        print(f'Timeout expired for: {input_path}')
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Timeout expired for {input_path}\n\n')
        return False

def extract_dcx_and_tpf(input_folder, yabber_path, bindertool_path):
    log_file_path = os.path.join(input_folder, 'extraction_log.txt')
    processed_files = set()

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            input_path = os.path.join(root, file)
            
            if file.lower().endswith('.dcx'):
                if extract_file(input_path, yabber_path, bindertool_path, log_file_path, processed_files):
                    # Extract associated .tpf files for .dcx
                    for sub_root, sub_dirs, sub_files in os.walk(root):
                        for sub_file in sub_files:
                            if sub_file.lower().endswith('.tpf'):
                                tpf_path = os.path.join(sub_root, sub_file)
                                # Skip extraction if tpfbdt or tpfbhd is present
                                if any(sf.lower().endswith('.tpfbdt') or sf.lower().endswith('.tpfbhd') for sf in sub_files):
                                    continue
                                extract_file(tpf_path, yabber_path, bindertool_path, log_file_path, processed_files)
            
            elif file.lower().endswith('.tpfbdt') or file.lower().endswith('.tpfbhd'):
                extract_file(input_path, yabber_path, bindertool_path, log_file_path, processed_files)
    
    # Perform a separate extraction for MENU_Load items
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            input_path = os.path.join(root, file)
            if 'menu_load' in file.lower() and file.lower().endswith('.tpf'):
                output_dir = input_path[:-4] + '-menu_load'
                os.makedirs(output_dir, exist_ok=True)
                if extract_file(input_path, yabber_path, bindertool_path, log_file_path, processed_files, use_bindertool_for_menu_load=True):
                    create_yabber_tpf_xml(output_dir, os.path.basename(input_path))
                    new_folder_name = os.path.join(root, os.path.basename(output_dir) + '-tpf')
                    os.rename(output_dir, new_folder_name)

# Example paths (edit these according to your setup)
input_folder_path = 'C:\\Yabber 1.3.1\\input_folder'  # Adjust the path to your input folder
yabber_path = 'C:\\Yabber 1.3.1\\Yabber.exe'  # Adjust the path to Yabber executable
bindertool_path = 'C:\\BinderTool.v0.7.0-pre4\\BinderTool.exe'  # Adjust the path to BinderTool executable

extract_dcx_and_tpf(input_folder_path, yabber_path, bindertool_path)

# Pause the script before exiting
input("Press Enter to exit...")
