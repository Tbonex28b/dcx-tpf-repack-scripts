import os
import shutil
import subprocess

def repack_dcx_folder(folder_path, yabber_path, log_file_path):
    try:
        command = [yabber_path, folder_path]
        print(f'Running repack command: {" ".join(command)}')

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=600)
        
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Repack output for {folder_path}:\n')
            log_file.write(f'STDOUT:\n{result.stdout}\n')
            log_file.write(f'STDERR:\n{result.stderr}\n')
            log_file.write(f'Return Code: {result.returncode}\n')
            log_file.write('\n' + '='*80 + '\n\n')
        
        if result.returncode != 0:
            print(f'Error repacking {folder_path}: Return code {result.returncode}')
            return False
        
        print(f'Successfully repacked: {folder_path}')
        
        shutil.rmtree(folder_path)
        print(f'Deleted directory: {folder_path}')
        
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Deleted directory: {folder_path}\n')

        # Check and delete the corresponding _Solo directory
        solo_dir = folder_path.replace('-tpfbhd', '_Solo')
        if os.path.exists(solo_dir):
            shutil.rmtree(solo_dir)
            print(f'Deleted corresponding _Solo directory: {solo_dir}')
            with open(log_file_path, 'a') as log_file:
                log_file.write(f'Deleted corresponding _Solo directory: {solo_dir}\n')
        
        return True

    except subprocess.CalledProcessError as e:
        print(f'Failed to repack: {folder_path}')
        print(f'Error: {e.stderr}')
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Failed to repack {folder_path}\n')
            log_file.write(f'Error: {e.stderr}\n\n')
        return False

    except subprocess.TimeoutExpired:
        print(f'Timeout expired for: {folder_path}')
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Timeout expired for {folder_path}\n\n')
        return False

def repack_all_dcx_and_tpfbhd(input_folder, yabber_path):
    log_file_path = os.path.join(input_folder, 'extraction_log.txt')

    # Repacking -dcx and -tpfbhd directories
    for root, dirs, files in os.walk(input_folder):
        for dir in dirs:
            if dir.endswith('-dcx') or dir.endswith('-tpfbhd'):
                folder_path = os.path.join(root, dir)
                repack_dcx_folder(folder_path, yabber_path, log_file_path)

    # Check and delete any _Solo directories
    for root, dirs, files in os.walk(input_folder):
        for dir in dirs:
            if dir.endswith('_Solo'):
                solo_folder_path = os.path.join(root, dir)
                shutil.rmtree(solo_folder_path)
                print(f'Deleted _Solo directory: {solo_folder_path}')
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f'Deleted _Solo directory: {solo_folder_path}\n')

# Usage for Phase 3
input_folder_path = 'C:\\Yabber 1.3.1\\input_folder'  # Adjust the path to your input folder
yabber_path = 'C:\\Yabber 1.3.1\\Yabber.exe'  # Adjust the path to Yabber executable

repack_all_dcx_and_tpfbhd(input_folder_path, yabber_path)

# Pause the script before exiting
input("Press Enter to exit...")
