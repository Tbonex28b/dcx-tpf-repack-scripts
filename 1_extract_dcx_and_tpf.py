import os
import subprocess
import shutil

def create_yabber_tpf_xml(output_dir, tpf_filename):
    textures = []
    for file in os.listdir(output_dir):
        if file.endswith('.dds'):
            textures.append(file)
    
    # Construct the XML content with actual file names
    xml_content = '''<?xml version="1.0" encoding="utf-8"?>
<tpf>
  <filename>{}</filename>
  <compression>None</compression>
  <encoding>0x01</encoding>
  <flag2>0x03</flag2>
  <textures>'''.format(tpf_filename)
    
    for i, texture in enumerate(textures):
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

def extract_file(input_path, yabber_path, bindertool_path, log_file_path):
    try:
        if input_path.lower().endswith('.tpf') and 'INTERROOT_ps4' in input_path:
            # Use BinderTool.exe for PS4 .tpf files
            output_dir = input_path + '-tpf'
            os.makedirs(output_dir, exist_ok=True)  # Create output directory for extracted files
            command = [bindertool_path, '--extract-tpf', input_path, output_dir]
        else:
            # Use Yabber for other files
            command = [yabber_path, input_path]

        print(f'Running command: {" ".join(command)}')

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=600)
        
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
            xml_file_path = create_yabber_tpf_xml(output_dir, os.path.basename(input_path))
            
            # No need to copy _yabber-tpf.xml to C:\\Yabber 1.3.1\\input_folder
            # Removing the copy operation

        else:
            print(f'Successfully extracted: {input_path}')
        
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

    # First run (extraction phase)
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.dcx'):
                input_path = os.path.join(root, file)  # Full path to the input .dcx file

                if extract_file(input_path, yabber_path, bindertool_path, log_file_path):
                    for sub_root, sub_dirs, sub_files in os.walk(input_folder):
                        for sub_file in sub_files:
                            if sub_file.endswith('.tpf'):
                                tpf_path = os.path.join(sub_root, sub_file)  # Full path to the .tpf file
                                extract_file(tpf_path, yabber_path, bindertool_path, log_file_path)

# Usage for Phase 1
input_folder_path = 'C:\\Yabber 1.3.1\\input_folder'  # Adjust the path to your input folder
yabber_path = 'C:\\Yabber 1.3.1\\Yabber.exe'  # Adjust the path to Yabber executable
bindertool_path = 'C:\\BinderTool.v0.7.0-pre4\\BinderTool.exe'  # Adjust the path to BinderTool executable

extract_dcx_and_tpf(input_folder_path, yabber_path, bindertool_path)
