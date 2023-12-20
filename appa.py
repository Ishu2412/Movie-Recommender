import requests

url = "https://drive.google.com/file/d/1MJRf2iQeIcND3xbSWkslQGh_hmx1AyIF/view?usp=sharing"
response = requests.get(url)

with open("sparse_matrix.npz", "wb") as file:
    file.write(response.content)
