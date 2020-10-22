from tkinter import *
from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from tkinter.filedialog import askdirectory
from tkinter import messagebox
from tqdm.auto import tqdm
import time
# path="C://Users//othma//Downloads"
# os.chdir(path)
screen=Tk()
screen.geometry("1080x720")
screen.title("Téléchargement Sur Voir Animé")

##Initialisation de valeur
site="ya rien"
nbr=""
name=""
vid=""
manga_name=""
## Fonction de l'UI
def all():
    try:
        geck

    except NameError:
        messagebox.showerror(title="Aucun chemin choisi", message="OH pelo met un chemin hachek")

    global entree,site,nbr,num
    if entree.get()=="" or entree.get()[:4]!="http":
        messagebox.showinfo(title="Lien non valide", message="Veuillez saisir un lien correcte")

    elif num.get()=='' or num.get().isalpha():

        messagebox.showinfo(title="Nombre non valide", message="Veuillez saisir une valeur correcte")
    else:

        nbr=int(num.get())
        site=entree.get()
        begin()

def change():
    global path
    path=askdirectory(title='Select Folder')
    if path !='':
        path="//".join(list(path.split("/")))
        os.chdir(path)
        pth.configure(text="  Votre path est : "+os.getcwd())
    elif path =='' or pth.cget('text')=='':
        messagebox.showinfo(title="Aucun chemin choisi", message="Veuillez choisir un chemin")

def allu(event):
    try:
        geck

    except NameError:
        messagebox.showerror(title="Aucun chemin choisi", message="OH pelo met un chemin hachek")

    global entree,site,nbr,num
    if entree.get()=="" or entree.get()[:4]!="http":
        messagebox.showinfo(title="Lien non valide", message="Veuillez saisir un lien correcte")

    elif num.get()=='' or num.get().isalpha():

        messagebox.showinfo(title="Nombre non valide", message="Veuillez saisir une valeur correcte")
    else:

        nbr=int(num.get())
        site=entree.get()
        begin()
def change_gecko():
    global geck
    geck=askdirectory(title='Select Folder')
    if geck !='':
        geck="//".join(list(geck.split("/")))+"//geckodriver.exe"
    elif geck =='':
        messagebox.showinfo(title="Aucun chemin choisi", message="Veuillez choisir un chemin")

### ENTRY
entree = Entry(screen, width=75)
entree.place(x=200,y=300)

num=Entry(screen, width=35)
num.place(x=680,y=300)

### BUTTON
dl=Button(screen,text="Télecharger cet épisode",fg='white', bg='purple', font=('comicsans', 10),command=all )
dl.place(x=350,y=350)
change_path=Button(screen, text="Changer le path",fg='white', bg='purple', font=('comicsans', 10),command=change )

change_path.place(x=500,y=0)

change_pth=Button(screen, text="Changer le path pour geckodriver",fg='white', bg='purple', font=('comicsans', 10),command=change_gecko )

change_pth.place(x=650,y=0)

###LABEL
nn = Label(screen, text="Lien de téléchargement",font=("Helvetica", 16))
nn.place(x=330,y=250)

ui= Label(screen, text="Nombre d'épisode", font=("Helvetica", 16))
ui.place(x=700,y=250)

pth=Label(screen,text="  Votre path est : "+ os.getcwd(),font=("Helvetica", 16))
pth.place(x=0,y=0)

bn=Label(screen,text="Téléchargement de : ",font=("Helvetica", 16))
bn.place(x=0,y=50)

url="http://voiranime.com/naruto-shippuden-085-vf/"



### Fonction pour dl

def begin():
    global site, nbr
    if site[:4] != "http":
        print("Euh je suis quasiment sur que ce que tu viens de rentrer n'est pas une un lien")
    else:
        for i in range(nbr):
            screen.update()
            traitement_page(site)
            bn.configure(text="Téléchargement de : l'épisode "+name+" de "+manga_name)
            screen.update()
            if nbr!=1:
                site=Next(site)

