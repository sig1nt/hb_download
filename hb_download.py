import requests
import hashlib
import termcolor
import fire
import os


class Book:
    def __init__(self, name, url, hash_alg, ref_hash):
        self.name = name
        self.url = url
        self.hash_alg = hash_alg
        self.ref_hash = ref_hash

    def __repr__(self):
        hash_rep = "{}:{}".format(self.hash_type.name, self.hash)
        return "Book({}, {}, {})".format(self.name, self.url, hash_rep)


def request_hb_api(key):
    url = "https://www.humblebundle.com/api/v1/order/{}".format(key)
    return requests.get(url).json()


def parse_book(book_json):
    name = book_json['machine_name']

    downloads = book_json['downloads'][0]['download_struct']
    pdf = next(filter(lambda x: x['name'] == "PDF", downloads))

    url = pdf['url']['web']

    if 'sha1' in pdf:
        hash_alg = hashlib.sha1
        ref_hash = pdf['sha1']
    else:
        hash_alg = hashlib.md5
        ref_hash = pdf['md5']
    return Book(name, url, hash_alg, ref_hash)


def get_books(hb_obj):
    subproducts = hb_obj['subproducts']
    return map(parse_book, subproducts)


def download_book(book, path):
    resp = requests.get(book.url)

    pdf_hash = book.hash_alg(resp.content).hexdigest()

    if pdf_hash != book.ref_hash:
        print("{} [{}]".format(book.name, termcolor.colored('fail', 'red')))
        return

    print("{} [{}]".format(book.name, termcolor.colored('ok', 'green')))

    filename = "{}/{}.pdf".format(path, book.name)
    with open(filename, 'wb') as f:
        f.write(resp.content)


def hb_download(key, path="books"):
    if not os.path.exists(path):
        os.makedirs(path)

    for book in get_books(request_hb_api(key)):
        download_book(book, path)


if __name__ == '__main__':
    fire.Fire(hb_download)
