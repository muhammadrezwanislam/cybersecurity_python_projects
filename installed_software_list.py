import winreg
import pandas as pd

# Create an EMPTY LIST to store all programs
all_programs = []

def listofinstalledsoftware(key_handle, hive_name, reg_path):
    for i in range(0, winreg.QueryInfoKey(key_handle)[0]):
        subkey_name = winreg.EnumKey(key_handle, i)
        
        # Create a NEW dictionary for THIS program
        program_info = {
            'Name': None,
            'Version': None,
            'Publisher': None,
            'InstallDate': None,      # Add this
            'InstallLocation': None,  # Add this
            'EstimatedSize': None,    # Add this
            'Hive': hive_name,
            'Path': reg_path
        }
        
        try:
            subkey_handle = winreg.OpenKey(key_handle, subkey_name)
            
            # Try to read DisplayName
            try:
                display_name = winreg.QueryValueEx(subkey_handle, "DisplayName")
                program_info['Name'] = display_name[0]  # Remember: it's a tuple!
            except:
                #pass
                program_info['Name'] = subkey_name
            
            # Try to read DisplayVersion
            try:
                display_version = winreg.QueryValueEx(subkey_handle, "DisplayVersion")
                program_info['Version'] = display_version[0]  # Remember: it's a tuple!
            except:
                pass
                
            # Try to read Publisher
            try:
                display_publisher = winreg.QueryValueEx(subkey_handle, "Publisher")
                program_info['Publisher'] = display_publisher[0]  # Remember: it's a tuple!
            except:
                pass
            
            try:
                install_date = winreg.QueryValueEx(subkey_handle, "InstallDate")
                program_info['InstallDate'] = install_date[0]
            except:
                pass
            
            try:
                install_location = winreg.QueryValueEx(subkey_handle, "InstallLocation")
                program_info['InstallLocation'] = install_location[0]
            except:
                pass
            
            try:
                Estimated_size = winreg.QueryValueEx(subkey_handle, "EstimatedSize")
                program_info['EstimatedSize'] = Estimated_size[0]/1024
            except:
                pass
            
            
            
            # Add this program to the list
            all_programs.append(program_info)
            
        except FileNotFoundError:
            pass

# List of registry locations
locations = [
    (winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", "HKLM"),
    (winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\WOW6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall", "HKLM_WOW64"),
    (winreg.HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall", "HKCU")
]

# Loop through locations
for hive, path, hive_name in locations:
    try:
        key_handle = winreg.OpenKey(hive, path)
        listofinstalledsoftware(key_handle, hive_name, path)
    except FileNotFoundError:
        pass

# NOW create the DataFrame from all collected data
df = pd.DataFrame(all_programs)
print(df)