import os
import shutil
import subprocess

def remove_bak_files(input_folder, log_file_path):
    """Remove .bak files in the specified directory and its subdirectories."""
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.bak'):
                bak_file_path = os.path.join(root, file)
                try:
                    os.remove(bak_file_path)
                    print(f'Deleted backup file: {bak_file_path}')
                    with open(log_file_path, 'a') as log_file:
                        log_file.write(f'Deleted backup file: {bak_file_path}\n')
                except OSError as e:
                    print(f'Error deleting backup file {bak_file_path}: {e}')
                    with open(log_file_path, 'a') as log_file:
                        log_file.write(f'Error deleting backup file {bak_file_path}: {e}\n')

def repack_tpf_folder(tpf_folder_path, yabber_path, log_file_path):
    try:
        command = [yabber_path, tpf_folder_path]
        print(f'Running repack command: {" ".join(command)}')

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=600)
        
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Repack output for {tpf_folder_path}:\n')
            log_file.write(f'STDOUT:\n{result.stdout}\n')
            log_file.write(f'STDERR:\n{result.stderr}\n')
            log_file.write(f'Return Code: {result.returncode}\n')
            log_file.write('\n' + '='*80 + '\n\n')
        
        if result.returncode != 0:
            print(f'Error repacking {tpf_folder_path}: Return code {result.returncode}')
            return False
        
        print(f'Successfully repacked: {tpf_folder_path}')
        
        # Remove .bak files after successful repack
        remove_bak_files(tpf_folder_path, log_file_path)
        
        # Delete the repacked directory
        try:
            shutil.rmtree(tpf_folder_path)
            print(f'Deleted directory: {tpf_folder_path}')
            
            with open(log_file_path, 'a') as log_file:
                log_file.write(f'Deleted directory: {tpf_folder_path}\n')
            
            return True
        except OSError as e:
            print(f'Error deleting directory {tpf_folder_path}: {e}')
            with open(log_file_path, 'a') as log_file:
                log_file.write(f'Error deleting directory {tpf_folder_path}: {e}\n')
            return False

    except subprocess.CalledProcessError as e:
        print(f'Failed to repack: {tpf_folder_path}')
        print(f'Error: {e.stderr}')
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Failed to repack {tpf_folder_path}\n')
            log_file.write(f'Error: {e.stderr}\n\n')
        return False

    except subprocess.TimeoutExpired:
        print(f'Timeout expired for: {tpf_folder_path}')
        with open(log_file_path, 'a') as log_file:
            log_file.write(f'Timeout expired for {tpf_folder_path}\n\n')
        return False

def repack_all_tpf(input_folder, yabber_path):
    log_file_path = os.path.join(input_folder, 'extraction_log.txt')

    # Second run (repacking -tpf directories)
    for root, dirs, files in os.walk(input_folder):
        for dir_name in dirs:
            if dir_name.endswith('-tpf'):
                tpf_folder_path = os.path.join(root, dir_name)
                if repack_tpf_folder(tpf_folder_path, yabber_path, log_file_path):
                    # Optionally, perform additional cleanup if needed
                    pass

# Usage for Phase 2
input_folder_path = 'C:\\Yabber 1.3.1\\input_folder'  # Adjust the path to your input folder
yabber_path = 'C:\\Yabber 1.3.1\\Yabber.exe'  # Adjust the path to Yabber executable

repack_all_tpf(input_folder_path, yabber_path)

# Pause the script before exiting
# input("Press Enter to exit...")
