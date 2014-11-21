# -*- coding: utf-8 -*-
import urllib2 
import re




def dohvatiPodatke(izvori):
    
    if type(izvori) is not list:
        
        return False;
    
    rezultati = []
    
    for izvor in izvori:
        
        rezultati.append(dohvatiSadrzaj(izvor))

    
    if len(rezultati) > 1:
        
        return rezultati
        
    else:
        
        return rezultati[0]
    

def dohvatiSadrzaj(adresa):

    return sortirajSadrzaj(urllib2.urlopen(adresa).read().decode("utf8"))
    
    
def sortirajSadrzaj(datoteka):
    
    rezultati = dict()
    
    postaje = re.findall(r'<tr (.*?) align="center">(.*?)</tr>', datoteka, re.M|re.I|re.S)
      
    for postaja in postaje[1:]: 
        
        naziv_postaje = re.findall(r'<td align="left">&nbsp;(.*?)</td>', postaja[1].strip(), re.M|re.I|re.S) # u [0]
        podaci = re.findall(r'<td>(.*?)</td>', postaja[1].strip(), re.M|re.I|re.S)
        
        # smjer vjetra, brzina vjetra, temperatura, relativna vlaznost, tlak zraka, tendencija tlaka, vrijeme
        rezultati[naziv_postaje[0]] = {'smjer_vjetra': podaci[0], 'brzina_vjetra': podaci[1], 'temperatura_zraka': podaci[2],'relativna_vlaznost': podaci[3], 'tlak_zraka': podaci[4], 'tendencija_tlaka': (re.findall(r'<font (.*?)>(.*?)</font>', podaci[5], re.M|re.I|re.S)[0][1]), 'vrijeme': podaci[6] }
        
    return rezultati


# temperatura zraka u Senju u 06h, 08h i 12h
for podatak in dohvatiPodatke(['http://vrijeme.hr/aktpod.php?id=hrvatska_n&param=06', 'http://vrijeme.hr/aktpod.php?id=hrvatska_n&param=08', 'http://vrijeme.hr/aktpod.php?id=hrvatska_n&param=12']):
    
    print podatak['Senj']['temperatura_zraka']
    
#temperatura zraka u Zagrebu sad
print dohvatiPodatke(['http://vrijeme.hr/aktpod.php?id=hrvatska_n'])['Zagreb-aer']['temperatura_zraka']