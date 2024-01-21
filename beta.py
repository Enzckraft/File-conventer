import os
from PIL import Image

# Ścieżka do katalogu ze zdjęciami
input_directory = 'E:\\mmeym\\memy'
output_directory = 'E:\\mmeym\\memy2'
processed_files_record = 'E:\\mmeym\\processed_files.txt'
counter_file = 'E:\\mmeym\\counter.txt'

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Odczytanie listy już przetworzonych plików i ich przypisanych numerów
if os.path.exists(processed_files_record):
    with open(processed_files_record, 'r') as file:
        processed_files = {}
        for line in file.read().splitlines():
            parts = line.split(',')
            if len(parts) == 2 and parts[1].isdigit():
                processed_files[parts[0]] = int(parts[1])
else:
    processed_files = {}

# Odczytanie ostatniego numeru zdjęcia (licznika) lub ustalenie go na podstawie przetworzonych plików
if os.path.exists(counter_file):
    with open(counter_file, 'r') as file:
        counter = int(file.read().strip())
else:
    counter = max(processed_files.values(), default=0) + 1

# Rozszerzenia plików, które są uznawane za zdjęcia
image_extensions = ['.jpg', '.jpeg', '.bmp', '.tif', '.tiff', '.png', '.webp']

# Pobranie listy plików w katalogu
files = [f for f in os.listdir(input_directory) if os.path.isfile(os.path.join(input_directory, f))]

for file in files:
    # Sprawdzenie, czy plik ma rozszerzenie zdjęcia
    if any(file.lower().endswith(ext) for ext in image_extensions):
        output_file_name = f'{processed_files.get(file, counter)}.png'
        output_file_path = os.path.join(output_directory, output_file_name)
        
        # Sprawdzenie, czy plik nie został jeszcze przetworzony lub plik wyjściowy nie istnieje
        if file not in processed_files or not os.path.exists(output_file_path):
            try:
                # Wczytanie obrazu
                with Image.open(os.path.join(input_directory, file)) as img:
                    # Zapisanie obrazu w formacie PNG z nową nazwą
                    img.save(output_file_path, 'PNG')
                    
                print(f'Zdjęcie {file} zostało przekonwertowane na {output_file_name}')
                
                # Dodanie nazwy pliku do listy przetworzonych
                if file not in processed_files:
                    processed_files[file] = counter
                    counter += 1

            except Exception as e:
                print(f'Wystąpił problem przy przetwarzaniu pliku {file}: {e}')

# Zapisanie listy przetworzonych plików z ich numerami
with open(processed_files_record, 'w') as file:
    for item, number in processed_files.items():
        file.write(f'{item},{number}\n')

# Zapisanie ostatniego numeru zdjęcia (licznika)
with open(counter_file, 'w') as file:
    file.write(str(counter))

print('Konwersja zakończona.')
