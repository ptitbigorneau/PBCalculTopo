#!/usr/bin/python
# -*- coding: utf_8 -*- 

from __future__ import division
import math
from math import *
import os, sys
import wx
import wxPython.lib.dialogs
import decimal

def fstation(xorigine, yorigine, angle, test):

    if test == "xy": 
       
        Fichier = open('calculvo','w')
        Fichier.write(xorigine)
        Fichier.write("\n")
        Fichier.write(yorigine)
        Fichier.write("\n")
        Fichier.close()

    if test == "xynv": 
       
        Fichier = open('calculvo','w')
        Fichier.write(xorigine)
        Fichier.write("\n")
        Fichier.write(yorigine)
        Fichier.write("\n")
        Fichier.write(angle)
        Fichier.write("\n")
        Fichier.close()

    if test == "xya": 

        Fichier = open('calculvo','r')
        data = Fichier.readlines()
        Fichier.close()
        return data

def CalculXY(xo, yo, g, d):

    pi = 4 * atan(1)

    cg = g * pi / 200
    x = xo + d * sin(cg)
    y = yo + d * cos(cg)

    return x, y

def CalculGisement(X1, Y1, X2, Y2):

    dx = X2 - X1
    dy = Y2 - Y1
    dx2 = abs(dx * dx)
    dy2 = abs(dy * dy)
    d = sqrt(dx2 + dy2)

    if abs(dx) == 0 and abs(dy) == 0:
        t = 0

    elif abs(dx) == 0:
        t = abs(atan(dx / dy))

    elif abs(dy) == 0:
        t = abs(atan(dy / dx))

    elif abs(dx) >= abs(dy):
        t = abs(atan(dy / dx))

    elif abs(dx) < abs(dy):
        t = abs(atan(dx / dy))

    t = t * 200 / pi

    if abs(dx) == abs(dy):
        v = t
    elif abs(dy) > abs(dx) and dx < 0 and dy > 0:
        v = 400 - t
    elif abs(dy) > abs(dx) and dx >= 0 and dy > 0:
        v = t
    elif abs(dx) > abs(dy) and dx > 0 and dy > 0:
        v = 100 - t
    elif abs(dx) > abs(dy) and dx > 0 and dy <= 0:
        v = 100 + t
    elif abs(dy) > abs(dx) and dx > 0 and dy < 0:
        v = 200 - t
    elif abs(dy) > abs(dx) and dx <= 0 and dy < 0:
        v = 200 + t
    elif abs(dx) > abs(dy) and dx < 0 and dy < 0:
        v = 300 - t
    elif abs(dx) > abs(dy) and dx < 0 and dy >= 0:
        v = 300 + t

    return v

def CalculDH(distance, av):

    pi = 4 * atan(1)
    avr = av * pi / 200
    dh = sin(avr) * distance

    return dh

def CalculDN(distance, av):

    pi = 4 * atan(1)
    angle = 100 - av
    angler  = angle * pi / 200
    dn = sin(angler) * distance

    return dn

