import requests
from bs4 import BeautifulSoup
import re


# URL'yi alalım ve sayfanın HTML içeriğini çekelim
def GetAndResultsURL(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return BeautifulSoup(response.content, 'html.parser')
    else:
        print("Sayfa alınamadı:", url)
        return None


# Hedef URL
base_url = 'https://www.thieme-connect.com/products/ejournals/issue/10.1055/s-013-57321'

# Ana sayfayı alalım
html = GetAndResultsURL(base_url)

if html:
    # Başlığı bul
    title = html.find('h1').text.strip() if html.find('h1') else 'Başlık Bulunamadı'

    # Yılları bul
    years = html.find_all('a', href=True)
    for year_link in years:
        if '/issues/' in year_link['href']:
            year_url = 'https://www.thieme-connect.com' + year_link['href']
            year = year_link.text.strip()

            # Yıl sayfasına istek yap
            year_html = GetAndResultsURL(year_url)

            if year_html:
                # Sayılara ait linkleri bul
                issue_links = year_html.find_all('a', href=True)

                # Her sayı için döngü
                for link in issue_links:
                    if '/issue/' in link['href']:  # Yalnızca "issue" linklerini çek
                        issue_url = 'https://www.thieme-connect.com' + link['href']

                        # Sayı sayfasını çekelim
                        issue_html = GetAndResultsURL(issue_url)

                        if issue_html:
                            # Her sayfa için p etiketlerini bul
                            issue_info_list = issue_html.find_all('p')

                            # articleListing div'ini bul
                            article_listing = issue_html.find('div', class_='articleListing')

                            if article_listing:
                                # "listItem scientific" div'lerinden bağlantıları bul ve href'i güncelle
                                for links in article_listing.findAll("div", {"class": "listItem scientific"}):
                                    if links.a and links.a["href"].startswith("/products/"):
                                        links.a["href"] = "https://www.thieme-connect.com" + links.a["href"]

                                # "li" etiketleri içindeki bağlantıları da bul ve href'i güncelle
                                for li in article_listing.findAll("li", {"class": "option"}):
                                    if li.a and li.a["href"].startswith("/products/"):
                                        li.a["href"] = "https://www.thieme-connect.com" + li.a["href"]

                                # relatedArticles içindeki tüm bağlantıları güncelle
                                related_articles = article_listing.find_all('div', class_='relatedArticles')
                                for related in related_articles:
                                    for related_link in related.find_all('a', href=True):
                                        if related_link['href'].startswith('/'):
                                            related_link['href'] = 'https://www.thieme-connect.com' + related_link[
                                                'href']


                                # Geçersiz karakterleri temizlemek için regex kullanıyoruz
                                def sanitize_filename(filename):
                                    return re.sub(r'[\/:*?"<>|]', '_', filename)


                                # Dosya ismi için başlık belirle
                                issue_title = sanitize_filename(link.text.strip().replace(":", "-").replace(" ", "_"))

                                # HTML dosyasına başlık ile birlikte yaz
                                with open(f'{year}_{issue_title}.html', 'w', encoding='utf-8') as file:
                                    # HTML başlığı ve stil bilgileri
                                    file.write(f'<!DOCTYPE html>\n')
                                    file.write(f'<html lang="en">\n')
                                    file.write(f'<head>\n')
                                    file.write(f'    <meta charset="UTF-8">\n')
                                    file.write(
                                        f'    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
                                    file.write(f'    <title>{title}</title>\n')
                                    file.write(
                                        f'    <link rel="stylesheet" href="style.css"> <!-- CSS dosyasını ekliyoruz -->\n')
                                    file.write(f'    <style>\n')
                                    file.write(f'        body {{\n')
                                    file.write(f'            font-family: Arial, sans-serif; /* Yazı tipi */\n')
                                    file.write(f'            margin: 0; /* Varsayılan margin\'i sıfırla */\n')
                                    file.write(f'            padding: 0; /* Varsayılan padding\'i sıfırla */\n')
                                    file.write(f'            text-align: center; /* Metni ortala */\n')
                                    file.write(f'        }}\n')
                                    file.write(f'        .issue-info {{\n')
                                    file.write(f'            margin: 20px 0; /* Üst ve alt kenar boşluğu */\n')
                                    file.write(f'        }}\n')
                                    file.write(f'        .articleListing {{\n')
                                    file.write(f'            text-align: left; /* Makale listesini sola hizala */\n')
                                    file.write(f'            max-width: 800px; /* Maksimum genişlik */\n')
                                    file.write(f'            margin: auto; /* Ortada konumlandır */\n')
                                    file.write(f'        }}\n')
                                    file.write(f'        .articleTitle {{\n')
                                    file.write(f'            display: block;\n')
                                    file.write(f'        }}\n')
                                    file.write(f'    </style>\n')
                                    file.write(f'</head>\n')
                                    file.write(f'<body>\n')

                                    # Başlık ekle
                                    file.write(f'<h1>{title}</h1>\n')

                                    # Her sayı için dinamik olarak issue_info'yu ekleyelim
                                    if issue_info_list:
                                        for info in issue_info_list:
                                            file.write(f'<div class="issue-info">{info.prettify()}</div>\n')

                                    # Article listing'i ekle
                                    file.write(article_listing.prettify())

                                    file.write(f'</body>\n')
                                    file.write(f'</html>\n')

                                print(f"{year}_{issue_title}.html dosyası oluşturuldu.")
                            else:
                                print(f"'articleListing' div'i bulunamadı: {issue_url}")
                    else:
                            print(f"Sayı sayfası alınamadı: {issue_url}")
            else:
                print(f"Yıl sayfası alınamadı: {year_url}")
else:
    print(f"Ana sayfa alınamadı: {base_url}")
