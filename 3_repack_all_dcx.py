import os
import shutil
import subprocess

def repack_dcx_folder(dcx_folder_path, yabber_path, log_file_path):
    try:
        command = [yabber_path, dcx_folder_path]
        print(f'Running repack command: {" ".join(command)}')

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=600)
        
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Repack output for {dcx_folder_path}:\n')
            log_file.write(f'STDOUT:\n{result.stdout}\n')
            log_file.write(f'STDERR:\n{result.stderr}\n')
            log_file.write(f'Return Code: {result.returncode}\n')
            log_file.write('\n' + '='*80 + '\n\n')
        
        if result.returncode != 0:
            print(f'Error repacking {dcx_folder_path}: Return code {result.returncode}')
            return False
        
        print(f'Successfully repacked: {dcx_folder_path}')
        
        shutil.rmtree(dcx_folder_path)
        print(f'Deleted directory: {dcx_folder_path}')
        
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Deleted directory: {dcx_folder_path}\n')
        
        return True

    except subprocess.CalledProcessError as e:
        print(f'Failed to repack: {dcx_folder_path}')
        print(f'Error: {e.stderr}')
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Failed to repack {dcx_folder_path}\n')
            log_file.write(f'Error: {e.stderr}\n\n')
        return False

    except subprocess.TimeoutExpired:
        print(f'Timeout expired for: {dcx_folder_path}')
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Timeout expired for {dcx_folder_path}\n\n')
        return False

def repack_all_dcx(input_folder, yabber_path):
    log_file_path = os.path.join(input_folder, 'extraction_log.txt')

    # Third run (repacking -dcx directories)
    for root, dirs, files in os.walk(input_folder):
        for dir_name in dirs:
            if dir_name.endswith('-dcx'):
                dcx_folder_path = os.path.join(root, dir_name)
                repack_dcx_folder(dcx_folder_path, yabber_path, log_file_path)

# Example paths (edit these according to your setup)
input_folder_path = 'C:\\Path\\To\\Your\\Input_Folder'  # Adjust the path to your input folder
yabber_path = 'C:\\Path\\To\\Yabber.exe'  # Adjust the path to Yabber executable

repack_all_dcx(input_folder_path, yabber_path)
