from ftplib import FTP
import os


def download_matching_files(ftp, path, prefix, region):
    try:
        file_list = ftp.nlst(path)
        print(file_list)
    except Exception as e:
        print(f"Error: {e}")
        return

    for file_name in file_list:
        if prefix in file_name and file_name.endswith('.zip'):
            print(f"Downloading {file_name}...")
            try:
                local_file_name = os.path.basename(file_name)
                region_directory = f"./downloads/{region}"
                os.makedirs(region_directory, exist_ok=True)
                local_path = os.path.join(region_directory, local_file_name)

                if os.path.exists(local_path):
                    print(f"Skipping {file_name} as it already exists")
                    continue

                with open(local_path, 'ab') as file:
                    ftp.retrbinary('RETR ' + file_name, file.write)
            except Exception as e:
                print(f"Error downloading {file_name}: {e}")

ftp_server = 'ftp.zakupki.gov.ru'
ftp_username = 'free'
ftp_password = 'free'
file_prefix = 'purchasedoc' 

ftp = FTP(ftp_server)
ftp.login(user=ftp_username, passwd=ftp_password)

# Change the name of directories if needed
regions_path = '/fcs_regions'
try:
    ftp.cwd(regions_path)
    regions = ftp.nlst()
except Exception as e:
    print(f"Error: {e}")
    regions = []

for region in regions:
    start_directory = f'/fcs_regions/{region}/purchasedocs' 
    download_matching_files(ftp, start_directory, file_prefix, region)

ftp.quit()
