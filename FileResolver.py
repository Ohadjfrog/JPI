import sys

import requests
import re

class FileResolver:
    def __init__(self, appVersion, url):
        self.appVersion = appVersion
        self.url = url

    def get_filename_from_cd(cd):
        """
        Get filename from content-disposition
        """
        if not cd:
            return None
        fname = re.findall('filename=(.+)', cd)
        if len(fname) == 0:
            return None
        return fname[0]

print('Beginning Artifactory file download with requests')
ArtifactoryVersion = input("Please enter the Artifactory version:\n")

url = f'https://jfrog.bintray.com/artifactory-pro/org/artifactory/pro/jfrog-artifactory-pro/{ArtifactoryVersion}/jfrog-artifactory-pro-{ArtifactoryVersion}.zip'
response = requests.get(url, stream=True)
filename = get_filename_from_cd(response.headers.get('content-disposition'))[1:-1]
#filename = filename[1:-1]
print(filename)
target_path = f'/Users/ohadl/Downloads/{filename}'
with open(target_path, 'wb') as f:
    print('Downloading %s' % target_path)
    total_length = response.headers.get('content-length')
    if total_length is None:  # no content length header
        f.write(response.content)
    else:
        dl = 0
        total_length = int(total_length)
        for data in response.iter_content(chunk_size=4096):
            dl += len(data)
            f.write(data)
            done = int(50 * dl / total_length)
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
            sys.stdout.flush()
# Retrieve HTTP meta-data
print("")
print(response.status_code)
print(response.headers['content-type'])
print(response.encoding)