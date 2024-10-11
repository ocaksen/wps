import requests
from bs4 import BeautifulSoup
import re

# Hedef URL // Hangi siteden alacağını yaz
base_url = 'https://www.thieme-connect.com/products/ejournals/issues/10.1055/s-00029030'

# Headers for requests
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Ana sayfayı alalım
response = requests.get(base_url, headers=headers)

if response.status_code == 200:
    # Sayfanın içeriğini işle
    soup = BeautifulSoup(response.content, 'html.parser')

    # Yılları bul
    years = soup.find_all('a', href=True)
    for year_link in years:
        if '/issues/' in year_link['href']:
            year_url = 'https://www.thieme-connect.com' + year_link['href']
            year = year_link.text.strip()

            # Yıl sayfasına istek yap
            year_response = requests.get(year_url, headers=headers)

            if year_response.status_code == 200:
                year_soup = BeautifulSoup(year_response.content, 'html.parser')

                # Sayılara ait linkleri bul
                issue_links = year_soup.find_all('a', href=True)

                # Her sayı için döngü
                for link in issue_links:
                    if '/issue/' in link['href']:  # Yalnızca "issue" linklerini çek
                        issue_url = 'https://www.thieme-connect.com' + link['href']

                        # Her sayı sayfasına istek yap
                        issue_response = requests.get(issue_url, headers=headers)

                        if issue_response.status_code == 200:
                            issue_soup = BeautifulSoup(issue_response.content, 'html.parser')

                            # Her sayfanın articleListing div'ini bul
                            article_listing = issue_soup.find('div', class_='articleListing')

                            if article_listing:
                                # Geçersiz karakterleri temizlemek için regex kullanıyoruz
                                def sanitize_filename(filename):
                                    # Dosya isimlerinde geçerli olmayan karakterleri boşluk ile değiştir
                                    return re.sub(r'[\/:*?"<>|]', '_', filename)

                                # Dosya ismi için başlık belirle
                                issue_title = sanitize_filename(link.text.strip().replace(":", "-").replace(" ", "_"))

                                # HTML dosyasına yaz
                                with open(f'{year}_{issue_title}.html', 'w', encoding='utf-8') as file:
                                    file.write(article_listing.prettify())

                                print(f"{year}_{issue_title}.html dosyası oluşturuldu.")
                            else:
                                print(f"'articleListing' div'i bulunamadı: {issue_url}")
                        else:
                            print(f"Sayı sayfası alınamadı: {issue_url}")
            else:
                print(f"Yıl sayfası alınamadı: {year_url}")
else:
    print(f"Ana sayfa alınamadı: {base_url}")
