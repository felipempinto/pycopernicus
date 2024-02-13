import requests
import os

def download(outpath,product,access_token):

    url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({product})/$value"
    # url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products(a5ab498a-7b2f-4043-ae2a-f95f457e7b3b)/$value"

    headers = {"Authorization": f"Bearer {access_token}"}

    session = requests.Session()
    session.headers.update(headers)
    response = session.get(url, headers=headers, stream=True)
    output = os.path.join(outpath,f"{product}.zip")
    with open(output, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)