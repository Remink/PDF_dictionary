#%%
import pdfplumber
import re

pages_par_feuille = 2
dico_mots = dict()

def estValide(mot):
    return True

def ajout_mots(file,pages_par_feuille, offset):

    with pdfplumber.open(file) as pdf:
        pages = pdf.pages

        for i in range(len(pages)):
            text =pages[i].extract_text()
            mots = words = re.findall(r"[-'a-zA-ZÀ-ÖØ-öø-ÿ]+", text)
            for mot in mots:
                mot2 = mot
                valide = estValide(mot2)
                num_page = (int) (i/pages_par_feuille + offset)
                if( valide and not(mot2 in dico_mots)):
                    dico_mots[mot2] = [num_page]
                elif (valide and not(num_page in dico_mots[mot2])):
                    dico_mots[mot2].append(num_page)

def main():

    ajout_mots(r".\cours1.pdf",pages_par_feuille,5)
    ajout_mots(r".\cours2.pdf",pages_par_feuille,33)
    ajout_mots(r".\cours3.pdf",pages_par_feuille,63)
    ajout_mots(r".\cours4.pdf",pages_par_feuille,83)
    ajout_mots(r".\cours5.pdf",pages_par_feuille,101)
    ajout_mots(r".\cours6.pdf",pages_par_feuille,155)
            

main()
#%%
print(dico_mots["upwelling"])
print(len(dico_mots))
# %%

print (sorted(dico_mots.keys()))

# %%
