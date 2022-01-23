"""
Automasjon av kabler og vern for ELE3002 og ELE3003.
Basert på NEK400:2018
TODO:
    Benytte pandas

Karl Odin Vold Røst

"""
import argparse as ap
import numpy as np
from pathlib import Path
import data
# GLOBAL DATA

class Kabel:
    """ 
    Her kan all data som deles for hver instans stå.
    """
    vern        = data.vern
    karakter_i2 = data.karakter_i2
    luft        = data.luft
    jord        = data.jord
    kfaktor_nf  = data.kfaktor_nf
    rim         = data.rim
    areal       = data.Areal

    def __init__(self, power=2200, volt=230, cosfi=1, faser=2, kar="C", RIM="A2", n=1,
            temp=25, norm="B", krav="B", s=None, i2=None, arr=None):

        self.power  = power
        self.volt   = volt
        self.cosfi  = cosfi
        self.faser  = faser      # Antall elektriske faser på kurs/forbruker
        self.kar    = kar        # Utløser karakteristikk --> Kabel.karakter_i2[self.kar] = i2koeffisient
        self.RIM    = RIM        # Referanseinstallasjonsmetode
        self.n      = n          # Nærføring
        self.temp   = temp       # Omgivelses temperatur
        self.norm   = norm       # Bolignorm/Industrinorm
        self.vern   = s          # Custom vern
        self.i2     = i2         # Custom i2 - koeffisient
        self.arr    = arr        # Arangemang av kabellegging
        self.krav   = krav

        # Følgende blir ikke gitt som argument
        self._ib    = None              # I_b --> Belastningstrøm
        self._in    = None              # I_n --> Nominell strøm 
        self._i2    = None              # I_2 --> timesstrøm
        self._kt    = None              # Korreksjonsfaktor temperatur.
        self._kn    = None              # Korreksjonsfaktor nærføring.
        self._iz    = None
        self._iz_min = None
        self._areal = None              # Kabeltverrsnitt

    def _recalc(*args):
        """
        Denne skal kunne justere hvem metoder som kalles for å justere algoritmen
        basert på hvilke argumenter som (ikke default) gis av input
        """
        pass


    def __call__(self, *args, **kwargs):
        """
        Argument parser goes here
        """
        parser = ap.ArgumentParser(description="Velkommen til Kabler og Vern!")
        parser.add_argument("Effekt", type=float, help="Hvor mange Watt bruker kursen")
        parser.add_argument("metode", type=str, choices=Kabel.rim.keys(), help="Referanseinstallasjonsmetode")
    #    parser.add_argument("metode", type=str, choices=rim.keys(), help="Referanseinstallasjonsmetode")
        pass


    def i_b(self):  #P, U=230, cosfi=1, fas=2)
        # DONE: OOP-ready
        # TODO: Make real documentation
        #       Write error handeling: What if self.faser is nonsense? Like -1 or 8
         """ 
         Funksjonen kalkulerer belastningsstrøm Ib
         Vurder hvordan argumentene skal håndteres, vi vill ikke at de gamle defaults
         skal overskrive gitte verdier:
         Argumneter nødvendig:
         self.power
         self.volt
         self.cosfi
         self.faser
         
         """
         if self.faser == 3:
             self._ib = self.power/(self.volt * self.cosfi * np.sqrt(3))
         else:
             self._ib = self.power/(self.volt * self.cosfi)

    def i_n(self):
        # DONE: OOP-ready
        # TODO: Write proper documentation
        #       Write error handeling
        #       This should maybe also be two methods
        """
        Denne metoden finner self._in (Nominell strøm) og self._i2 gjennom i2 koeffisienten i 
        dictionaryen; Kabel.karakter_i2 eller i den custome koeffisienten i self.i2.
        """
        # Case if i2 is not given, we will select from the standars in MHB.
        if self.i2 == None:
            # elif self.kar == "effektbryter" or "Effektbryter" or "Eff":
            if self.kar == "eff":
                if self._ib > 63:
                    i2_koeff = Kabel.karakter_i2[self.kar]["hi"]
                else:
                    i2_koeff = Kabel.karakter_i2[self.kar]["lo"]
            else:
                i2_koeff = Kabel.karakter_i2[self.kar]
        else:
            i2_koeff = self.i2

        if self.vern is None:
            # Selects the first value in Kabel.vern that is greater than self._ib
            self._in = Kabel.vern[np.argmax(Kabel.vern > self._ib)]
        else:
            self._in = self.vern

        self._i2 = self._in * i2_koeff


