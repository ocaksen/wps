
import os
import requests

# WordPress ayarları
wp_url = 'https://dergi.egeyamancigkofte.com/wp-json/wp/v2/posts'
username = 'karataya'
password = 'd#Y2f$6T(Vn*@Q4Qvm9vIt)&'

# Dosya dizini
directory = 'C:/Users/osman.caksen/OneDrive - BilgeAdam/Documents/GitHub/wps/wps/JPE'

# HTML dosyalarını yükleme
for filename in os.listdir(directory):
    if filename.endswith('.html'):
        file_path = os.path.join(directory, filename)

        # HTML içeriğini oku
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # REST API ile yazı oluştur
        response = requests.post(wp_url, json={
            'title': filename,
            'content': f'[load_html file="{filename}"]',
            'status': 'publish',
            'categories': [4]  # ID=4 olan kategoriye atama

        }, auth=(username, password))

        # Sonuçları kontrol et
        if response.status_code == 201:
            print(f'Successfully created post for {filename}')
        else:
            print(f'Failed to create post for {filename}: {response.status_code} - {response.text}')
