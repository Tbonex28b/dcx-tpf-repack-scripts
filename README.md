# DCX and TPF Repack Scripts
These scripts were developed to facilitate the conversion of PC textures for use on the PS4 version of Elden Ring. They automate the extraction, repacking, and management of texture files, streamlining the process of adapting textures between different platforms.

## Prerequisites
### Install Python:
- Ensure Python is installed on your system. You can download it from the [official Python website](https://www.python.org/downloads/).
- Add Python to your system's PATH during the installation process.

### Download Yabber and BinderTool:
- Download Yabber and BinderTool executables from their respective sources (e.g., modding communities, forums).
- Ensure you have the paths to these executables ready for configuration in the scripts.

## Instructions

### Setup:
- Ensure Python is installed on your system.
- Download Yabber and BinderTool and place their executables in convenient locations.
- Adjust the paths to your Yabber input folder, Yabber executable, and BinderTool executable in the scripts.

### Create Input Folder:
- Create a folder named `input_folder` inside your Yabber directory (`C:\\Yabber`).
- Place `.dcx` files inside this folder.

### Using Drag and Drop:
You can use a drag-and-drop method to apply the scripts to individual `.dcx` files or their master folders:

1. **Extract .dcx and .tpf files:**
   - Drag any `.dcx` file or its master folder (the one created from first extracting the `.dcx`) onto `1_extract_dcx_and_tpf.py`.
   - This will extract all `.dcx` and `.tpf` files inside the `input_folder`.

2. **Repack .tpf files:**
   - Drag the master folder of the extracted `-tpf` files onto `2_repack_all_tpf.py`.
   - This will repack all the `-tpf` directories created in the previous step into `.tpf` files.

3. **Repack .dcx files:**
   - Drag the master folder of the extracted `.dcx` files onto `2_repack_all_dx.py`.
   - This will repack all the `.dcx` directories created in the first step into `.dcx` files.

### Using Command Prompt:
- Save each script (`1_extract_dcx_and_tpf.py`, `2_repack_all_tpf.py`, `3_repack_all_dx.py`) in a convenient location.
- To run the scripts via command prompt:
  - Open a command prompt or terminal.
  - Navigate to the directory where the script is saved.
  - Run the script using the command: `python script_name.py`.

## Summary of the Process

1. **Extract .dcx and .tpf files:**
   - Drag any `.dcx` file or its master folder onto `1_extract_dcx_and_tpf.py` to extract all `.dcx` and `.tpf` files in the specified input folder.
   - Alternatively, run `python 1_extract_dcx_and_tpf.py` in the command prompt.

2. **Repack .tpf files:**
   - Drag the master folder of the extracted `-tpf` files onto `2_repack_all_tpf.py` to repack all the `-tpf` directories created in the previous step into `.tpf` files.
   - Alternatively, run `python 2_repack_all_tpf.py` in the command prompt.

3. **Repack .dcx files:**
   - Drag the master folder of the extracted `.dcx` files onto `3_repack_all_dx.py` to repack all the `.dcx` directories created in the first step into `.dcx` files.
   - Alternatively, run `python 3_repack_all_dx.py` in the command prompt.

