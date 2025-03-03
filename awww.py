import textwrap
import requests
from bs4 import BeautifulSoup
from googlesearch import search

def formatowanie(description, max_width=80):
    if description:
        return "\n".join(textwrap.wrap(description, width=max_width))
    return "Brak informacji"

def pozyskiwanie_opisu(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        description = soup.find('p') # Pobieram pierwszy losowy paragraf na stronie
        min_długość = 200 # minimalna długość opisu ustawiona na 200
        if description and len(description.text.strip()) > min_długość:
            return description.text.strip()
        else:
            return ""
    except Exception as e:
        return f"Nie udało się pobrać ze strony, błąd {e}"

def tworzenie_strony():
    try:
        adres = 'https://www.tiobe.com/tiobe-index/'
        response = requests.get(adres)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Znalezienie tabeli z rankingiem
        table = soup.find('tbody')

        info = []
        # Pobranie pierwszych 20 języków
        jezyki = table.find_all('tr')[:20]

        for jezyk in jezyki:
            dane = jezyk.find_all('td')

            rank = dane[0].text.strip()
            language = dane[4].text.strip()
            percentage = dane[5].text.strip()
            img_tag = dane[3].find('img')
            img_url = "https://www.tiobe.com" + img_tag['src']
            temp = [rank, language, percentage, img_url]
            info.append(temp)

        strona_główna = "strona_glowna.md"
        opis = soup.find_all('p')
        with open(strona_główna, "w", encoding="utf-8") as f:
            f.write("# TIOBE Index\n")
            f.write(formatowanie(opis[4].text))
            f.write("\n\n[Click here to find out more.](podstrona.md)\n")
            
        max_długość = 5 # tworzę podstrony dla top 5 języków, można to dowolnie zmieniać
        ranking = f"# Top 20 programming languages \n ### Learn more about top {max_długość} by clicking on them.\n"
        top = 0
        for lan in info:
            if top < max_długość:
                ranking += f"### {lan[0]}. [{lan[1]}]({lan[1]}.md)\n\n"
                top += 1
                strona = f"{lan[1]}.md"
                with open(strona, "w", encoding="utf-8") as f:
                    f.write(f"## ![Opis obrazka]({lan[3]}) Learn more about {lan[1]}\n\n")
                    query = f"{lan[1]} programming description"
                    results = list(search(query))
                    for i, url in enumerate(results):
                        if pozyskiwanie_opisu(url) == "":
                            continue
                        else:
                            f.write(formatowanie(pozyskiwanie_opisu(url)))
                            f.write("\n\n")
            else:
                ranking += f"### {lan[0]}. {lan[1]} \n"
            ranking += f"#### Logo:  ![Opis obrazka]({lan[3]})\n\n"
            ranking += f"#### Popularity: {lan[2]}\n"

        podstrona = "podstrona.md"
        with open(podstrona, "w", encoding="utf-8") as f:
            f.write(ranking)
    except Exception as e:
        print(f"Nie udało się, błąd {e}")

def main():
    tworzenie_strony()

if __name__ == "__main__":
    main()
