import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb
from PIL import ImageTk, Image
import random
import time
import copy
import datetime                                         
import simpleaudio as sa
class Main: #hlavna trieda ktora ma ostatne podtriedy (definuje Menu)
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Dama')
        img = self.daj_fon('obrazky/background/background_menu.png')
        self.panel = tk.Label(self.root, image=img)
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.panel.place(x=0, y=0)
        self.panel.pack(fill="both", expand=1)

        self.buttons = self.give_img_buttons()

        tk.Button(self.root, image=self.buttons[0], bg = "#3a1e13", activebackground = "#3a1e13", command=self.load_game_1).place(x=270, y=350) #tlacidlo "Player vs computer"
                
        tk.Button(self.root, image=self.buttons[1], bg = "#3a1e13", activebackground = "#3a1e13", command=self.load_game_2).place(x=270, y=420) #tlacidlo "Player vs Player"
                
        tk.Button(self.root, image=self.buttons[2], bg = "#3a1e13", activebackground = "#3a1e13", command=self.load_save_game).place(x=270, y=490) #tlacidlo "load game"

        tk.Button(self.root, image=self.buttons[3], bg = "#3a1e13", activebackground = "#3a1e13", command=self.init_option).place(x=270, y=560)  #tlacislo "options"

        self.zoz_option = ['Color pesiakov:White/Black\n', 'Lvl:Middle\n']
        self.root.mainloop()
        
        



    def give_img_buttons(self):  #obrazky tlacidl
        img = Image.open('obrazky/image_button/b_big_startmenu_p_vs_c.png')
        but_p_vs_c = ImageTk.PhotoImage(img)
        img = Image.open('obrazky/image_button/b_big_startmenu_p_vs_p.png')
        but_p_vs_p = ImageTk.PhotoImage(img)
        img = Image.open('obrazky/image_button/b_big_startmenu_load.png')
        but_load = ImageTk.PhotoImage(img)
        img = Image.open('obrazky/image_button/b_big_startmenu_options.png')
        but_option = ImageTk.PhotoImage(img)

        return [but_p_vs_c, but_p_vs_p, but_load, but_option]
            
    def daj_fon(self, path):  #definuje obrazok fonu
        img = Image.open(path)
        width = 800
        height = 800
        imag = img.resize((width, height))
        image = ImageTk.PhotoImage(imag)
        return image
    
    def load_game_1(self):   #zapise do suboru setting pre hry proti pocitaca
        with open('setting.txt', 'a') as t:
            if not self.existuje_subor('setting.txt'):
                t.write(''.join(self.zoz_option))
            t.write('New Game\n')
            t.write('Player vs Computer\n')
            aky_color = mb.askyesno(title="Choose color", message="Do you want to play white?")
            if aky_color:
                t.write('Color: White\n')
            else:
                t.write('Color: Black\n')
        self.init_game()

    def load_game_2(self):  #zapise do suboru setting pre hry proti hraca
        with open('setting.txt', 'a') as t:
            if not self.existuje_subor('setting.txt'):
                t.write(''.join(self.zoz_option))
            t.write('New Game\n')
            t.write('Player vs Player\n')
            t.write('Color: White\n')
        self.init_game()

    def load_save_game(self):   #zapise do suboru setting pre ulozenu hru
        over = self.existuje_subor('last_save.txt')
        if over:
            with open('setting.txt', 'a') as t:
                if not self.existuje_subor('setting.txt'):
                    t.write(''.join(self.zoz_option))
                t.write('Load Game\n')
            self.init_game()
        else:
            self.vypis_warning()

    def init_game(self):            #zacne hru
        self.root.destroy()
        pole = self.Ploha()
        self.Hraci(pole)

    def init_option(self):      #otvori options
        self.root.destroy()
        self.option = self.GameOptions()
        

    def existuje_subor(self, meno_suboru):  #overi ci existuje ulozena hra
        try:
            t = open(meno_suboru)
            if t.read() == '':
                return False
            t.close()
            return True
        except FileNotFoundError:
            return False

    def vypis_warning(self):        #vypise warning na neexistovanie ulozenej hry
        self.war = tk.Label(self.root, text = "Ulozena hra neexistuje", width=55, bg='#ffaaaa', font = ('Consolas', 20, 'bold'))
        self.war.place(x=0, y=100)
        self.war.after(2000 , lambda: self.war.destroy())

    def exit(self):         #zatvory hru
        t = open('setting.txt', 'w')
        t.close()
        self.root.destroy()



    class GameOptions:  #trieda dafinue okno options
        
        def __init__(self):
            self.okno = tk.Tk()
            self.okno.protocol("WM_DELETE_WINDOW", self.back_to_menu)
            
            self.background = tk.Label(self.okno, width = 50, height = 30)
            self.background.pack()
            
            tk.Label(self.okno, text = 'Choose color', width=23, font = ('Consolas', 20, 'bold')).place(x=0, y=0)
            
            self.color = IntVar(value=1)
            self.white = tk.Radiobutton(self.okno, text = 'White vs Black', variable=self.color, value=1, font = 'Consolas 15')
            self.blue  = tk.Radiobutton(self.okno, text = 'Blue vs Red', variable=self.color, value=0, font = 'Consolas 15')
            self.white.pack()            
            self.blue.pack()
            self.white.place(x=10, y=50)
            self.blue.place(x=190, y=50)

            tk.Label(self.okno, text = 'Choose Lavel', width=25, bg='#ffaaaa', font = ('Consolas', 20, 'bold')).place(x=0, y=100)

            self.lvl = IntVar(value=2)
            self.easy = tk.Radiobutton(self.okno, text = 'Easy', variable=self.lvl, value=1, font = 'Consolas 15')
            self.middle = tk.Radiobutton(self.okno, text = 'Middle', variable=self.lvl, value=2, font = 'Consolas 15')
            self.hard = tk.Radiobutton(self.okno, text = 'Hard ', variable=self.lvl, value=3, font = 'Consolas 15')
            self.easy.pack()
            self.middle.pack()
            self.hard.pack()
            self.easy.place(x=10, y=150)
            self.middle.place(x=120, y=150)
            self.hard.place(x=250, y=150)
            
            self.but = self.give_button()
            self. save = tk.Button(self.okno, image=self.but[0], bg = "#3a1e13", command=self.save_option)
            self.save.pack()
            self.save.place(x=60, y=400)

            self.back = tk.Button(self.okno, image=self.but[1], bg = "#3a1e13", command=self.back_to_menu)
            self.back.pack()
            self.back.place(x=180, y=400)

        def give_button(self):          #definue obrzky tlacidl
            img = Image.open('obrazky/image_button/b_save.png')
            but_save = ImageTk.PhotoImage(img)
            img = Image.open('obrazky/image_button/b_back.png')
            but_back = ImageTk.PhotoImage(img)
            return [but_save, but_back]
        
        def save_option(self):          #ulozi zmeny
            with open('setting.txt', 'w') as t:
                if self.color.get():
                    t.write('Color pesiakov:White/Black\n')
                else:
                    t.write('Color pesiakov:Blue/Red\n')
                if self.lvl.get() == 1:
                    t.write('Lvl:Easy\n')
                elif self.lvl.get() == 2:
                    t.write('Lvl:Middle\n')
                else:
                    t.write('Lvl:Hard\n')
            okey = tk.Label(self.okno, text= 'Options were loaded successfully', width = 32, bg='green', font='Consolas 15')
            okey.pack()
            okey.place(x=0, y=300)
            
        def back_to_menu(self):     #vrati na menu
            self.okno.destroy()
            Main()
  
    class Ploha:                #tato trieda odpoveda za vsetke zmeny na ihrisku
        def __init__(self):
            ########################################        
            self.peski = None           #tu budu obrazky pesiakov
            self.aktiv_peski = None             #tu budu obrazky aktivnych pesiakov
            self.zoz_hodov = []                             #vsetke urubene pohyby ( pre zapisania logov)
            self.pohyb_p = sa.WaveObject.from_wave_file("zvuk/pohyb.wav")
            self.mr_poc_pes = []
            self.mr_hrac_pes = []
            self.sirka = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
            self.vyska = ['1', '2', '3', '4', '5', '6', '7', '8']
            self.color = 1           #akym colorom hrate *(default = white)
            self.frb_change = 1
            
            ############################################
            
            self.logy = 'logy_hodov.txt'                #nazov suboru, kde sa budu chranit logy
            self.nedokoncena_hra = 'last_save.txt'                  #posledna ulozena hra
            self.stare_logy = 'last_save_logs.txt'
            self.nova_hra = True            # hrate teraz novu hru, alebo ulozenu
            
            ###########################################
                

        def start_game(self):               #definuje ihrisko
            self.gl_okno = Tk()  #
            self.gl_okno.title("Dama")          #nazva hry
            self.pole = Canvas(self.gl_okno, width=800,height=640,bg='#FFFFFF')#okno hry
            self.pole.pack()
            self.gl_okno.protocol("WM_DELETE_WINDOW", self.zatvor_hru)    #otazka, ak zatvarate subor

            self.doska = PhotoImage(file="obrazky/background/chess_board.png") #damova doska
            self.tlacidla = self.vytvor_tlacidla()
            self.ihrisko = self.nova_igra()        #pešiaky
    
        def zatvor_hru(self):           #zatvori hru a vrati sa do Menu
            ask = mb.askyesno(title='Exit', message='Do you really want to leave?')
            if ask:
                self.delete_hru()
                self.gl_okno.destroy()
                Main()


        def delete_hru(self):           #vymaze setting
            t = open('setting.txt')
            zoz_option = [t.readline(), t.readline()]
            t.close()
            with open('setting.txt', 'w')as t:
                t.write(''.join(zoz_option))

        def zvuk_pohyb(self):           #definue zvuk pohybu
            play_obj = self.pohyb_p.play()

        def vypis_save(self):           #vypise podtvrdenie 
            save = tk.Label(self.gl_okno, text='Game vas loaded', width=23, bg='green', font='Consolas 10')
            save.place(x=640, y=140)
            save.after(3000, lambda: save.destroy())

        def izobrazheniya_peshek(self, subor, biele = True):#vyrobi zoznam obrazkov pesiakov
            self.subor = subor
            i1=PhotoImage(file=subor + "/white.png")  #biely obycajny
            i2=PhotoImage(file=subor + "/white_king.png")  #biela kralovna
            i3=PhotoImage(file=subor + "/black.png")  #cierny obycajny
            i4=PhotoImage(file=subor + "/black_king.png")  #cierna kralovna
            i5=PhotoImage(file=subor + "/white_small.png")   #biely maly
            i6=PhotoImage(file=subor + "/black_small.png")   #cierny maly
            if biele:
                return [i1, i2, i3, i4, i5, i6]
            else:
                return [i3, i4, i1, i2, i5, i6]

        def obrazky_aktinych_peshek(self, subor, biele = True):#vyrobi zoznam obrazkov aktivnych pesiakov
            i1=PhotoImage(file=subor + "/white_akt.png")  #biela obycajna
            i2=PhotoImage(file=subor + "/white_akt_king.png")  #biela kralovna
            i3=PhotoImage(file=subor + "/black_akt.png")  #cierna obycajna
            i4=PhotoImage(file=subor + "/black_akt_king.png")  #cierna kralovna
            if biele:
                return [i1, i2, i3, i4]
            else:
                return [i3, i4, i1, i2]

        def hladaj_mrtvu(self, x, y, hrac):                #hlada mrtveho pesiaka zo zoznamu.
            if hrac:
                for i in range(len(self.mr_hrac_pes)):
                    if (x, y) == self.mr_hrac_pes[i][0]:
                        pesiak = self.mr_hrac_pes.pop(i)
                        return pesiak
            else:
                for i in range(len(self.mr_poc_pes)):
                    if (x, y) == self.mr_poc_pes[i][0]:
                        pesiak = self.mr_poc_pes.pop(i)
                        return pesiak

        def nova_igra(self):#vyrobe novy zoznam pola
            self.nova_hra = True
            pole=[[0,3,0,3,0,3,0,3],
                  [3,0,3,0,3,0,3,0],
                  [0,3,0,3,0,3,0,3],
                  [0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0],
                  [1,0,1,0,1,0,1,0],
                  [0,1,0,1,0,1,0,1],
                  [1,0,1,0,1,0,1,0]]
            return pole
        
        def stara_igra(self):  #stahne zo suboru ulozenu hru
            self.nova_hra = False
            hrac  = {'Hraca.':True, 'Pocitaca.':False}
            cej_hod = 1
            pole = []
            color = 1  #biely
            aka = 0 #vs Computer
            with open(self.nedokoncena_hra) as t:
                col_pes = t.readline().strip().split(':')[1]
                if col_pes == 'White/Black':
                    subor = 'obrazky/image_white_checker'
                else:
                    subor = 'obrazky/image_blue_checker'
                lvl = t.readline().strip().split(':')[1]
                if lvl == 'Easy':
                    lvl == 1
                elif lvl == 'Middle':
                    lvl = 2
                else:
                    lvl = 3
                rezim = t.readline().strip().split()
                if rezim[2] == 'Player':
                    aka = 1
                for i in range(8):    
                    riadok = t.readline().strip().split()
                    a = []
                    for j in range(8):
                        a.append(int(riadok[j]))
                    pole.append(a)
                hod = t.readline().strip().split()
                cej_hod = hrac[hod[1]]
                if hod[4] == 'ciernmy.':
                    color = 0
            return aka, pole, cej_hod, color, subor, lvl

        def vymen_pesiaky(self):            #zmeny hodnoty pesiakov na ihrisku (pouziva sa pre hry proti hraca)
            for i in range(8):
                for j in range(8):                        
                    if self.ihrisko[i][j] == 1 or self.ihrisko[i][j] == 2:
                        self.ihrisko[i][j] += 2
                    elif self.ihrisko[i][j] != 0:
                        self.ihrisko[i][j] -= 2
                        
            self.frb_change = not self.frb_change        
            self.peski = self.izobrazheniya_peshek(self.subor, self.frb_change)
            self.aktiv_peski = self.obrazky_aktinych_peshek(self.subor, self.frb_change)
                    
                    
        def vivod(self, x_poz_1,y_poz_1,x_poz_2,y_poz_2):#nakresli ihrisko
            k = 80
            self.pole.delete('all')
            self.pole.create_image(0, 0, anchor=NW, image=self.doska) 
            self.kresli_mrtve(len(self.mr_hrac_pes), len(self.mr_poc_pes))           #maly pesiake na pravej strane
            for y in range(8):                          #vytvory na doske pesiaky
                for x in range(8):
                    z=self.ihrisko[y][x]
                    if z:
                        if (x, y) != (x_poz_1, y_poz_1):
                            self.pole.create_image(x*k,y*k, anchor=NW, image=self.peski[z-1])
                
                #aktivny pesiak        
            z=self.ihrisko[y_poz_1][x_poz_1]
            if z:
                akt = self.pole.create_image(x_poz_1*k,y_poz_1*k, anchor=NW, image=self.aktiv_peski[z-1],tag='ani')
            
            #koef. pre animacie
            kx = 1 if x_poz_1<x_poz_2 else -1
            ky = 1 if y_poz_1<y_poz_2 else -1
            for i in range(abs(x_poz_1-x_poz_2)):#анимация перемещения пешки
                for ii in range(25):
                    self.pole.move('ani',0.04*k*kx,0.04*k*ky)
                    self.pole.update()#обновление
                    time.sleep(0.01)


        def kresli_mrtve(self, comp_p, hrac_p):   #nakresli malych pesiakov na pravej strane
            k = 40
            if self.color:
                pesiak1, pesiak2 = self.peski[4], self.peski[5]
            else:
                pesiak1, pesiak2 = self.peski[5], self.peski[4]
            for i in range(hrac_p):
                self.pole.create_image(650 + i%3*(k+10) , 188 + i//3 * (k + 10), anchor=NW, image=pesiak1)
                
            for j in range(comp_p):
                self.pole.create_image(650 + j%3*(k+10) , 590 - j//3 * (k + 10), anchor=NW, image=pesiak2)
                    

        def vytvor_tlacidla(self):        #vytvori tlacidlo "nova hra"
            tl_new_game = PhotoImage(file="obrazky/image_button/b_newgame.png")  #tlacidlo

            tl_save = PhotoImage(file="obrazky/image_button/b_savegame.png")  #tlacidlo

            tl_undo = PhotoImage(file="obrazky/image_button/b_undo.png")  #tlacidlo
            
            return [tl_new_game, tl_save, tl_undo]

        
        def soobsenie(self, s):   #da otazku, kedy sa skonci hra
            z='Игра завершена'
            if s==1:
                i=mb.askyesno(title=z, message='Vyhrali ste!\nTlacnite "Ano" ak chcete zacat znovu.',icon='info')
            elif s==2:
                i=mb.askyesno(title=z, message='Prehrali ste!\nTlacnite "Ano" ak chcete zacat znovu.',icon='info')
            elif s==3:
                i=mb.askyesno(title=z, message='Pohyby nie su.\nTlacnite "Ano" ak chcete zacat znovu.',icon='info')
            elif s==4:
                i=mb.askyesno(title=z, message='Patove situacia.\nTlacnite "Ano" ak chcete zacat znovu.',icon='info')
            if not self.nova_hra:      #ak hrate staru, tak vymaze ju
                self.vymaz_subor(self.nedokoncena_hra)
            if i:                   
                return True
            else:
                
                return False
            self.zapis_do_suboru(True, self.nova_hra) #zapise do logov vysledok
            
                
        def zapis_hody(self, kto, poz1_x, poz1_y, poz2_x, poz2_y, typ_peshki): #zoznam urobenych pohybov
            ret = self.sirka[poz1_x] + self.vyska[poz1_y] + '-' + self.sirka[poz2_x] + self.vyska[poz2_y]
            self.zoz_hodov.append((kto, ret, typ_peshki))

        def zapis_mrtvu(self, poz_x, poz_y, typ, kto):  #zapise coord mrtveho pesiaka
            if kto:
                self.mr_hrac_pes.insert(0, ((poz_x, poz_y), typ))
            else:
                self.mr_poc_pes.insert(0, ((poz_x, poz_y), typ))


        def zapis_do_suboru(self, vysl, color_cheker, lvl, mode, turn, stara = False):     #zapise do vseobcnych resp. logov ulozenej hry vsetke pohyby
            subor = self.logy
            if not self.nova_hra and (stara or vysl):           #ak hrate ulozenu hru a chcete ju dalej ulozit alebo ste ju skoncily
                self.load_logs(self.stare_logy, vysl)
            elif self.nova_hra and stara:                           #ak hrate novu  a chcete ju ulozit
                self.skopiruj_subor(self.logy, self.stare_logy)   #ulozi pohuby z logov ulozenej hry do vseobecnych
                self.load_logs(self.stare_logy, vysl)
                self.vymaz_subor(self.stare_logy)
            else:
                self.load_logs(self.logy, vysl)
            
                
            if stara:                                               #ak chcete ulozit hru
                self.zapis_staru(color_cheker, lvl, mode, turn)                   #ulozi pole do suboru
            if not self.nova_hra and vysl:                          #ak ste hrali staru a skoncily ju
                self.skopiruj_subor(self.logy, self.stare_logy, True)  #ulozi logy do vseobecnysh logov
                self.vymaz_subor(self.stare_logy)                       #vymaze logy ulozenej hry
                
            self.zoz_hodov = []

        def load_logs(self, file, vysl):                    #zapise logy pohybov
            with open(file, 'a') as t:
                if self.nova_hra or not(self.existuje_subor(file)):
                    cas = datetime.datetime.today().strftime("%Y.%m.%d %H:%M:%S")
                    if self.existuje_subor(file):
                        t.write('\n')
                    t.write('\n' + cas + ' Hra ')
                    if vysl:
                        t.write('dokoncena. ')
                    else:
                        t.write('nedokoncena. ')
                    if self.color:
                        t.write('Hrac hra bielmy\n')
                    else:
                        t.write('Hrac hra ciernmy\n')
                for hody in range(0, len(self.zoz_hodov)):
                    hod_bielych = self.zoz_hodov[hody][0]
                    if hod_bielych:
                        if hody == 0:
                            t.write('\nBiele: ' + self.zoz_hodov[0][1])
                        elif self.zoz_hodov[hody][0] != self.zoz_hodov[hody-1][0]:
                            t.write('\nBiele: ' + self.zoz_hodov[hody][1])
                        else:
                            t.write(', ' + self.zoz_hodov[hody][1])
                    else:
                        if hody == 0:
                            t.write('\nCierne: ' + self.zoz_hodov[0][1])
                        elif self.zoz_hodov[hody][0] != self.zoz_hodov[hody-1][0]:
                            t.write('\nCierne: ' + self.zoz_hodov[hody][1])
                        else:
                            t.write(', ' + self.zoz_hodov[hody][1])
            
        def zapis_staru(self, color_cheker, lvl, mode, turn):                 #ulozi ihrisko do suboru
            with open(self.nedokoncena_hra, 'w') as t:
                if self.subor == 'obrazky/image_blue_checker':
                    t.write('Color pesiakov:Blue/Red\n')
                else:
                    t.write('Color pesiakov:White/Black\n')
                if lvl == 1:
                    t.write('Lvl:Easy\n')
                elif lvl == 2:
                    t.write('Lvl:Middle\n')
                else:
                    t.write('Lvl:Hard\n')
                if mode:
                    t.write('Player vs Player\n')
                else:
                    t.write('Player vs Computer\n')
                
                for i in range(len(self.ihrisko)):
                    t.write(str(self.ihrisko[i][0]))
                    for j in range(1, len(self.ihrisko[i])):
                        t.write(' ' + str(self.ihrisko[i][j])) 
                    t.write('\n')
                if turn:
                    t.write('hod Hraca. ')
                    if self.color:
                        t.write('Hrac hra bielmy.\n')
                    else:
                        t.write('Hrac hra ciernmy.\n')
                else:
                    t.write('hod Pocitaca. ')
                    if self.color:
                        t.write('Hrac hra bielmy.\n')
                    else:
                        t.write('Hrac hra ciernmy.\n')


        def existuje_subor(self, meno_suboru):  #overi ci existuje ulozena hra
            try:
               t = open(meno_suboru)
               if t.read() == '':
                   return False
               t.close()
               return True
            except FileNotFoundError:
                return False

        def vymaz_subor(self, subor):           #vymaze obsah suboru
            t =  open(subor, 'w')
            t.close()

        def skopiruj_subor(self, subor1, subor2, vysl=False):   #kopiruje obsah subor2 do subor1
            with open(subor1, 'a') as t:
                if self.existuje_subor(subor2):
                    sub = open(subor2)
                    for i in sub:
                        s = i
                        if vysl:
                            if 'nedokoncena' in s:
                                s = i
                                s = s.replace('nedokoncena', 'dokoncena')
                        t.write(s)
                    sub.close()

    class Hraci:        #trieda odpoveda za vsetke pohyby a zmeny hodnot pesiakov
        def __init__(self, ploha):
            self.hra = ploha
            self.hra.start_game()
            tk.Button(self.hra.pole, image=self.hra.tlacidla[0], command=self.init_hru).place(x=655, y=20)
            tk.Button(self.hra.pole, image=self.hra.tlacidla[1], command=self.load_game).place(x=655, y=60)
            tk.Button(self.hra.pole, image=self.hra.tlacidla[2], command=self.vozvrat).place(x=655, y=100)
            self.poz1_x, self.poz1_y, self.poz2_x, self.poz2_y = -1, 0, 0, 0#pozicie 1, pozicie 2 pesiaka (pre pohybu)
            self.n2_spisok=()                                               #konečný zoznam pohybov počítača
            self.o_rez = 0                                                  #rozdiel pesiakov po pohybu
            self.k_rez = 0                                                  #pocet predpokladanych akcií(rata pre hladamia najlepsieho pohybu)
            self.ur = 2
            #kolko vie pocitac pohybov napred
            self.f_hi = True  #hod hraca
            self.zoz_akt_p = []  #mozni oihyby hraca< ak zacal hrat nieakym pesiakom
            ##############################
            self.init_hru()
            self.hra.vivod(-1, -1, -1, -1)
            self.hra.pole.bind("<Button-1>", self.pozicia)
             
            mainloop()
            ###################################



        def init_hru(self, nova=True):    #nastavi hru (stara alebo nova, color pesiakov, a t.d.)
            self.hra.zoz_hodov = []
            with open('setting.txt') as t:
                color_pes = t.readline().strip().split(':')[1]
                if color_pes == 'White/Black':
                    subor = "obrazky/image_white_checker"
                else:
                    subor = "obrazky/image_blue_checker"
                lvl = t.readline().strip().split(':')
                aka_hra = t.readline().strip().split()
                ####################################
                if aka_hra[0] == 'New':
                    self.hra.mr_poc_pes = []
                    self.hra.mr_hrac_pes = []
                    self.hra.nova_hra = True
                    self.hra.ihrisko = self.hra.nova_igra()
                    if lvl[1] == 'Easy':
                        self.ur = 1
                    elif lvl[1] == 'Middle':
                        self.ur = 2
                    else:
                        self.ur = 3
                    ####################################
                    rival = t.readline().strip().split()
                    color = t.readline().strip().split()
                    ####################################
                    if rival[2] == "Computer":
                        self.proti_hraca = False
                        self.hra.pr_hrac = 0
                    else:
                        self.hra.pr_hrac = 1
                        self.proti_hraca = True
                    ####################################
                    if color[1] == 'White':
                        self.hra.color = 1
                        self.f_hi = True
                    else:
                        self.hra.color = 0
                        self.f_hi = False
                    self.hra.peski = self.hra.izobrazheniya_peshek(subor, self.hra.color)            #zoz obrazkov pesiakov
                    self.hra.aktiv_peski = self.hra.obrazky_aktinych_peshek(subor, self.hra.color)#zoz obrazkov aktivnych pesiakov
                    #####################################
                    if not self.f_hi and not(self.proti_hraca):
                        self.hod_pocitaca()
                    ####################################
                else:
                    self.hra.nova_hra = False
                    self.proti_hraca, self.hra.ihrisko, self.f_hi, self.color, subor, self.ur = self.hra.stara_igra()

                    self.hra.frb_change = self.proti_hraca and self.f_hi
                    self.hra.peski = self.hra.izobrazheniya_peshek(subor, self.hra.color and (self.f_hi or not(self.proti_hraca)))            #zoz obrazkov pesiakov
                    self.hra.aktiv_peski = self.hra.obrazky_aktinych_peshek(subor, self.hra.color and (self.f_hi or not(self.proti_hraca)))#zoz obrazkov aktivnych pesiakov
                    o_i, o_p, k_i, k_p = self.skan()#result(pocety pesiakov)
                    
                    self.hra.mr_poc_pes = [((0, 0), 0)]*(12 - o_i+k_i)
                    self.hra.mr_hrac_pes = [((0, 0), 0)]*(12 - o_p+k_p)
                    if not(self.f_hi) and not(self.proti_hraca):
                        self.hod_pocitaca()
            self.hra.vivod(-1, -1, -1, -1)

        def load_game(self):                #suhrani hru
            self.hra.zapis_do_suboru(False, 'White', self.ur, self.proti_hraca, self.f_hi, True)
            self.hra.vypis_save()

            
        def pozicia(self, event):#vyber stvorcika pre pohybu
            x,y=(event.x)//80,(event.y)//80# coord pesiaka
            if x < 8:
                if self.hra.ihrisko[y][x]==1 or self.hra.ihrisko[y][x]==2:#overim ci je to nas pesiak
                    if self.f_hi or self.proti_hraca:
                        if self.poz1_x != -1:    #ak uz vybrali pesiaka
                            self.hra.pole.delete('akt')
                        self.hra.pole.create_image(x*80,y*80, anchor=NW, image = self.hra.aktiv_peski[self.hra.ihrisko[y][x]-1], tag='akt')#pesiak stane aktivnym
                        self.poz1_x, self.poz1_y = x , y
                else:
                    if self.poz1_x != -1:#stvorcik je vybrany
                        self.poz2_x, self.poz2_y=x,y    #cielove coord
                        if self.f_hi or self.proti_hraca:#pohyb hraca
                            hod = self.hod_hraca()
                            if hod:
                                self.hra.pole.delete('akt')
                                v = self.kontrola()
                                if v:
                                    v1 = self.hra.soobsenie(v)
                                    if v1:
                                        self.init_hru() #
                                        self.hra.vivod(-1,-1,-1,-1)#kresli ihrisko
                                elif self.proti_hraca:
                                    self.hra.vymen_pesiaky()
                                    self.hra.vivod(-1, -1, -1, -1)                                
                                else:
                                    if not(self.f_hi):  #pohyb pocitaca                                
                                        self.hod_pocitaca()#pohyb pocitaca


                                
        def hod_pocitaca(self):  #urobi hod pocitaca
            self.proverka_hk(1,(),[])
            if self.n2_spisok:#overim existovanie pohybov
                kh=len(self.n2_spisok)#pocet pohybov
                th=random.randint(0,kh-1)#nahodny pohyb
                dh=len(self.n2_spisok[th])#dlzka pohybu
                for i in range(dh-1):
                    #robime pohyb
                    spisok=self.hod(1, self.n2_spisok[th][i][0], self.n2_spisok[th][i][1], self.n2_spisok[th][1+i][0],self.n2_spisok[th][1+i][1], self.f_hi) #urobime pohyb
                self.n2_spisok=[]#robime zoznam pohybov prazdnym
         
            #určime víťaza
            self.f_hi=True#ход игрока доступен  
            vysl = self.kontrola()
            if vysl:
                v1 = self.hra.soobsenie(vysl)
                if v1:
                    self.init_hru()#
                    self.hra.vivod(-1,-1,-1,-1)#kresli ihrisko
                
                
        def kontrola(self):     #overi pocet pesikov kazdej strany
            o_i, o_p, k_i, k_p = self.skan()#result(pocety pesiakov)
            if not(o_i) and not (k_i):   #ziadne su pesiaky hraca
                return 2
            elif not(o_p) and not(k_p):     #ziadne su pesiaky pocitaca
                return 1
            elif k_i == 3 and k_p == 3 and o_i == 0 and o_p == 0: #patova situacia (ak pocitac ,a iba jednu kralovnu a hrac ma iba jednu kralovnu)
                return 4
            elif self.f_hi and not(self.spisok_hi()):           #ak hrac nema moznost pohybu
                return 3
            elif not(self.f_hi) and not(self.spisok_hk()):      #ak pocitac nema moznost pohybu
                self.f_hi = False
                return 3

            else:
                return False
               
                    
        def spisok_hk(self):#robime zoznam pohybov pre pocitaca
            spisok=self.prehlad_hodov_k1([])#povinné pohyby
            if not(spisok): #ak nie su
                spisok=self.prehlad_hodov_k2([])#ostatne pohyby
            return spisok

        def proverka_hk(self, tur, n_spisok, spisok):#kontrola pohybov počítača
            if not(spisok):#еak zoznam je prazdny
                spisok=self.spisok_hk()#naplnime ho
         
            if spisok: # ak su pohyby
                k_pole=copy.deepcopy(self.hra.ihrisko)#kopiruje pole
                for ((poz1_x, poz1_y),(poz2_x, poz2_y)) in spisok:#prechadzame vsetke pohyby
                    t_spisok=self.hod(0, poz1_x, poz1_y, poz2_x,poz2_y, self.f_hi) #vrati zoznam existujucych este pohybov 
                    if t_spisok:#ak existuje este pohyb
                        self.proverka_hk(tur,(n_spisok+((poz1_x, poz1_y),)),t_spisok) #kontrola pohybov počítača
                    else:
                        self.proverka_hi(tur,[]) #kontrola pohybov hraca   #tu pocitac pozera na mozne pohyby hraca a tato funkcia meni obsah premennej s vysledokon pohybu (self.t_rez, self.o_rez)
                        if tur==1:
                            t_rez=self.o_rez/self.k_rez
                            if not(self.n2_spisok):#zapiseme ak je prazdny
                                self.n2_spisok=(n_spisok+((poz1_x, poz1_y),(poz2_x, poz2_y)),)  #pridame do zoznamu pohyb (potom z toho zoznamu pocitac vyberie pohyb)
                                self.l_rez = t_rez #ulozime hajlepsi result
                            else:
                                if t_rez == self.l_rez: #ak aktualny result sa rovna lepsiemu 
                                    self.n2_spisok +=(n_spisok+((poz1_x, poz1_y),(poz2_x, poz2_y)),)
                                if t_rez> self.l_rez:  #ak aktualny result je lepsi ako minuly lepsi
                                    self.n2_spisok=()   #vynuluje zoznam... 
                                    self.n2_spisok=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),) #...a prida novy (najlepsi) pohyb
                                    self.l_rez=t_rez#ulozime najlepsi result
                            self.o_rez=0 #vynulujme resulty
                            self.k_rez=0
         
                    self.hra.ihrisko=copy.deepcopy(k_pole)#vratime pole
            else:#???
                o_i, o_p, k_i, k_p = self.skan()#ratame vysledky pohybu (pocet pesiakov)
                self.o_rez+=((o_p + k_p) - (o_i + k_i))
                self.k_rez+=1

                
        def spisok_hi(self):#robi zoznam pohybov hraca
            spisok=self.prehlad_hodov_i1([])#povinne pohyby
            if not(spisok):
                spisok=self.prehlad_hodov_i2([])#зostatne pohyby
            return spisok

        def proverka_hi(self, tur, spisok):     #kontrola pohybov hraca
            if not(spisok):                 #ak zoznam je prazdny - naplnime ho
                spisok=self.spisok_hi()
         
            if spisok:#konntrolujeme existujuce mozne pohyby
                k_pole=copy.deepcopy(self.hra.ihrisko)#kopirujeme pole
                for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:  #prechadzame vsetke pohyby                  
                    t_spisok=self.hod(0,poz1_x,poz1_y,poz2_x,poz2_y, self.f_hi)  #vrati zoznam existujucych este pohybov
                    if t_spisok:#ak existuje este pohyb
                        self.proverka_hi(tur,t_spisok) #kontrola dialsych pohybov hraca pre urobeny pohyb
                    else:
                        if tur<self.ur:         #ak pocet predpokladenych pohybov mensia ako pocet pohybov, ktore pocitac moze predpokladat
                            self.proverka_hk(tur+1,(),[])       #kontrola pohybov počítača (
                        else:
                            o_i, o_p, k_i, k_p = self.skan()#подсчёт результата хода
                            self.o_rez+=((o_p + k_p) - (o_i + k_i))
                            self.k_rez+=1
         
                    self.hra.ihrisko=copy.deepcopy(k_pole)#возвращаем поле
            else:#доступных ходов нет
                o_i, o_p, k_i, k_p = self.skan()#подсчёт результата хода
                self.o_rez+=((o_p + k_p) - (o_i + k_i))
                self.k_rez+=1
                
        def skan(self):#подсчёт пешек на поле
            o_i=0
            o_p=0
            k_i=0
            k_p=0
            for i in range(8):
                for ii in self.hra.ihrisko[i]:
                    if ii==1:
                        o_i+=1
                    if ii==2:
                        k_i+=3
                    if ii==3:
                        o_p+=1
                    if ii==4:
                        k_p+=3
            return o_i, o_p, k_i, k_p
        
        def hod_hraca(self):
            self.f_hi=not self.f_hi#считаем ход игрока выполненным
            if self.zoz_akt_p == []:
                spisok=self.spisok_hi()
            else:
                spisok=self.zoz_akt_p
            if spisok:
                if ((self.poz1_x, self.poz1_y),(self.poz2_x, self.poz2_y)) in spisok:#проверяем ход на соответствие правилам игры
                    t_spisok=self.hod(1, self.poz1_x, self.poz1_y, self.poz2_x, self.poz2_y, not self.f_hi)#если всё хорошо, делаем ход
                    if t_spisok:#если есть ещё ход той же пешкой
                        self.zoz_akt_p = t_spisok
                        self.poz1_x, self.poz1_y = self.poz2_x, self.poz2_y
                        x, y = self.poz1_x, self.poz1_y
                        self.hra.pole.create_image(x*80, y*80, anchor=NW, image = self.hra.aktiv_peski[self.hra.ihrisko[y][x]-1], tag='akt')#рамка в выбранной клетке
                        self.f_hi=not self.f_hi#считаем ход игрока невыполненным
                        return False
                    else:
                        self.zoz_akt_p = []
                        return True
                else:
                    self.f_hi=not self.f_hi#считаем ход игрока невыполненным
                    return False
            self.hra.pole.update()#!!!обновление
                

        def hod(self, f, poz1_x, poz1_y, poz2_x, poz2_y, kto):   #zmani hodnoty pesiakov podla pohybu hraca alebo pocitaca
            typ_peshki = self.hra.ihrisko[poz1_y][poz1_x]
            if f:
                self.hra.vivod(poz1_x,poz1_y,poz2_x,poz2_y)#kreslim ihrisko
                self.hra.zvuk_pohyb()
            if poz2_y==0 and self.hra.ihrisko[poz1_y][poz1_x]==1:
                self.hra.ihrisko[poz1_y][poz1_x]=2
            if poz2_y==7 and self.hra.ihrisko[poz1_y][poz1_x]==3:
                self.hra.ihrisko[poz1_y][poz1_x]=4
            #robime pohyb           
            self.hra.ihrisko[poz2_y][poz2_x]=self.hra.ihrisko[poz1_y][poz1_x]
            self.hra.ihrisko[poz1_y][poz1_x]=0
            if f:
                self.hra.zapis_hody(kto, poz1_x, poz1_y, poz2_x, poz2_y, typ_peshki) #ulohym poheb a typ pesiaka       
            #nasekame pesiaka hraca
            kx = ky = 1
            if poz1_x < poz2_x:
                kx = -1
            if poz1_y < poz2_y:
                ky = -1
            x_poz, y_poz = poz2_x, poz2_y
            while (poz1_x != x_poz) or (poz1_y != y_poz):
                x_poz += kx
                y_poz += ky
                if self.hra.ihrisko[y_poz][x_poz]!=0:
                    typ_peski = self.hra.ihrisko[y_poz][x_poz]
                    self.hra.ihrisko[y_poz][x_poz]=0
                    if f:
                        self.hra.zapis_mrtvu(x_poz, y_poz, typ_peski, kto)
                        self.hra.vivod(-1, -1, -1, -1)
                    #overim pohyb tym istym pesiakom pre..
                    if self.hra.ihrisko[poz2_y][poz2_x]==3 or self.hra.ihrisko[poz2_y][poz2_x]==4:#...pocitaca
                        return self.prehlad_hodov_k1p([], poz2_x, poz2_y)#vrati zoznam moznych pohybov
                    elif self.hra.ihrisko[poz2_y][poz2_x]==1 or self.hra.ihrisko[poz2_y][poz2_x]==2:#...hrac
                        return self.prehlad_hodov_i1p([], poz2_x, poz2_y)#vrati zoznam moznych pohybov

                

        def vozvrat(self):  #zruso tah
            if len(self.hra.zoz_hodov) > 1 and self.f_hi:
                for i in range(2):
                    o_i, o_p, k_i, k_p = self.skan()
                    if o_p == 0 and k_p == 0:
                        self.f_hi = False
                    posledny_1 = self.hra.zoz_hodov.pop()
                    self.return_hod(posledny_1, i%2)
                    if (len(self.hra.zoz_hodov) > 0 and self.hra.zoz_hodov[-1][0] == posledny_1[0]):
                        while len(self.hra.zoz_hodov) > 0 and self.hra.zoz_hodov[-1][0] == posledny_1[0]:
                            posledny_1 = self.hra.zoz_hodov.pop()
                            self.return_hod(posledny_1, i%2)
                self.hra.vivod(-1, -1, -1, -1)
                if not self.f_hi and not(self.proti_hraca):
                    self.hod_pocitaca()
         
                    
        def return_hod(self, posledny, aka): #vrati hodnoty  na ihrisko
            poz1, poz2 = posledny[1].split('-')
            x_1, y_1 = self.hra.sirka.index(poz1[0]), int(poz1[1])-1
            x_2, y_2 = self.hra.sirka.index(poz2[0]), int(poz2[1])-1
            
            self.hra.ihrisko[y_1][x_1] = posledny[2]
            self.hra.ihrisko[y_2][x_2] = 0
            if self.proti_hraca and not(aka):
                self.hra.ihrisko[y_1][x_1] += 2
            if abs(x_1 - x_2) >= 2:
                self.vrat_na_pole(x_1, y_1, x_2, y_2, aka)
                    
                    
                
        def vrat_na_pole(self, x_1, y_1, x_2, y_2, hrac):  #vrati hodnoty mrtveho pesiaka (ak bol)
            for i in range(1, abs(x_2 - x_1)):
                kx, ky = i, i
                if x_2 < x_1:
                    kx = -kx
                if y_2 < y_1:
                    ky = -ky
                if hrac:
                    if self.hra.color:
                        mrtva = self.hra.hladaj_mrtvu(x_1 + kx, y_1 + ky, True)
                    else:
                        mrtva = self.hra.hladaj_mrtvu(x_1 + kx, y_1 + ky, False)
                else:
                    if self.hra.color:
                        mrtva = self.hra.hladaj_mrtvu(x_1 + kx, y_1 + ky, False)
                    else:
                        mrtva = self.hra.hladaj_mrtvu(x_1 + kx, y_1 + ky, True)
                if mrtva:
                    poz = mrtva[0]
                    if not (hrac) and self.proti_hraca:
                        self.hra.ihrisko[poz[1]][poz[0]] = mrtva[1] - 2
                    else:
                        self.hra.ihrisko[poz[1]][poz[0]] = mrtva[1]
                    break

        def prehlad_hodov_k1(self, spisok):#overi na povinne pohyby pre pocitaca
            for y in range(8):#skanujem pole
                for x in range(8):
                    spisok=self.prehlad_hodov_k1p(spisok,x,y)
            return spisok

        def prehlad_hodov_k1p(self, spisok,x,y):   #pre danu poziciu overi povinny pohyb (ak je) pre pocitaca
            if self.hra.ihrisko[y][x]==3:#pesiak
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    if 0<=y+2*iy<=7 and 0<=x+2*ix<=7:
                        if self.hra.ihrisko[y+iy][x+ix]==1 or self.hra.ihrisko[y+iy][x+ix]==2:
                            if self.hra.ihrisko[y+iy+iy][x+ix+ix]==0:
                                spisok.append(((x,y),(x+2*ix,y+2*iy)))#zapise pohyb do zoznamu
            elif self.hra.ihrisko[y][x]==4:#kralovna
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    error=0#moznost hodu
                    for i in  range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if error==1:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#zapise pohyb do zoznamu
                            if self.hra.ihrisko[y+iy*i][x+ix*i]==1 or self.hra.ihrisko[y+iy*i][x+ix*i]==2:
                                error+=1
                            if self.hra.ihrisko[y+iy*i][x+ix*i]==3 or self.hra.ihrisko[y+iy*i][x+ix*i]==4 or error==2:
                                if error>0:
                                    spisok.pop()#vymaze hod
                                break
            return spisok

        def prehlad_hodov_k2(self, spisok):#overi ostatne mozne nepovinne pohyby pre pocitaca
            for y in range(8):#skanuje pole 
                for x in range(8):
                    if self.hra.ihrisko[y][x]==3:#pesiak
                        for ix,iy in (-1,1),(1,1):
                            if 0<=y+iy<=7 and 0<=x+ix<=7:
                                if self.hra.ihrisko[y+iy][x+ix]==0:
                                    spisok.append(((x,y),(x+ix,y+iy)))#zapise pohyb do zoznamu
                                if self.hra.ihrisko[y+iy][x+ix]==1 or self.hra.ihrisko[y+iy][x+ix]==2:
                                    if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                        if self.hra.ihrisko[y+iy*2][x+ix*2]==0:
                                            spisok.append(((x,y),(x+ix*2,y+iy*2)))#zapise pohyb do zoznamu                 
                    if self.hra.ihrisko[y][x]==4:#kralovna
                        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                            error=0#overi moznost poybu
                            for i in range(1,8):
                                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                                    if self.hra.ihrisko[y+iy*i][x+ix*i]==0:
                                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#zapise pohyb do zoznamu
                                    if self.hra.ihrisko[y+iy*i][x+ix*i]==1 or self.hra.ihrisko[y+iy*i][x+ix*i]==2:
                                        error+=1
                                    if self.hra.ihrisko[y+iy*i][x+ix*i]==3 or self.hra.ihrisko[y+iy*i][x+ix*i]==4 or error==2:
                                        break
            return spisok

        def prehlad_hodov_i1(self, spisok):#overi na povinne pohyby pre hraca
            spisok=[]#список ходов
            for y in range(8):#сканируем всё поле
                for x in range(8):
                    spisok=self.prehlad_hodov_i1p(spisok,x,y)
            return spisok

        def prehlad_hodov_i1p(self, spisok,x,y):
            if self.hra.ihrisko[y][x]==1:#пешка
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    if 0<=y+2*iy<=7 and 0<=x+2*ix<=7:
                        if self.hra.ihrisko[y+iy][x+ix]==3 or self.hra.ihrisko[y+iy][x+ix]==4:
                            if self.hra.ihrisko[y+2*iy][x+2*ix]==0:
                                spisok.append(((x,y),(x+2*ix,y+2*iy)))#zapise pohyb do zoznamu
            if self.hra.ihrisko[y][x]==2:#пешка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    error=0#определение правильности хода
                    for i in  range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if error==1:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#zapise pohyb do zoznamu
                            if self.hra.ihrisko[y+iy*i][x+ix*i]==3 or self.hra.ihrisko[y+iy*i][x+ix*i]==4:
                                error+=1
                            if self.hra.ihrisko[y+iy*i][x+ix*i]==1 or self.hra.ihrisko[y+iy*i][x+ix*i]==2 or error==2:
                                if error>0:
                                    spisok.pop()#удаление хода из списка
                                break
            return spisok

        def prehlad_hodov_i2(self, spisok):#overi ostatne mozne nepovinne pohyby pre hraca
            for y in range(8):
                for x in range(8):
                    if self.hra.ihrisko[y][x]==1:
                        for ix,iy in (-1,-1),(1,-1):
                            if self.proti_hraca and self.f_hi:
                                ix, iy = -ix, -iy
                            if 0<=y+iy<=7 and 0<=x+ix<=7:
                                if self.hra.ihrisko[y+iy][x+ix]==0:
                                    spisok.append(((x,y),(x+ix,y+iy)))
                                elif self.hra.ihrisko[y+iy][x+ix]==3 or self.hra.ihrisko[y+iy][x+ix]==4:
                                    if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                        if self.hra.ihrisko[y+iy*2][x+ix*2]==0:
                                            spisok.append(((x,y),(x+ix*2,y+iy*2)))                 
                    elif self.hra.ihrisko[y][x]==2:
                        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                            error=0
                            for i in range(1,8):
                                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                                    if self.hra.ihrisko[y+iy*i][x+ix*i]==0:
                                        spisok.append(((x,y),(x+ix*i,y+iy*i)))
                                    if self.hra.ihrisko[y+iy*i][x+ix*i]==3 or self.hra.ihrisko[y+iy*i][x+ix*i]==4:
                                        error+=1
                                    if self.hra.ihrisko[y+iy*i][x+ix*i]==1 or self.hra.ihrisko[y+iy*i][x+ix*i]==2 or error==2:
                                        break
            return spisok

Dama = Main()

