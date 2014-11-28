# -*- coding: utf-8 -*-
import urllib2 
import re

"""

postajaPodatak(postaja, podatak)

    Vrijednosti argumenta postaja je ime postaje malim slovima, razmak pretvoren u -, bez dijakritika
    
        npr.
        Gorice-Nova Gradiška    "gorice-nova-gradiska"
        Zagreb Grič             "zagreb-gric"
        
        dodatno, moguce je za sljedece gradove samo upisati ime grada i dobiti prvi rezultat vezan
        
        npr.
        "zagreb"        > "zagreb gric" ako je dostupno, inace "zagreb-maksimir" ako je dostupno, inace "zagreb-aerodrom" 
        
        popis gradova:
        Zagreb
        Split
        Zadar
        Osijek
        Rijeka
        Pula
        Dubrovnik
    
    Naravno, ukoliko su podaci dostupni

    -------------

    Vrijednosti argumenta podatak:

        smjer_vjetra
        brzina_vjetra
        temperatura_zraka
        relativna_vlaznost
        tlak_zraka
        tendencija_tlaka
        vrijeme
    
--------------------------------------    
    
TO DO:

-   dokumentirati funkcije: istovarPodataka(), postajaPodatak(), postajaPodaci()
-   napisati funkciju datum() koja vadi datum i vrijeme podataka

-   ne postoji potreba za dohvatiSadrzaj(), trebalo bi napisati funkciju koja returna sadrzaj stranice bez da ga odmah poziva u nesto sljedece
    bilo bi dobro pohraniti podatke u neku varijablu i dalje se igrati s njom
-   kada se stvori funkcija za dohvacanje sadrzaja, onda je moguce napraviti datum() funkciju uz regex

"""

class MeteoHR:


    podaci = dict()
    izvor = ""

    def __init__(self, izvor="http://vrijeme.hr/aktpod.php?id=hrvatska_n"):
        
        self.izvor = izvor
        self.dohvatiPodatke(izvor)
    
    def istovarPodataka(self):
        
        return self.podaci
        

    def pretraziKljuc(self, kljuc):
        
        kljucevi = {
            kljuc: kljuc if kljuc in self.podaci else None,
            'zagreb': 'zagreb-gric' if 'zagreb-gric' in self.podaci else ('zagreb-maksimir' if 'zagreb-maksimir' in self.podaci else ('zagreb-aer' if 'zagreb-aer' in self.podaci else None)),
            'split': 'split' if 'split' in self.podaci else ('split-aer' if 'split-aer' in self.podaci else None),
            'rijeka': 'rijeka' if 'rijeka' in self.podaci else ('rijeka-aer' if 'rijeka-aer' in self.podaci else None),
            'pula': 'pula' if 'pula' in self.podaci else ('pula-aer' if 'pula-aer' in self.podaci else None),
            'zadar': 'zadar' if 'zadar' in self.podaci else ('zadar-aer' if 'zadar-aer' in self.podaci else None),
            'osijek': 'osijek' if 'osijek' in self.podaci else ('osijek-aer' if 'osijek-aer' in self.podaci else None),
            'dubrovnik': 'dubrovnik' if 'dubrovnik' in self.podaci else ('dubrovnik-aer' if 'dubrovnik-aer' in self.podaci else None)
        }
        
        return kljucevi[kljuc]
        

    def postajaPodaci(self, postaja):
        
        kljuc = self.pretraziKljuc(postaja)
        
        if kljuc == None: 
            
            return "Nisu dostupni podaci o postaji"
            
        else:
            
            return self.podaci[kljuc]
    
    
    def postajaPodatak(self, postaja, podatak):
        
        kljuc = self.pretraziKljuc(postaja)
        
        if kljuc == None:
            
            return "Nisu dostupni podaci o postaji"
            
        else:
            
            return self.podaci[kljuc][podatak]
        
        
    def dohvatiPodatke(self, izvor):
    
        self.podaci = self.dohvatiSadrzaj(izvor)
        

    def dohvatiSadrzaj(self, adresa):

        return self.sortirajSadrzaj(urllib2.urlopen(adresa).read().decode("utf8"))
    
    
    def puz(self, tekst):
        
        tekst = unicode(tekst).lower()
        
        tekst = tekst.replace('č'.decode("utf8"), 'c')
        tekst = tekst.replace('ć'.decode("utf8"), 'c')
        tekst = tekst.replace('š'.decode("utf8"), 's')
        tekst = tekst.replace('ž'.decode("utf8"), 'z')
        tekst = tekst.replace('đ'.decode("utf8"), 'd')
        
        tekst = re.sub(r'[^a-z0-9]+', '-', tekst)
        
        return tekst
        
        
    def datum(self):
        
        return True
        #<div class="sadrzajHeader-zuti"><img src="trokutic.gif">Vrijeme u Hrvatskoj 
    
    
    def sortirajSadrzaj(self, datoteka):
    
        rezultati = dict()
    
        postaje = re.findall(r'<tr (.*?) align="center">(.*?)</tr>', datoteka, re.M|re.I|re.S)
      
        for postaja in postaje[1:]: 
        
            naziv_postaje = re.findall(r'<td align="left">&nbsp;(.*?)</td>', postaja[1].strip(), re.M|re.I|re.S) # u [0]
            podaci = re.findall(r'<td>(.*?)</td>', postaja[1].strip(), re.M|re.I|re.S)
            
            # smjer vjetra, brzina vjetra, temperatura, relativna vlaznost, tlak zraka, tendencija tlaka, vrijeme
            rezultati[self.puz(naziv_postaje[0])] = {'smjer_vjetra': podaci[0], 'brzina_vjetra': podaci[1], 'temperatura_zraka': podaci[2], 'relativna_vlaznost': podaci[3], 'tlak_zraka': podaci[4], 'tendencija_tlaka': (re.findall(r'<font (.*?)>(.*?)</font>', podaci[5], re.M|re.I|re.S)[0][1]), 'vrijeme': podaci[6] }
            
        return rezultati


meteo = MeteoHR()

print meteo.postajaPodatak('dubrovnik', 'temperatura_zraka')
