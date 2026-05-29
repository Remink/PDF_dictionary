#%%
import pdfplumber
cours1 = r".\cours1.pdf"

pages_par_feuille = 2
dico_mots = dict()

def estValide(mot):
    return True

def add_words(file,pages_par_feuille, offset):

    with pdfplumber.open(file) as pdf:
        pages = pdf.pages

        for i in range(len(pages)):
            mots = pages[i].extract_text().split()
            for mot in mots:
                valide = estValide(mot)
                num_page = (int) (i/pages_par_feuille + offset)
                if( valide and not(mot in dico_mots)):
                    dico_mots[mot] = [num_page]
                elif (valide and not(num_page in dico_mots[mot])):
                    dico_mots[mot].append(num_page)

def main():

    add_words(r".\cours1.pdf",pages_par_feuille,5)
    add_words(r".\cours2.pdf",pages_par_feuille,33)
    add_words(r".\cours3.pdf",pages_par_feuille,63)
    add_words(r".\cours4.pdf",pages_par_feuille,83)
    add_words(r".\cours5.pdf",pages_par_feuille,101)
    add_words(r".\cours6.pdf",pages_par_feuille,155)
            

main()
#%%
print(dico_mots["(upwelling)"])
# %%
