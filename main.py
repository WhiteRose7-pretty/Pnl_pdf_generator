from PyPDF2 import PdfFileReader, PdfFileWriter
from tqdm import tqdm
import urllib.request
import urllib.parse
import hashlib
import os
import random
import string

pdf_api_key = 'e123a9'

pnl_pdf_origin = "pnl_origin.pdf"
pnl_pdf_origin_update = "pnl.pdf"
pnl_function = "read_file"
pnl_server = "http://77.68.28.47/"


def get_random_name(num):
    letters = string.ascii_lowercase
    random_name = ''.join(random.choice(letters) for i in range(num))
    random_name += '.pdf'
    return random_name


def generate_url(customer_key, secret_phrase, options):
    api_url = 'https://pdfapi.screenshotmachine.com/?key=' + customer_key
    if secret_phrase:
        api_url = api_url + '&hash=' + hashlib.md5((options.get('url') + secret_phrase).encode('utf-8')).hexdigest()
    api_url = api_url + '&' + urllib.parse.urlencode(options)
    return api_url


def remove_last_page(pdf_file, out_file):
    print('Converting pdf...')
    with open(pdf_file, 'rb') as f:
        p = PdfFileReader(f)
        number_of_pages = p.getNumPages()
        writer = PdfFileWriter()
        for i in tqdm(range(number_of_pages - 1)):
            page = p.getPage(i)
            writer.addPage(page)

        with open(out_file, 'wb') as f1:
            writer.write(f1)


def pdf_from_api(token, file_name):
    try:
        print('generating pdf...')
        secret_phrase = ''
        paper_options = {
            'url': 'http://77.68.7.117/newsletter/pnl/report/?token=' + token + '&path=' + file_name,
            'paper': 'A4',
            'orientation': 'landscape',
            'media': 'screen',
            'bg': 'bg',
            'delay': '2000',
            'scale': '83',
        }
        pdf_api_url = generate_url(pdf_api_key, secret_phrase, paper_options)
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', '-')]
        urllib.request.install_opener(opener)
        output_pdf = get_random_name(10)
        urllib.request.urlretrieve(pdf_api_url, output_pdf)
    except Exception as e:
        output_pdf = False
        results = {'error': str(e)}
        print(results)

    return output_pdf


def generate_pdf(path, token):
    output_pdf_origin = pdf_from_api(token, path)
    if output_pdf_origin:
        pnl_final = path + '.pdf'
        remove_last_page(output_pdf_origin, pnl_final)
        os.remove(output_pdf_origin)


path = 'reports/report_5swp.json'
token = 'eyJpc3MiOiJodHRwczovL2V4YW1wbGUuYXV0aDA'


generate_pdf(path, token)