class CalculVODialog(wx.Dialog):
    
    def __init__(self, *args, **kw):
        super(CalculVODialog, self).__init__(*args, **kw) 
            
        self.InitUI()
        self.SetSize((350, 250))
        self.SetTitle("Calcul V0")
        
        
    def InitUI(self):

        xr = ""
        yr = ""
        angle = ""
        station = fstation("X", "Y", "ANGLE", "xya")
        self.xori = str(station[0])
        self.yori = str(station[1])

        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(10, 10)
        sizer = wx.GridBagSizer(5, 5)

        font = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(12, wx.NORMAL, wx.NORMAL, wx.BOLD)
        fontc = wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL)

        txref = wx.StaticText(panel, label=u"X Référence")
        sizer.Add(txref, pos=(1, 1), flag=wx.TOP, border=10)
        txref.SetFont(font)

        tyref = wx.StaticText(panel, label=u"Y Référence")
        sizer.Add(tyref, pos=(1, 2), flag=wx.TOP, border=10)
        tyref.SetFont(font)
        
        self.tangle = wx.StaticText(panel, label="AH")
        sizer.Add(self.tangle, pos=(1, 3), flag=wx.TOP, border=10)
        self.tangle.SetFont(font)

        self.xref = wx.TextCtrl(panel, value=xr, size =(100,25))
        sizer.Add(self.xref, pos=(2, 1),flag=wx.TOP, 
            border=5)
        self.yref = wx.TextCtrl(panel, value=yr, size =(100,25))
        sizer.Add(self.yref, pos=(2, 2),flag=wx.TOP, 
            border=5)

        self.angle = wx.TextCtrl(panel, value=angle, size =(100,25))
        sizer.Add(self.angle, pos=(2, 3),flag=wx.TOP, 
            border=5)
        
        buttoncalvo = wx.Button(panel, 1, label="Calculer")
        sizer.Add(buttoncalvo, pos=(4, 1),span=(1,1),flag=wx.TOP|wx.RIGHT, border=5) 

        buttonclose = wx.Button(panel,2, label="Quitter")
        sizer.Add(buttonclose, pos=(4, 2),span=(1,1),flag=wx.TOP|wx.RIGHT, border=5) 

        sizer.AddGrowableCol(5)
        
        panel.SetSizer(sizer)
        panel.SetBackgroundColour("#f0f0f0") 
        self.Show(True)

        self.Bind(wx.EVT_BUTTON, self.Calcul, id=1)
        self.Bind(wx.EVT_BUTTON, self.Close, id=2)

    def Close(self, e):
        
        self.Destroy()

    def Calcul(self, e):

        if self.xref.GetValue()=="" or self.yref.GetValue() =="" or self.angle.GetValue()=="":

            wx.MessageBox("Erreur !", "Erreur !", wx.OK | wx.ICON_ERROR)
            self.Destroy()
            return
        
        try:

            xo = float(self.xori)
            yo = float(self.yori)
            xr = float(self.xref.GetValue())
            yr = float(self.yref.GetValue())
            angle = float(self.angle.GetValue())

        except:

            wx.MessageBox("Erreur !", "Erreur !", wx.OK | wx.ICON_ERROR)
            self.Destroy()
            return

        v = float(CalculGisement(xo, yo, xr, yr))

        v0 = v - angle

        message = ("Gisement: %s\n\nV0: %s"%(v, v0))
        wx.MessageBox(message, "V0", wx.OK | wx.ICON_INFORMATION)
        self.Destroy()

        fstation(str(xo), str(yo), str(v0), "xynv")

