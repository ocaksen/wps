import os
import re

# Değiştirmek istediğiniz klasörün yolu
folder_path = r'C:\Users\osman.caksen\OneDrive - BilgeAdam\Desktop\JPN'

# Klasördeki tüm .html dosyalarını listele
for filename in os.listdir(folder_path):
    if filename.endswith('.html'):
        file_path = os.path.join(folder_path, filename)

        # Dosyayı oku
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Issue ve Volume bilgilerini çıkar
            issue_match = re.search(r'Issue\s+(\d+)', content)
            volume_match = re.search(r'Volume\s+(\d+)', content)

            if issue_match and volume_match:
                issue_number = issue_match.group(1)
                volume_number = volume_match.group(1)

                # Yeni dosya adını oluştur
                new_filename = f'JPN-V{volume_number}N{issue_number}.html'
                new_file_path = os.path.join(folder_path, new_filename)

                # Dosya adını değiştir
                os.rename(file_path, new_file_path)
                print(f'Dosya adı değiştirildi: {filename} -> {new_filename}')
            else:
                print(f'Issue veya Volume bilgisi bulunamadı: {filename}')
