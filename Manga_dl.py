# Import
from tkinter import *
from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from tkinter.filedialog import askdirectory
from tkinter import messagebox
import time
import inspect
from win10toast import ToastNotifier


class Manga_dl:
    def __init__(self):
        self.screen=Tk()
        self.screen.geometry("1080x720")
        self.screen.title("Téléchargement de video")
        a=inspect.getfile(inspect.currentframe()) # on get le path du fichier executé
        pp=a.split("""\\""") # On arrange le path pour avoir
        pp.pop()
        self.pp="\\".join(pp)
        self.geck=self.pp+"\\geckodriver.exe"
        self.screen.iconbitmap(self.pp+"\\dl_icon.ico")
        self.site=""
        self.nbr=""
        self.name=""
        self.vid=""
        self.mp4=""
        self.manga_name=""
        self.type=""
        self.Affichage()
        self.screen.bind('<Return>',self.Allu)
        self.screen.resizable(False, False)
        self.screen.focus_force()
        self.screen.mainloop()


    def Affichage(self):
        self.entree = Entry(self.screen, width=75)
        self.entree.place(x=200,y=300)

        self.num=Entry(self.screen, width=35)
        self.num.place(x=680,y=300)

        dl=Button(self.screen,text="Télecharger cet épisode",fg='white', bg='purple', font=('comicsans', 10),command=self.All )
        dl.place(x=350,y=350)

        change_path=Button(self.screen, text="Chemin de téléchargement des fichiers ",fg='white', bg='purple', font=('comicsans', 10),command=self.change )
        change_path.place(x=0,y=500)

        nn = Label(self.screen, text="Lien de téléchargement",font=("Helvetica", 16))
        nn.place(x=330,y=250)

        ui= Label(self.screen, text="Nombre d'épisode", font=("Helvetica", 16))
        ui.place(x=700,y=250)

        self.pth=Label(self.screen,text=" Le chemin de téléchargement est :   "+ os.getcwd(),font=("Helvetica", 16))
        self.pth.place(x=0,y=0)

        self.bn=Label(self.screen,text="Téléchargement de : ",font=("Helvetica", 16))
        self.bn.place(x=0,y=50)

        self.ghj= Label(self.screen, text="Statut du téléchargement : ", font=("Helvetica", 16))
        self.ghj.place(x=350,y=650)


    def change(self):
        path=askdirectory(title='Choisissez un dossier')
        if path !='':
            path="//".join(list(path.split("/")))
            os.chdir(path)
            self.pth.configure(text="  Votre path est : "+os.getcwd())
        elif path =='' or self.pth.cget('text')=='':
            messagebox.showinfo(title="Aucun chemin choisi", message="Veuillez choisir un chemin")

    def Launch(self):
        self.screen.update()
        if self.site[:4] != "http":
            messagebox.showinfo(title="Site invalide", message="Veuillez saisir un site commençant par http.")
        else:
            for i in range(self.nbr):
                self.screen.update()
                self.traitement_page(self.site)
                self.bn.configure(text="Téléchargement de : l'épisode "+self.name+" de "+self.manga_name)
                self.screen.update()
                self.Get_la_video()
                self.screen.update()
                if self.mp4[-3:]=="mp4":
                    self.download_video_series(self.mp4)
                    self.screen.update()
                    toaster = ToastNotifier()
                    toaster.show_toast("Episode Téléchargé",
                                    "L'épisode " +self.name +" de "+self.manga_name+"  est téléchargé",
                                    icon_path=self.pp+"\\dl_icon.ico",
                                    duration=10,
                                    threaded=True)
                # pass
                if self.nbr!=1:
                    self.site=self.Next(self.site)

    def traitement_page(self,site):
        if "voiranime" in site :
            self.name=site.split("/")[-2].split('-')[-2]
            self.manga_name=self.get_name(site)
            self.bn.configure(text="Téléchargement de : l'épisode "+self.name+" de "+self.manga_name)
            self.screen.update()
            page = requests.get(site)
            soup = BeautifulSoup(page.text, 'html.parser')
            self.ghj.configure(text="Statut du téléchargement :  Parcours de la page ")
            self.screen.update()
            kl=str(soup.findAll("span")[4].contents).split("=")[-1].split(">")[1].partition("</a")[0]
            get_le_site=soup.find("div", {"id": "player-embed"}).contents[1]['src']
            self.ghj.configure(text="Statut du téléchargement :  Recherche de la vidéo ")
            self.screen.update()
            self.vid=get_le_site
            # self.Get_la_video(get_le_site)


        if "01streaming" in site:
            self.name=site.split("-")[-1][:-1]
            self.manga_name=self.get_name(site)
            if self.type=="film":
                self.bn.configure(text="Téléchargement de : "+self.manga_name)
            else:
                self.bn.configure(text="Téléchargement de : l'épisode "+self.name+" de "+self.manga_name)
            self.screen.update()
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--mute-audio')
            dri = webdriver.Firefox(options=options,executable_path=self.geck)
            self.ghj.configure(text="Statut du téléchargement :  Parcours de la page ")
            self.screen.update()
            dri.get(site)
            self.screen.update()
            if dri.title == "www.01streaming.net | 523: Origin is unreachable":
                messagebox.showinfo(title="Impossible", message="Le site est momentanément indisponible")
            else:
                time.sleep(3)
                self.screen.update()
                ul=dri.find_elements_by_tag_name("ul")
                bn_ul=ul[5]
                li=bn_ul.find_elements_by_tag_name("li")
                xcv=0
                for io in li:
                    if xcv!=1:
                        if "EMBED" in io.text or "mystream" in io.text or "vudeo" in io.text or "Vudeo" :
                            xcv=1
                            # io.click()
                            # dri.switch_to.window(dri.window_handles[1])
                            # dri.close()
                            # dri.switch_to.window(dri.window_handles[0])
                            ifr=dri.find_elements_by_tag_name("iframe")
                            src=ifr[li.index(io)].get_attribute("src")
                            self.vid=src
                            # self.Get_la_video(src)
        if "11anim.com" in site:
            print(site)
            bn=site.split("-")
            self.name=bn[1]
            self.manga_name=site.split("/")[-1].split("-")[0]
            options = Options()
            options.add_argument('--headless')
            dri = webdriver.Firefox(options=options)
            dri.get(site)
            self.screen.update()
            dri.find_element_by_class_name("playButton").click()
            if len(dri.window_handles) == 2:
                dri.switch_to_window(dri.window_handles[1])
                dri.close()
                dri.switch_to_window(dri.window_handles[0])
            dri.quit()
            self.screen.update()
            time.sleep(5)
            soup=BeautifulSoup(dri.page_source,"html.parser")
            div=soup.findAll("iframe")[1]["src"]
            div="https:"+div
            self.vid=div
            # self.Get_la_video(div)

    def Get_la_video(self):#,work_str
        self.screen.update()
        # print(self.vid)
        if "gounlimited" in self.vid:
            soup=BeautifulSoup(requests.get(self.vid).text,"html.parser")
            ui=soup.text
            work_str=ui[65513:]
            op=work_str.split('|')
            src="https://"+op[-2].split(".")[0][:-1]+".gounlimited.to/"+op[-3]+"/v.mp4"
            if BeautifulSoup(requests.get(src).text,"html.parser").text=='error_nofile' or str(BeautifulSoup(requests.get(src).text,"html.parser").find("title")) == "<title>500 Internal Server Error</title>":
                print("bah ça marche pas avec " + src)
                messagebox.showerror(title="Episode "+name, message="L'épisode "+name+" de "+manga_name +" n'a pas pu être téléchargé car les vidéos ne sont plus disponibles.")
            else:
                self.ghj.configure(text="Statut du téléchargement :  Vidéo trouvé ")
                self.screen.update()
                vid=src
                self.ghj.configure(text="Statut du téléchargement :  Le téléchargement va commencer ")
                self.screen.update()
                self.mp4=vid
                self.screen.update()
        elif "mystream" in self.vid:
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--mute-audio')
            driver = webdriver.Firefox(options=options,executable_path=self.geck)
            print(self.vid)
            driver.get(self.vid)
            self.screen.update()
            if driver.title == "Video not found — Mystream" and "voiranime" in self.site:
                options = Options()
                options.add_argument('--headless')
                options.add_argument('--mute-audio')
                dri = webdriver.Firefox(options=options)
                dri.get(self.site)
                self.screen.update()
                a=dri.find_elements_by_class_name("multilink-link")
                b=dri.find_elements_by_class_name("mn-position-fixed__close-button")
                b[0].click()
                a[2].click()
                soup=BeautifulSoup(dri.page_source,'html.parser')
                self.screen.update()
                get_le_site=soup.find("div", {"id": "player-embed"}).contents[0]['src']
                print(get_le_site)
                Get_la_video(get_le_site)
                self.screen.update()
                dri.quit()
            else:
                self.ghj.configure(text="Statut du téléchargement :  Vidéo trouvé ")
                self.screen.update()
                vid=driver.find_elements_by_tag_name("source")[0].get_attribute("src")
                driver.quit()
                self.ghj.configure(text="Statut du téléchargement :  Le téléchargement va commencer ")
                self.screen.update()
                self.mp4=vid
                self.screen.update()

        elif "vudeo" in self.vid:
            r=requests.get(self.vid)
            soup=BeautifulSoup(r.text,"html.parser")
            s=soup.findAll("script")[9].text
            url=s.split('"')[1]
            self.mp4=url
        elif "dailymotion" in self.vid:
            options = Options()
            options.add_argument('--headless')
            dri = webdriver.Firefox(options=options)
            ui="https://fr.savefrom.net/10-comment-t%C3%A9l%C3%A9charger-vid%C3%A9os-sur-dailymotion.html"
            dri.get(ui)
            time.sleep(3)
            self.screen.update()
            inpu=dri.find_element_by_tag_name("input")
            inpu.send_keys(self.vid)
            inpu.submit()
            time.sleep(5)
            self.screen.update()
            soup=BeautifulSoup(dri.page_source,"html.parser")
            a=dri.find_elements_by_tag_name("a")
            good_link=a[9].get_attribute("href")
            dri.quit()
            print(good_link)
            self.mp4=good_link
            self.screen.update()
        else:
            if self.type=="film":
                messagebox.showerror(title="Episode "+self.name, message="L'épisode "+self.name+" de "+self.manga_name +" n'a pas pu être téléchargé car les vidéos ne sont plus disponibles ou alors il n'est pas téléchargeable par le programme.")
            else:
                messagebox.showerror(title=self.manga_name, message=self.manga_name +" n'a pas pu être téléchargé car les vidéos ne sont plus disponibles ou alors il n'est pas téléchargeable par le programme.")



    def Next(self,url):
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
            kl=str(int(kl[:-1])+1)+kl[-1]
            url.pop(-1)
            url.append(kl)
            newurl="-".join(url)
            r=requests.get(newurl)
            if r.status_code == 200:
                return newurl
            else:
                a=newurl.split("-")
                a[-3]=str(int(a[-3])+1)
                a="-".join(a)
                return a
        if "11anim.com" in url:
            bn=url.split("-")
            bn[-2]=str(int(bn[-2])+1)
            url='-'.join(bn)
            return url
    def get_name(self,u):
        if "voiranime" in u:
            u=u.split('/')
            L=["http:","voiranime.com","","vf","vostfr",self.name,""]
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
            if "film" not in u:
                self.type="serie"
                u=" ".join(u.split("/")[-2].split("-")[:-4]).capitalize()
                return u
            else:
                self.type="film"
                u=u.split("/")[-2].replace("-"," ").capitalize()
                return u
    def download_video_series(self,link):
        # print(link)
        if self.type =="film":
            file_name=self.manga_name
        else:
            file_name = "Episode "+self.name+".mp4"

        print ("Downloading file: %s"%file_name)
        r = requests.get(link, stream = True)
        fg=int(r.headers['content-length'])

        size=round(fg*0.00000095367432)
        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024*1024):
                self.screen.update()
                if chunk:
                    self.screen.update()
                    f.write(chunk)
                    cv=os.path.getsize(file_name)*0.00000095367432
                    self.ghj.configure(text="Statut du téléchargement :  " +str(round(cv))+" Mo  /  "+str(size) + " Mo"+"  ("+str(round(((round(cv)*100))/size))+" %/ 100%)")
                    self.screen.update()
        f.close()

        print ("%s downloaded!\n"%file_name)
        self.ghj.configure(text="Statut du téléchartgement :")
        self.bn.configure(text='Téléchargement de : ')

    def All(self):
        if self.entree.get()=="" or self.entree.get()[:4]!="http":
            messagebox.showinfo(title="Lien non valide", message="Veuillez saisir un lien correcte")

        elif self.num.get()=='' or self.num.get().isalpha():

            messagebox.showinfo(title="Nombre non valide", message="Veuillez saisir une valeur correcte")
        else:

            self.nbr=int(self.num.get())
            self.site=self.entree.get()
            self.Launch()

    def Allu(self,event):
        self.All()




if __name__ =="__main__":
    a=Manga_dl()
    os.system("taskkill /F /IM Firefox.exe")
    os.system("taskkill /F /IM geckodriver.exe")
    os.remove("geckodriver.log")