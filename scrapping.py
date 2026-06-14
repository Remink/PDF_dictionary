
import pdfplumber
import re
import locale 
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer

pages_par_feuille = 2
dico_mots = dict()
max_apparitions = 50

stop_words = [w.strip() for w in open("stop_words.txt", "r").readlines()]
lemmatizer = FrenchLefffLemmatizer()

def nettoie(mot):
    mot = mot.lower().strip()

    if mot[0] == "-":
        mot = mot[1:]
    if mot[-1] == "-":
        mot = mot[:-1]

    bases = lemmatizer.lemmatize(mot, "all")
    if len(bases) > 0:
        mot = bases[0][0]

    return mot

def estValide(mot):
    num_count = sum(c.isdigit() for c in mot)
    alpha_count = sum(c.isalpha() for c in mot)

    len_ok = len(mot) >= 3 and len(mot) < 15
    ok_number = len(mot) >= 4 and len(mot) < 5 and num_count == len(mot)
    ok_word = alpha_count >= 2 and num_count <= 3

    return len_ok and (ok_number or ok_word)

def handle_word(dico_mots, mot, num_page):
    if len(mot) < 2: return
    mot2 = nettoie(mot)
    valide = estValide(mot2) and mot2 not in stop_words

    if valide:
        if mot2 not in dico_mots:
            dico_mots[mot2] = [num_page]
        elif num_page not in dico_mots[mot2]:
            dico_mots[mot2].append(num_page)

def ajout_mots(file,pages_par_feuille, offset):
    with pdfplumber.open(file) as pdf:
        pages = pdf.pages

        for i in range(len(pages)):
            text = pages[i].extract_text()
            mots = re.findall(r"[-'a-zA-ZÀ-ÖØ-öø-ÿ0-9α-ωΑ-Ω]+", text)
            num_page = (int) (i/pages_par_feuille + offset)

            for mot in mots:
                subwords = mot.split("-")

                for word in subwords:
                    handle_word(dico_mots, word, num_page)

                if len(subwords) > 1:
                    handle_word(dico_mots, mot, num_page)



def main():
    locale.setlocale(locale.LC_ALL, "fr_FR.utf8")

    ajout_mots(r"cours1.pdf",pages_par_feuille,5)
    ajout_mots(r"cours2.pdf",pages_par_feuille,33)
    ajout_mots(r"cours3.pdf",pages_par_feuille,63)
    ajout_mots(r"cours4.pdf",pages_par_feuille,83)
    ajout_mots(r"cours5.pdf",pages_par_feuille,101)
    ajout_mots(r"cours6.pdf",pages_par_feuille,155)

    res = open("out.typ", "w")

    res.write("#set text(size: 9pt, top-edge: 1pt)\n#set page(margin: 2cm)\n#set align(right)\n#columns(5, gutter: 4pt)[\n")

    for word in sorted(dico_mots.keys(), key=locale.strxfrm):
        if len(dico_mots[word]) > max_apparitions:
            continue

        pages = ", ".join(map(str, dico_mots[word]))
        res.write(f"{word} #box(stroke: (paint: black, thickness: 0.25pt, dash: \"dotted\"), width: 1fr) {pages}\\\n")

    res.write("]")

    print(dico_mots["bilan"])

main()
