import os
import zipfile


def archivation():
    file_zip = zipfile.ZipFile("Cookies_json.zip", "w")

    for folder, subfolder, files in os.walk(r"C:\Users\patap\PycharmProjects\ConvertationTestBot\cookies_json"):
        for file in files:
            if file.endswith('.txt'):
                file_zip.write(os.path.join(folder, file),
                               os.path.relpath(os.path.join(folder, file),
                                               r"C:\Users\patap\PycharmProjects\ConvertationTestBot"),
                               compress_type=zipfile.ZIP_DEFLATED)

    file_zip.close()
    print("Archive created")