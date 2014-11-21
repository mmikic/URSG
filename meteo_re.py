# -*- coding: utf-8 -*-
import urllib2 
import re

def dohvatiPodatke():
    
    izvori = ['http://vrijeme.hr/aktpod.php?id=hrvatska_n']


def dohvatiSadrzaj(adrese):

    mjerenja = []

    for adresa in adrese:
        
        mjerenja.append(sortirajSadrzaj(urllib2.urlopen(adresa).read().decode("utf8")))
    
    return mjerenja
    
    
def sortirajSadrzaj(datoteka):
    
    rezultati = dict()
    
    postaje = re.findall(r'<tr bgcolor="(.*?)" align="center">(.*?)</tr>', datoteka, re.M|re.I|re.S)    
    for postaja in dokument[1:]: 
        
        naziv_postaje = re.findall(r'<td align="left">&nbsp;(.*?)</td>', postaja[1].strip(), re.M|re.I|re.S) # u [0]
        podaci = re.findall(r'<td>(.*?)</td>', postaja[1].strip(), re.M|re.I|re.S)
        
        # smjer vjetra, brzina vjetra, temperatura, relativna vlaznost, tlak zraka, tendencija tlaka, vrijeme
        rezultati[naziv_postaje[0]] = {'smjer_vjetra': podaci[0], 'brzina_vjetra': podaci[1], 'temperatura_zraka': podaci[2],'relativna_vlaznost': podaci[3], 'tlak_zraka': podaci[4], 'tendencija_tlaka': podaci[5] }
        
    return rezultati
    

podaci = dohvatiPodatke()

print podaci[0]['Zagreb-aer']