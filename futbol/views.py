from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def classificacio_menu(request):
	#fem directament el queryset
	queryset= Lliga.objects.all()
	return render(request, "classificacio_menu.html",
		{"lligues":queryset})

def classificacio(request, lliga_id):
    lliga = Lliga.objects.get(id=lliga_id)
    equips = lliga.equips.all()
    classi = []
 
    # calculem punts en llista de tuples (equip,punts)
    for equip in equips:
        punts = 0
        for partit in lliga.partits.filter(local=equip):
            if partit.gols_local() > partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1
        for partit in lliga.partits.filter(visitant=equip):
            if partit.gols_local() < partit.gols_visitant():
                punts += 3
            elif partit.gols_local() == partit.gols_visitant():
                punts += 1

        # si posem tupla, s'ordenarà pel primer dels criteris
        # en aquest cas, per punts(no per nom de l'equip)
        classi.append( (punts,equip.nom) )
    # ordenem llista
    classi.sort(reverse=True)
    return render(request,"classificacio.html",
                {
                    "classificacio":classi,
                })