#    def kfaktor(RIM, n=1, temp=25, arr=None):
    def _korreksjons_faktor(self):
        # DONE: OOP-ready
        # Vil hente data ut ifra csv filer
        # self._kt
        # self._kn
        # TODO: Trenger 
        """
        self.RIM - Refereanseinstalsjonsmetode   -   string
            "A1", "A2", "B1" ....

        self.n - Antall kabler inntil            -   int
            (Nærføring)
        self.temp - Omgivelses temperatur i C    -   int
        
        Returns:    korreksjonsfaktorer k_
            self._kt, self._kn

        Foreløpig kun implementert for  PVC
        """
        temp_array = np.arange(10, 65, 5)
        fl = "luft"                         # Placeholder for å ikke inkludere alle scenarioer
        

        if self.RIM != "D2":
            fl = "luft"
        
        if fl == "luft":
            self._kt = Kabel.luft[np.where(temp_array == self.temp)[0][0]]
        elif fl == "jord":
            self._kt = Kabel.jord[np.where(temp_array == self.temp)[0][0]]
        else:
            print("0")          #?

        if self.RIM == "C":
            self._kn = Kabel.kfaktor_nf[1, self.n-1]/100 
        elif self.arr == "tak": 
           self._kn = Kabel.kfaktor_nf[2, self.n-1]/100
        else:
            self._kn = Kabel.kfaktor_nf[0, self.n-1]/100

    
    # def iz(In, key="A2",faser=2, nf=1, temp=25, arr=None):
    def i_z(self):
        # DONE: OOP-ready
        # TODO: Write proper documentation
        #       Write error handeling
        #       This should be split into several 
        """
        Funkjonene tar en av referanseinstallasjonsmetodene fra tabell 6.2b
        i MHB s.207 og kryssreferer verdien med Arealet fra første kollone
        """
        self._korreksjons_faktor() 
     
        faser = self.faser-2
        self._iz_min = self._in/(self._kt * self._kn)
        cross_index = lambda RIM, iz_min, faser: np.argmax(Kabel.rim[RIM][:,faser] >= iz_min)
        index = cross_index(self.RIM, self._iz_min, faser)
        self._avlest = Kabel.rim[self.RIM][index, faser] 
        self._iz = self._avlest * self._kt * self._kn
        self._areal = Kabel.areal[index] 




#    def bnz(Ib, In, Iz, I2, krav="B"):
    def _bnz(self):
        # DONE: OOP-ready
        # TODO: Write proper documentation
        #       Write error handeling
        #       Needs to check for Area if boilgkrav
        if self.krav == "B":
            self._msg0 = "Boligkrav"
            if self._ib <= self._in:
                self._msg1 = "OK!"
            else:
                self._msg1 = "IKKE OK!"
            if self._i2 <= self._iz:
                self._msg2 = "OK!"
            else:
                self._msg2 = "IKKE OK!"
        if self.krav == "I":
            self._msg0 = "Industrikrav"
            if self._ib <= self._in <= self._iz:
                self._msg1 = "OK!"
            else:
                self._msg1 = "IKKE OK!"
            if self._i2 <= self._iz*1.45:
                self._msg2 = "OK!"
            else:
                self._msg2 = "IKKE OK!"
        # Silly placeholder error handeling
        elif self.krav != "B" or "I":
            self._msg1 = "WRONG"
            self._msg2 = "WRONG"


    def __str__(self):
        # Kan ikke returnere pint metoden
        """
        Printer Kabler og Vern
        """
        self._bnz()
        string = ("=====================================================\n"
            f"En kurs med {self.power}W total effekt, {self.faser}-fas og {self.volt}V\n"
            f"Ib = {self._ib:.2f}A\n"
            f"In = {self._in}A\n"
            f"I2 = {self._i2:.2f}A\n"
            f"kt = {self._kt}\n"
            f"kn = {self._kn}\n"
            f"Iz_min = {self._iz_min:.2f}A\n"
            f"Iz_avlest = {self._avlest}A\n"
            f"Tverrsnitt = {self._areal}mm2\n"
            f"Iz = {self._iz:.2f}A\n"
            f"Vernet er en {self.faser}X{self._in}A {self.kar}-kar, forlagt med RIM={self.RIM}\n"
            f"{self._msg0} 1) {self._msg1}, 2) {self._msg2}\n")
#            if self.krav == "I":
#                f"Iz * 1,45 = {self._iz*1.45}\n")
        return string
        


if __name__ == '__main__':
    pass
    #main()
