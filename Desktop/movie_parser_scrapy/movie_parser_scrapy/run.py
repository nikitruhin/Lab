#!/usr/bin/env python3
import subprocess
import sys

def main():
    print("🎬 Парсим фильмы с Википедии")
    
    # Спроси сколько фильмов
    try:
        n = int(input("Сколько фильмов собрать? "))
    except:
        n = 20
        print(f"Использую значение по умолчанию: {n}")
    
    cmd = [
        sys.executable, "-m", "scrapy", "crawl",
        "wikipedia_movies",
        "-a", f"max_movies={n}"  
    ]
    subprocess.run(cmd)

if __name__ == "__main__":
    main()