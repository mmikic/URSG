# -*- coding: utf-8 -*-
import urllib2 
import re

"""

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
        

    def postajaPodaci(self, postaja):
        
        return self.podaci.get(postaja, "Nisu dostupni podaci o postaji")
    
    
    def postajaPodatak(self, postaja, podatak):
        
        if self.podaci.get(postaja, False) == False:
            
            return "Nisu dostupni podaci o postaji"
            
        else:
            
            return self.podaci[postaja][podatak]
        
        
    def dohvatiPodatke(self, izvor):
    
        self.podaci = self.dohvatiSadrzaj(izvor)
        

    def dohvatiSadrzaj(self, adresa):

        return self.sortirajSadrzaj(urllib2.urlopen(adresa).read().decode("utf8"))
    
    
    def puz(self, tekst):
        
        tekst = unicode(tekst).lower()
        tekst = tekst.replace(unicode('č', errors="ignore"), unicode('c', errors="ignore"))
        tekst = tekst.replace(unicode('ć', errors="ignore"), unicode('c', errors="ignore"))
        tekst = tekst.replace(unicode('š', errors="ignore"), unicode('s', errors="ignore"))
        tekst = tekst.replace(unicode('ž', errors="ignore"), unicode('z', errors="ignore"))
        tekst = tekst.replace(unicode('đ', errors="ignore"), unicode('d', errors="ignore"))
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
        
        for x in rezultati:
            
            print x
            
        #return rezultati


meteo = MeteoHR("http://vrijeme.hr/aktpod.php?id=hrvatska_n&param=07")

print meteo.postajaPodatak("crni-lug-np-risnjak", "temperatura_zraka")
print meteo.postajaPodatak("hr-kostajnica", "temperatura_zraka")
print meteo.postajaPodatak("gradiste-zupanja", "temperatura_zraka")