from setuptools import setup, find_packages


setup(
    name='arh',
    version='1.1.0',
    description='Я здесь за эту улицу стою. Пацаны мне всё, и я всё пацанам. Кто меня знает, тот в курсе.',
    license = 'MIT',
    packages = ['arh'],
    author = 'Andreu S',
    author_email = 'Thesonikpk@gmail.com',
    keywords=['Думайте 144iq'],
    url='https://github.com/ObiVanBanan/arh',
    install_requires=[
        'fpdf==1.7.2',
        'img2pdf==0.5.1',
        'lxml==4.9.3',
        'openpyxl==3.1.2',
        'packaging==23.2',
        'pandas==2.1.2',
        'pdf2image==1.16.3',
        'pdfkit==1.0.0',
        'pikepdf==8.7.1',
        'Pillow==10.0.1',
        'pycryptodomex==3.19.0',
        'pytesseract==0.3.10',
        'PyPDF2==2.12.0',
        'tqdm==4.66.1',
        'pillow==10.0.1',
        ],
    )