def traitement_page(site):
    global name,manga_name
    if "voiranime" in site :
        name=site.split("/")[-2].split('-')[-2]
        bn.configure(text="Téléchargement de : l'épisode "+name)
        manga_name=get_name(site)
        page = requests.get(site)
        soup = BeautifulSoup(page.text, 'html.parser')
        screen.update()
        kl=str(soup.findAll("span")[4].contents).split("=")[-1].split(">")[1].partition("</a")[0]
        get_le_site=soup.find("div", {"id": "player-embed"}).contents[1]['src']
        Get_la_video(get_le_site)


    if "01streaming" in site:
        name=site.split("-")[-1][0]
        bn.configure(text="Téléchargement de : l'épisode "+name)
        manga_name=get_name(site)
        options = Options()
        options.add_argument('--headless')
        dri = webdriver.Firefox(options=options)
        dri.get(site)
        time.sleep(3)
        op=dri.find_elements_by_tag_name("img")
        op[3].click()
        ab=dri.find_elements_by_tag_name("div")
        for i in range(4):
            ab[0].click()
        ifr=dri.find_elements_by_tag_name("iframe")
        src=ifr[0].get_attribute("src")
        Get_la_video(src)
        dri.close()
    if "seriestreaming" in site:
        print("ghj")

def Get_la_video(work_str):
    global vid,site,manga_name,site
    if "gounlimited" in work_str:
        soup=BeautifulSoup(requests.get(work_str).text,"html.parser")
        ui=soup.text
        work_str=ui[65513:]
        op=work_str.split('|')
        src="https://"+op[-2].split(".")[0][:-1]+".gounlimited.to/"+op[-3]+"/v.mp4"
        if BeautifulSoup(requests.get(src).text,"html.parser").text=='error_nofile' or str(BeautifulSoup(requests.get(src).text,"html.parser").find("title")) == "<title>500 Internal Server Error</title>":
            print("bah ça marche pas avec " + src)
            messagebox.showerror(title="Episode "+name, message="L'épisode "+name+" de "+manga_name +" n'a pas pu être téléchargé car les vidéos ne sont plus disponibles.")
        else:
            vid=src
            download_video_series([vid])
            screen.update()
            messagebox.showinfo(title="Téléchargement réussi", message="L'épisode "+name+" de "+manga_name + " a été téléchargé avec succès !!")
    elif "mystream" in work_str:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Firefox(options=options,executable_path=geck)
        print(work_str)
        driver.get(work_str)
        if driver.title == "Video not found — Mystream" and "voiranime" in site:
            options = Options()
            options.add_argument('--headless')
            dri = webdriver.Firefox(options=options)
            dri.get(site)
            a=dri.find_elements_by_class_name("multilink-link")
            b=dri.find_elements_by_class_name("mn-position-fixed__close-button")
            b[0].click()
            a[2].click()
            soup=BeautifulSoup(dri.page_source,'html.parser')
            get_le_site=soup.find("div", {"id": "player-embed"}).contents[0]['src']
            print(get_le_site)
            Get_la_video(get_le_site)
            dri.close()
        else:
            vid=driver.find_elements_by_tag_name("source")[0].get_attribute("src")
            download_video_series([vid])
            messagebox.showinfo(title="Téléchargement réussi", message="L'épisode "+name+" de "+manga_name + " a été téléchargé avec succès !!")
            driver.close()
    else:
        messagebox.showerror(title="Episode "+name, message="L'épisode "+name+" de "+manga_name +" n'a pas pu être téléchargé car les vidéos ne sont plus disponibles.")


def download_video_series(video_links):
    global name
    for link in video_links:

        file_name = "Episode "+name+".mp4"

        print ("Downloading file: %s"%file_name)

        r = requests.get(link, stream = True)
        total_size_in_bytes= int(r.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        # download started
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                if chunk:
                    progress_bar.update(len(chunk))
                    screen.update()
                    f.write(chunk)

        print ("%s downloaded!\n"%file_name)

    return
def Next(url):
    if "voiranime" in url:
        domaine="/".join(url.split('/')[:-2])+"/"
        nom=url.split('/')[-2].split("-")
        num="{:03d}".format(int(nom[-2])+1)
        nom[-2]=num
        newurl=domaine+"-".join(nom)+"/"
        return newurl
    if "01streaming" in url:
        url=url.split("-")
        kl=url[-1]
        kl=str(int(kl[0])+1)+kl[1]
        url.pop(-1)
        url.append(kl)
        newurl="-".join(url)
        return newurl
def get_name(u):
    global name
    if "voiranime" in u:
        u=u.split('/')
        L=["http:","voiranime.com","","vf","vostfr",name,""]
        for io in L:
            if io in u:
                u.remove(io)
        u="-".join(u)
        u=u.split("-")
        for io in L:
            if io in u:
                u.remove(io)
        u=" ".join(u)
        u=u.capitalize()
        return u
    if "01streaming" in u:
        u="".join(url.split("/")[4].split("-")[:-4]).capitalize()
        return u

screen.bind('<Return>',allu)
screen.resizable(False, False)
screen.mainloop()
print("Vous avez quitté")