class Myframe(wx.Frame):

    def __init__(self, titre):    

        wx.Frame.__init__(self, None, -1, title = titre, size=(700,650))
        
        self.InitUI()
        self.Centre()
        self.Show()     

    def InitUI(self):

        xo = ""
        yo = ""
        zo = ""
        ht = ""
        hv = ""
        v = ""
        vo = "0"
        d = ""
        av=""
        self.testd = 'dh'
        self.testz = 'xy'

        menuFichier = wx.Menu(style = wx.MENU_TEAROFF) 
        menuFichier.Append(wx.ID_COPY, "&Copier\tAlt+C", "Copier dans le Presse-Papier")
        menuFichier.Append(wx.ID_CANCEL, "&Effacer\tAlt+E", "Effacer les données") 
        menuFichier.Append(wx.ID_EXIT, "&Quitter\tAlt+Q", "Quitter PBCalculTopo") 

        menuHelp = wx.Menu()
        menuHelp.Append(wx.ID_ABOUT, "A propos","A propos de CalculTopo")

        menuBarre = wx.MenuBar() 
        menuBarre.Append(menuFichier, "&Fichier")
        menuBarre.Append(menuHelp, "?")

        self.barre = wx.StatusBar(self, -1) 
        self.barre.SetFieldsCount(2) 
        self.barre.SetStatusWidths([-1, -1]) 

        self.SetStatusBar(self.barre)

        self.SetMenuBar(menuBarre)        

        panel = wx.ScrolledWindow(self)
        panel.SetScrollRate(10, 10)
        sizer = wx.GridBagSizer(5, 5)

        font = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.BOLD)
        font2 = wx.Font(12, wx.NORMAL, wx.NORMAL, wx.BOLD)
        fontc = wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL)

        text1 = wx.StaticText(panel, label="PBCalculTopo")
        sizer.Add(text1, pos=(0, 0), span=(1,2), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=20)
 
        icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('topo.gif'))
        sizer.Add(icon, pos=(0, 5), flag=wx.TOP|wx.RIGHT|wx.ALIGN_RIGHT, 
            border=5)
        font3 = wx.Font(14, wx.NORMAL, wx.NORMAL, wx.BOLD)
        text1.SetFont(font3)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1, 0), span=(1, 6), 
            flag=wx.EXPAND|wx.BOTTOM, border=10)
        
        self.radio3 = wx.RadioButton( panel, label = "XY", style = wx.RB_GROUP )
        sizer.Add(self.radio3, pos=(2, 1),flag=wx.TOP, border= 10)
        self.radio3.SetFont(fontc)

        self.radio4 = wx.RadioButton( panel, label = "XYZ")
        sizer.Add(self.radio4, pos=(3, 1))
        self.radio4.SetFont(fontc)

        self.radio1 = wx.RadioButton( panel, label = "Distance Horizontale", style = wx.RB_GROUP )
        sizer.Add(self.radio1, pos=(2, 2),flag=wx.TOP, border= 10)
        self.radio1.SetFont(fontc)

        self.radio2 = wx.RadioButton( panel, label = "Distance Verticale")
        sizer.Add(self.radio2, pos=(3, 2))
        self.radio2.SetFont(fontc)

        txorigine = wx.StaticText(panel, label="X Station")
        sizer.Add(txorigine, pos=(4, 1), flag=wx.TOP, border=10)
        txorigine.SetFont(font)

        tyorigine = wx.StaticText(panel, label="Y Station")
        sizer.Add(tyorigine, pos=(4, 2), flag=wx.TOP, border=10)
        tyorigine.SetFont(font)
        
        self.tzorigine = wx.StaticText(panel, label="Z Station")
        sizer.Add(self.tzorigine, pos=(4, 3), flag=wx.TOP, border=10)
        self.tzorigine.SetFont(font)

        self.tht = wx.StaticText(panel, label="Hauteur Tourillon ")
        sizer.Add(self.tht, pos=(4, 4), flag=wx.TOP, border=10)
        self.tht.SetFont(font)

        self.xorigine = wx.TextCtrl(panel, value=xo, size =(100,25))
        sizer.Add(self.xorigine, pos=(5, 1),flag=wx.TOP, 
            border=5)
        self.yorigine = wx.TextCtrl(panel, value=yo, size =(100,25))
        sizer.Add(self.yorigine, pos=(5, 2),flag=wx.TOP, 
            border=5)

        self.zorigine = wx.TextCtrl(panel, value=zo, size =(100,25))
        sizer.Add(self.zorigine, pos=(5, 3),flag=wx.TOP, 
            border=5)

        self.ht = wx.TextCtrl(panel, value=ht, size =(100,25))
        sizer.Add(self.ht, pos=(5, 4),flag=wx.TOP, 
            border=5)
        
        self.tvo = wx.StaticText(panel, label=u'V0')
        sizer.Add(self.tvo, pos=(6, 1), flag=wx.TOP, border=10)
        self.tvo.SetFont(font)        

        self.vo= wx.TextCtrl(panel, value= vo, size =(100,25))
        sizer.Add(self.vo, pos=(7, 1),flag=wx.TOP, 
            border=5)

        buttoncalvo = wx.Button(panel, 1, label="Calcul V0")
        sizer.Add(buttoncalvo, pos=(7, 2),span=(1,1),flag=wx.TOP|wx.RIGHT, border=5) 

        tgisement = wx.StaticText(panel, label='Ah')
        sizer.Add(tgisement, pos=(8, 1), flag=wx.TOP, border=10)
        tgisement.SetFont(font)
        self.tdistance = wx.StaticText(panel, label='Dh')
        sizer.Add(self.tdistance, pos=(8, 2), flag=wx.TOP, border=10)
        self.tdistance.SetFont(font)

        self.tav = wx.StaticText(panel, label="Av")
        sizer.Add(self.tav, pos=(8, 3), flag=wx.TOP, border=10)
        self.tav.SetFont(font)
        self.av = wx.TextCtrl(panel, value= av, size =(100,25))
        sizer.Add(self.av, pos=(9, 3),flag=wx.TOP, border=5)

        self.thv = wx.StaticText(panel, label="Hauteur voyant")
        sizer.Add(self.thv, pos=(8, 4), flag=wx.TOP, border=10)
        self.thv.SetFont(font)
        self.hv = wx.TextCtrl(panel, value= hv, size =(100,25))
        sizer.Add(self.hv, pos=(9, 4),flag=wx.TOP, border=5)

        self.gisement = wx.TextCtrl(panel, value=v, size =(100,25))
        sizer.Add(self.gisement, pos=(9, 1),flag=wx.TOP, 
            border=5)
        self.distance = wx.TextCtrl(panel, value=d, size =(100,25))
        sizer.Add(self.distance, pos=(9, 2),flag=wx.TOP, 
            border=5)

        buttonenvoyer = wx.Button(panel,2, label="Calcul")
        sizer.Add(buttonenvoyer, pos=(9, 5),span=(1,1),flag=wx.TOP|wx.RIGHT, border=5) 

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(11, 0), span=(1, 6), 
            flag=wx.EXPAND, border=10)

        texte1 = wx.StaticText(panel, label="Liste points")
        sizer.Add(texte1, pos=(12, 1), flag=wx.TOP|wx.LEFT, border=10)
        texte1.SetFont(font)

        self.text5=wx.TextCtrl(panel, value="",style = wx.TE_READONLY|wx.TE_MULTILINE, size =(350,100))
        sizer.Add(self.text5, pos=(13, 1),span=(6,4), flag=wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)

        buttoncopy = wx.Button(panel,3, label="Copier")
        sizer.Add(buttoncopy, pos=(13, 5),span=(1,1),flag=wx.TOP|wx.RIGHT, border=5)

        buttonreset = wx.Button(panel,4, label="Reset")
        sizer.Add(buttonreset, pos=(14, 5),span=(1,1),flag=wx.TOP|wx.RIGHT, border=5)

        self.radio1.Bind(wx.EVT_RADIOBUTTON, self.onbouton)
        self.radio2.Bind(wx.EVT_RADIOBUTTON, self.onbouton)

        self.radio3.Bind(wx.EVT_RADIOBUTTON, self.onbouton)
        self.radio4.Bind(wx.EVT_RADIOBUTTON, self.onbouton)

        sizer.AddGrowableCol(5)
        
        panel.SetSizer(sizer)
        panel.SetBackgroundColour("#f0f0f0") 
        self.Show(True)
            
        self.tzorigine.SetLabel('')
        self.zorigine.Hide()
        self.tht.SetLabel('')
        self.ht.Hide()        
        self.tav.SetLabel('')
        self.av.Hide() 
        self.thv.SetLabel('')
        self.hv.Hide()

        self.Bind(wx.EVT_BUTTON, self.Calculvo, id=1)
        self.Bind(wx.EVT_BUTTON, self.Calcul, id=2)
        self.Bind(wx.EVT_BUTTON, self.Copier, id=3)
        self.Bind(wx.EVT_BUTTON, self.Reset, id=4)

        wx.EVT_MENU(self, wx.ID_COPY, self.Copier)
        wx.EVT_MENU(self, wx.ID_CANCEL, self.Reset)
        wx.EVT_MENU(self, wx.ID_EXIT, self.Quit)
        wx.EVT_MENU(self, wx.ID_ABOUT, self.About)
   
    def onbouton(self, event):

        btn = event.GetEventObject()
        label = btn.GetLabel()

        if label == "XYZ":

            self.testz="xyz"

            if  self.radio1.GetValue() == True:

                self.testd="dv"
                self.tzorigine.SetLabel('Z Station')
                self.zorigine.Show()
                self.tht.SetLabel('Hauteur Tourillon')
                self.ht.Show()        
                self.radio1.SetValue(False)
                self.radio2.SetValue(True)
                self.tav.SetLabel('Av')
                self.tdistance.SetLabel('Dv')
                self.av.Show() 
                self.thv.SetLabel('Hauteur Voyant')
                self.hv.Show() 
                event.Skip()

            elif  self.radio2.GetValue() == True:

                self.tzorigine.SetLabel('Z Station')
                self.zorigine.Show()
                self.tdistance.SetLabel('Dv')
                self.tht.SetLabel('Hauteur Tourillon')
                self.ht.Show()        
                self.thv.SetLabel('Hauteur Voyant')
                self.hv.Show() 
                event.Skip()

        if label == 'XY':

            self.testz="xy"

            if self.radio2.GetValue() == True:

                self.testd="dh"
                self.tzorigine.SetLabel('')
                self.zorigine.Hide()
                self.tht.SetLabel('')
                self.ht.Hide()        
                self.tav.SetLabel('')
                self.av.Hide()
                self.tdistance.SetLabel('Dh')
                self.thv.SetLabel('')
                self.hv.Hide()
                self.radio2.SetValue(False)
                self.radio1.SetValue(True)
                event.Skip()

            elif self.radio1.GetValue() == True:

                self.tav.SetLabel('')
                self.av.Hide() 
                self.tzorigine.SetLabel('')
                self.zorigine.Hide()
                self.tht.SetLabel('')
                self.ht.Hide()        
                self.tdistance.SetLabel('Dh')
                self.thv.SetLabel('')
                self.hv.Hide()
                event.Skip()

        if label == "Distance Horizontale":

            self.testd="dh"

            if self.radio3.GetValue() == True:
            
                self.tav.SetLabel('')
                self.av.Hide() 
                self.tdistance.SetLabel('Dh')
                event.Skip()

            elif self.radio4.GetValue() == True:
            
                self.tdistance.SetLabel('Dh')
                event.Skip()
        
        if label == "Distance Verticale":

            self.testd="dv"

            self.tdistance.SetLabel('Dv')
            self.tav.SetLabel('Av')
            self.av.Show() 
            event.Skip()

    def Quit(self, evt):

        os.remove('calculvo')
        self.Destroy()

    def Calcul(self, evt):

        xori = self.xorigine.GetValue()
        yori = self.yorigine.GetValue()
        vo = self.vo.GetValue()
        ah = self.gisement.GetValue()
        distance = self.distance.GetValue()
        zo = self.zorigine.GetValue()
        ht = self.ht.GetValue()
        hv = self.hv.GetValue()
        av = self.av.GetValue()

        try:

            xori = float(xori)
            yori = float(yori)
            vo = float(vo)
            ah = float(ah)
            distance = float(distance)

        except:

            wx.MessageBox("Erreur !", "Erreur !", wx.OK | wx.ICON_ERROR)
            return

        g = ah + vo

        if g > 400:

            g = g - 400

        if g < 0:

            g = g + 400

        if self.testd == "dv":

            try:

                av = float(av)

            except:

                wx.MessageBox("Erreur !", "Erreur !", wx.OK | wx.ICON_ERROR)
                return
            
            distance = CalculDH(distance, av)

        else:

            av = 100

        if self.testz == "xy":

            resultat = CalculXY(xori, yori, g, distance)

            x=resultat[0]
            y=resultat[1]

            x= round(x,5)
            y= round(y,5)

            recu =  "x=" + str(x) + " y=" + str(y) + "\n\n" + self.text5.GetValue()

            self.text5.SetValue(recu)
            evt.Skip()

        if self.testz == "xyz":
            
            try:

                zo = float(zo)
                ht = float(ht)
                hv = float(hv)

            except:

                wx.MessageBox("Erreur !", "Erreur !", wx.OK | wx.ICON_ERROR)
                return

            rdn = CalculDN(distance, av)

            z = zo + ht + rdn - hv

            resultat = CalculXY(xori, yori, g, distance)

            x=resultat[0]
            y=resultat[1]

            x= round(x,5)
            y= round(y,5)
            z= round(z,5)

            recu =  "x=" + str(x) + " y=" + str(y) + " Z=" + str(z) +"\n\n" + self.text5.GetValue()

            self.text5.SetValue(recu)
            evt.Skip()


    def Calculvo(self, evt):

        xori = self.xorigine.GetValue()
        yori = self.yorigine.GetValue()

        try:

            testxori = float(xori)
            testyori = float(yori)
           
        except:

            wx.MessageBox("Erreur !", "Erreur !", wx.OK | wx.ICON_ERROR)
            return 

        fstation(xori, yori, "ANGLE", "xy")

        calculvo = CalculVODialog(None, 
            title='Calcul V0')
        calculvo.ShowModal()
        calculvo.Destroy() 

        resultat = fstation(xori, yori, "ANGLE", "xya")

        if len(resultat) != 3:
             return

        self.vo.SetValue(resultat[2])
        evt.Skip()

    def Copier(self, evt):

        if self.text5.GetValue() == '':
            wx.MessageBox(u"Aucune Donnée a copier", "Erreur !", wx.OK | wx.ICON_ERROR)

        else:

            self.dataObj = wx.TextDataObject()
            self.dataObj.SetText(self.text5.GetValue())

            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(self.dataObj)
                wx.TheClipboard.Close()
                wx.MessageBox(u"Données copiées le Presse-papiers", "Presse-papiers", wx.OK | wx.ICON_INFORMATION)
        
            else:
                wx.MessageBox(u"Impossible d'ouvrir le Presse-papiers", "Erreur !", wx.OK | wx.ICON_ERROR)

    def Reset(self, evt):

        self.text5.SetValue('')
        evt.Skip()

    def About(self, evt):

        description = u"Calcul Topométrique ( Python 2.7, wxPython )"
       
        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO))
        info.SetName('PBCalculTopo')
        info.SetVersion('beta1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2012 PtitBigorneau')
        info.SetWebSite('http://www.ptitbigorneau.fr')
             
        wx.AboutBox(info)

if __name__ == '__main__':

    app = wx.App()
    frame=Myframe(titre="PBCalculTopo")
    icone = wx.Icon("./icone.ico", wx.BITMAP_TYPE_ICO)

    frame.SetIcon(icone)
    frame.Show()

    app.MainLoop()

