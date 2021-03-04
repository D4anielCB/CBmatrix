# -*- coding: utf-8 -*-
import sys, xbmcplugin ,xbmcgui, xbmcaddon, xbmc, os, json, hashlib, re, math, html
#htmlentitydefs
from urllib.parse import urlparse, quote_plus
from urllib.request import urlopen, Request
import urllib.request, urllib.parse, urllib.error
import urllib.parse

Versao = "21.03.04"

AddonID = 'plugin.video.CubePlay'
Addon = xbmcaddon.Addon(AddonID)
AddonName = Addon.getAddonInfo("name")
addonDir = Addon.getAddonInfo('path')
icon = os.path.join(addonDir,"icon.png")

iconsDir = os.path.join(addonDir, "resources", "images")

libDir = os.path.join(addonDir, 'resources', 'lib')
sys.path.insert(0, libDir)
#import common

addon_data_dir = xbmc.translatePath(Addon.getAddonInfo("profile"))
cacheDir = os.path.join(addon_data_dir, "cache")
if not os.path.exists(cacheDir):
	os.makedirs(cacheDir)

cadulto = Addon.getSetting("cadulto")
cPage = Addon.getSetting("cPage") # dublado redecanais
cPageleg = Addon.getSetting("cPageleg")
cPagenac = Addon.getSetting("cPagenac")
cPagelan = Addon.getSetting("cPagelan")
cPageser = Addon.getSetting("cPageser")
cPageani = Addon.getSetting("cPageani")
cPagenov = Addon.getSetting("cPagenov")
cPagedes = Addon.getSetting("cPagedes")
cPagefo1 = Addon.getSetting("cPagefo1")
cPageMMf = Addon.getSetting("cPageMMf")
cPageGOf = Addon.getSetting("cPageGOf")

cPageFNC = Addon.getSetting("cPageFNC") #paginacao Filmes Netcine

cPageserSF = Addon.getSetting("cPageserSF")

cEPG = Addon.getSetting("cEPG")
cOrdFO = "date" if Addon.getSetting("cOrdFO")=="0" else "title"
cOrdRCF = "date" if Addon.getSetting("cOrdRCF")=="0" else "title"
cOrdRCS = "date" if Addon.getSetting("cOrdRCS")=="0" else "title"
cOrdNCF = Addon.getSetting("cOrdNCF")
cOrdNCS = Addon.getSetting("cOrdNCS")

cPlayD = Addon.getSetting("cPlayD") #play

Cat = Addon.getSetting("Cat")
Catfo = Addon.getSetting("Catfo")
CatMM = Addon.getSetting("CatMM")
CatGO = Addon.getSetting("CatGO")

cSIPTV = Addon.getSetting("cSIPTV")

Clista=[ "todos",                     "acao", "animacao", "aventura", "comedia", "drama", "fantasia", "ficcao-cientifica", "romance", "suspense", "terror"]
Clista2=["Sem filtro (Mostrar Todos)","Acao", "Animacao", "Aventura", "Comedia", "Drama", "Fantasia", "ficcao-cientifica", "Romance", "Suspense", "Terror"]
Clista3=["Sem filtro (Mostrar Todos)","Ação", "Animação", "Aventura", "Comédia", "Drama", "Fantasia", "Ficção-Científica", "Romance", "Suspense", "Terror"]
Clistafo0=[ "0",                        "48",         "3",    "7",        "8",        "5",       "4",      "14",                "16",      "15",       "11"]
Clistafo1=["Sem filtro (Mostrar Todos)","Lançamentos","Ação", "Animação", "Aventura", "Comédia", "Drama",  "Ficção-Científica", "Romance", "Suspense", "Terror"]
ClistaMM0=["lancamentos","acao","animacao","aventura","comedia","drama","fantasia","ficcao-cientifica","guerra","policial","romance","suspense","terror"]
ClistaMM1=["Lançamentos","Ação","Animação","Aventura","Comédia","Drama","Fantasia","F. Científica",    "Guerra","Policial","Romance","Suspense","Terror"]
ClistaGO0=["all",                       "lancamentos","acao","animacao","aventura","comedia","drama","ficcao-cientifica","guerra","policial","romance","suspense","terror"]
ClistaGO1=["Sem filtro (Mostrar Todos)","Lançamentos","Ação","Animação","Aventura","Comédia","Drama","Ficção-Científica","Guerra","Policial","Romance","Suspense","Terror"]

def setViewS():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	xbmc.executebuiltin("Container.SetViewMode(50)")
def setViewS2():
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	xbmc.executebuiltin("Container.SetViewMode(50)")
def setViewM():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmc.executebuiltin("Container.SetViewMode(50)")
def setViewM2():
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
	xbmc.executebuiltin("Container.SetViewMode(50)")
	
favfilmesFile = os.path.join(addon_data_dir, 'favoritesf.txt')
favseriesFile = os.path.join(addon_data_dir, 'favoritess.txt')
historicFile = os.path.join(addon_data_dir, 'historic.txt')

	
makeGroups = "true"
URLP="http://cubeplay.000webhostapp.com/"
#URLP="http://localhost:8080/"
URLNC=URLP+"cloud/v2/nc/"
URLFO=URLP+"fo/"

proxy = "http://cubeplay.000webhostapp.com/nc/nc.php?u="
proxy = ""

RC="redecanais.cloud/"
RCref="https://homeingles.fun/"
	
def getLocaleString(id):
	return Addon.getLocalizedString(id).encode('utf-8')

def Categories(): #70
	#AddDir("[B]!{0}: {1}[/B] - {2} ".format(getLocaleString(30036), getLocaleString(30037) if makeGroups else getLocaleString(30038) , getLocaleString(30039)), "setting" ,50 ,os.path.join(iconsDir, "setting.png"), isFolder=False)
	#AddDir("[COLOR white][B][Canais de TV1][/B][/COLOR]" , "", 100, "http://oi68.tinypic.com/116jn69.jpg", "http://oi68.tinypic.com/116jn69.jpg")
	AddDir("[COLOR white][B][Canais de TV][/B][/COLOR]" , "", 102, "http://www.clker.com/cliparts/c/a/c/2/12316861951931359250rg1024_cartoon_tv.svg.hi.png", "http://www.clker.com/cliparts/c/a/c/2/12316861951931359250rg1024_cartoon_tv.svg.hi.png")
	AddDir("[COLOR white][B][Canais de TV2][/B][/COLOR]" , "", 100, "http://www.clker.com/cliparts/c/a/c/2/12316861951931359250rg1024_cartoon_tv.svg.hi.png", "http://www.clker.com/cliparts/c/a/c/2/12316861951931359250rg1024_cartoon_tv.svg.hi.png")
	AddDir("[B][COLOR white][Filmes][/COLOR][/B]", "" , -2,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	AddDir("[COLOR white][B][Séries/Animes/Desenhos/Novelas][/B][/COLOR]" , "", -3, "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg", "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg")
	AddDir("[COLOR gold][B][Filmes Favoritos Cube Play][/B][/COLOR]", "" ,301 , "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png", "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png")
	AddDir("[COLOR gold][B][Séries Favoritas Cube Play][/B][/COLOR]", "" ,302 , "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png", "http://icons.iconarchive.com/icons/royalflushxx/systematrix/256/Favorites-icon.png")
	AddDir("[COLOR green][B][Histórico Filmes][/B][/COLOR]", "" ,305 , "https://cdn2.iconfinder.com/data/icons/business-office-icons/256/To-do_List-512.png", "https://cdn2.iconfinder.com/data/icons/business-office-icons/256/To-do_List-512.png")
	AddDir("[COLOR pink][B][Busca][/B][/COLOR]" , "", 160, "https://azure.microsoft.com/svghandler/search/?width=400&height=315", "https://azure.microsoft.com/svghandler/search/?width=400&height=315")
	AddDir("[B][Sobre o Addon][/B]", "" ,0 ,"http://www.iconsplace.com/icons/preview/orange/about-256.png", "http://www.iconsplace.com/icons/preview/orange/about-256.png", isFolder=False, info="Addon modificado do PlaylistLoader 1.2.0 por Avigdor\r https://github.com/avigdork/xbmc-avigdork.\r\nNão somos responsáveis por colocar o conteudo online, apenas indexamos os vídeos disponíveis na internet.\r\nVersão atual: "+Versao)
	AddDir("[B][COLOR orange][Checar Atualizações][/COLOR][/B]", "" , 200,"https://accelerator-origin.kkomando.com/wp-content/uploads/2015/04/update2-970x546.jpg", "https://accelerator-origin.kkomando.com/wp-content/uploads/2015/04/update2-970x546.jpg", isFolder=False, info="Checar se há atualizações\n\nAs atualizações normalmente são automáticas\nUse esse recurso caso não esteja recebendo automaticamente\r\nVersão atual: "+Versao)
# --------------  Menu
def MCanais(): #-1
	AddDir("[B][COLOR cyan][Filmes Lançamentos MMFilmes.tv][/COLOR][/B]", "config" , 100,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	link = OpenURL("https://pastebin.com/raw/31SLZ8D8")
	match = re.compile('(.+);(.+)').findall(link)
	for name2,url2 in match:
		AddDir("[COLOR while][B]["+name2+"][/COLOR][/B]" , url2, 102, "http://oi68.tinypic.com/116jn69.jpg", "http://oi68.tinypic.com/116jn69.jpg")
	setViewM()
def MFilmes(): #-2
	#AddDir("[COLOR white][B][Filmes Dublado/Legendado][/B][/COLOR]" , cPage, 220, "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", background="cPage")
	#AddDir("[B][COLOR cyan][Filmes Lançamentos MMFilmes.tv][/COLOR][/B]", "config" , 184,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	#AddDir("[B][COLOR cyan][Filmes MMFilmes.tv][/COLOR][/B]", "config" , 180,"https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", "https://walter.trakt.tv/images/movies/000/191/797/fanarts/thumb/6049212229.jpg", isFolder=True)
	#AddDir("[COLOR maroon][B][Filmes GoFilmes.me][/B][/COLOR]" , "", 210, "https://walter.trakt.tv/images/movies/000/219/436/fanarts/thumb/0ff039faa5.jpg", "https://walter.trakt.tv/images/movies/000/219/436/fanarts/thumb/0ff039faa5.jpg")
	AddDir("[COLOR yellow][B][Filmes NetCine.us][/B][/COLOR]" , "", 71, "https://walter.trakt.tv/images/movies/000/181/312/fanarts/thumb/e30b344522.jpg", "https://walter.trakt.tv/images/movies/000/181/312/fanarts/thumb/e30b344522.jpg")
	AddDir("[COLOR blue][B][Filmes Lançamentos RedeCanais][/B][/COLOR]" , cPage, 221, "https://walter.trakt.tv/images/movies/000/222/216/fanarts/thumb/6f9bb1a733.jpg", "https://walter.trakt.tv/images/movies/000/222/216/fanarts/thumb/6f9bb1a733.jpg", background="cPage")
	AddDir("[COLOR blue][B][Filmes Dublado RedeCanais][/B][/COLOR]" , cPage, 90, "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", "https://walter.trakt.tv/images/movies/000/222/254/fanarts/thumb/401d5f083e.jpg", background="cPage")
	AddDir("[COLOR blue][B][Filmes Legendado RedeCanais][/B][/COLOR]" , cPageleg, 91, "https://walter.trakt.tv/images/movies/000/181/313/fanarts/thumb/cc9226edfe.jpg", "https://walter.trakt.tv/images/movies/000/181/313/fanarts/thumb/cc9226edfe.jpg", background="cPageleg")
	AddDir("[COLOR blue][B][Filmes Nacional RedeCanais][/B][/COLOR]" , cPagenac, 92, "http://cdn.cinepop.com.br/2016/11/minhamaeeumapeca2_2-750x380.jpg", "http://cdn.cinepop.com.br/2016/11/minhamaeeumapeca2_2-750x380.jpg", background="cPagenac")
	#AddDir("[COLOR purple][B][Filmes FilmesOnline.online][/B][/COLOR]" , "", 170, "https://walter.trakt.tv/images/movies/000/167/163/fanarts/thumb/23ecb5f950.jpg.webp", "https://walter.trakt.tv/images/movies/000/167/163/fanarts/thumb/23ecb5f950.jpg.webp")
	#AddDir("[COLOR lightgreen][B][Filmes Superflix.net][/B][/COLOR]" , "", 411, "https://walter.trakt.tv/images/movies/000/167/163/fanarts/thumb/23ecb5f950.jpg.webp", "https://walter.trakt.tv/images/movies/000/167/163/fanarts/thumb/23ecb5f950.jpg.webp")
	setViewM()
def MSeries(): #-3
	AddDir("[COLOR yellow][B][Séries NetCine.us][/B][/COLOR]" , "", 60, "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg", "https://walter.trakt.tv/images/shows/000/098/898/fanarts/thumb/bca6f8bc3c.jpg")
	AddDir("[COLOR blue][B][Séries RedeCanais][/B][/COLOR]" , cPageser, 130, "https://walter.trakt.tv/images/shows/000/001/393/fanarts/thumb/fc68b3b649.jpg", "https://walter.trakt.tv/images/shows/000/001/393/fanarts/thumb/fc68b3b649.jpg", background="cPageser")
	AddDir("[COLOR blue][B][Animes RedeCanais][/B][/COLOR]" , cPageser, 140, "https://walter.trakt.tv/images/shows/000/098/580/fanarts/thumb/d48b65c8a1.jpg", "https://walter.trakt.tv/images/shows/000/098/580/fanarts/thumb/d48b65c8a1.jpg", background="cPageser")
	AddDir("[COLOR blue][B][Desenhos RedeCanais][/B][/COLOR]" , cPageani, 150, "https://walter.trakt.tv/images/shows/000/069/829/fanarts/thumb/f0d18d4e1d.jpg", "https://walter.trakt.tv/images/shows/000/069/829/fanarts/thumb/f0d18d4e1d.jpg", background="cPageser")
	AddDir("[COLOR blue][B][Novelas RedeCanais][/B][/COLOR]" , cPagenov, 230, "https://walter.trakt.tv/images/shows/000/126/467/fanarts/full/efa214c5f4.jpg.webp", "https://walter.trakt.tv/images/shows/000/126/467/fanarts/full/efa214c5f4.jpg.webp", background="cPageser")
	#AddDir("[B][COLOR cyan][Séries MMFilmes.tv][/COLOR][/B]", "config" , 190,"https://walter.trakt.tv/images/shows/000/037/522/fanarts/thumb/6ecdb75c1c.jpg", "https://walter.trakt.tv/images/shows/000/037/522/fanarts/thumb/6ecdb75c1c.jpg", isFolder=True)
	#AddDir("[B][COLOR lightgreen][Séries Superflix.net][/COLOR][/B]", "config" , 401,"https://walter.trakt.tv/images/shows/000/037/522/fanarts/thumb/6ecdb75c1c.jpg", "https://walter.trakt.tv/images/shows/000/037/522/fanarts/thumb/6ecdb75c1c.jpg", isFolder=True)
	setViewM()
# --------------  Fim menu
# --------------  common
def OpenURL(url, headers={}, user_data={}, cookieJar=None, justCookie=False):
	req = Request(url)
	headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0'
	req.headers['Range'] = 'bytes=%s-%s' % (100, 350)
	for k, v in headers.items():
		req.add_header(k, v)
	#if not 'User-Agent' in headers:
		#req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0')
	return urlopen(req).read().decode("utf-8").replace("\r", "")
def ReadList(fileName):
	import shutil
	try:
		with open(fileName, 'r') as handle:
			content = json.load(handle)
	except Exception as ex:
		xbmc.log(str(ex), 5)
		if os.path.isfile(fileName):
			shutil.copyfile(fileName, "{0}_bak.txt".format(fileName[:fileName.rfind('.')]))
			xbmc.executebuiltin('Notification({0}, NOT read file: "{1}". \nBackup createad, {2}, {3})'.format(AddonName, os.path.basename(fileName), 5000, icon))
		content=[]
	return content
def SaveList(filname, chList):
	try:
		with io.open(filname, 'w', encoding='utf-8') as handle:
			handle.write(unicode(json.dumps(chList, indent=4, ensure_ascii=False)))
		success = True
	except Exception as ex:
		xbmc.log(str(ex), 3)
		success = False
	return success
# --------------  Inicio Filme CB
def Filmes96(): #220
	link = OpenURL("https://pastebin.com/raw/ZkfFMB20")
	m = link.split("\n")
	for x in m:
		try:
			meta = eval(x)
			AddDir(meta['title'] +" [COLOR yellow]("+str(meta['year'])+")[/COLOR] "+" [COLOR blue]["+str(meta['rating'])+"][/COLOR]" , meta['mp4'] +"?play", 229, isFolder=False, IsPlayable=True, metah=meta)
		except:
			pass
	setViewM()
def FilmesRC(): #221
	link = OpenURL("https://pastebin.com/raw/taJHVbXj")
	m = link.split("\n")
	link2 = OpenURL("https://pastebin.com/raw/FwSnnr65")
	i=1
	for x in m:
		try:
			meta = eval(x)
			file = meta['mp4'].split("$")
			reg = "(.+)\$"+file[1]
			m = re.compile(reg, re.IGNORECASE).findall(link2)
			url2 = m[0]
			AddDir(meta['title'] +" [COLOR yellow]("+str(meta['year'])+")[/COLOR] "+" [COLOR blue]["+str(meta['rating'])+"][/COLOR]" , url2 + file[0] +"?play|Referer=http://redecanais.xyz/", 229, isFolder=False, IsPlayable=True, metah=meta)
		except:
			pass
	setViewM()
def PlayFilmes96(): #229
	PlayUrl(name, url, iconimage, info, "", metah)
# --------------  Fim Filme CB
# --------------  NETCINE
def CategoryOrdem(x):
	x2 = Addon.getSetting(eval("x"))
	name2 = "Data" if x2=="0" else "Título"
	AddDir("[COLOR green][B][Organizado por:][/B] "+name2 +" (Clique para alterar)[/COLOR]" , x, 81, "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
def CategoryOrdem2(url):
	x2 = Addon.getSetting(url)
	x = "0" if x2=="1" else "1"
	#xbmcgui.Dialog().ok("Escolha a resolução:", x + x2 + url)
	Addon.setSetting(url, x )
	xbmc.executebuiltin("Container.Refresh()")
def Series(): #60
	try:
		CategoryOrdem("cOrdNCS")
		link = OpenURL("http://netcine.biz/tvshows/page/1/").replace("\n","").replace("\r","")
		ST(link)
		l2 = re.compile("box_movies(.+)").findall(link)
		link = OpenURL("http://netcine.biz/tvshows/page/2/").replace("\n","").replace("\r","")
		l3 = re.compile("box_movies(.+)").findall(link)
		lista = re.compile("img src\=\"([^\"]+).+?alt\=\"([^\"]+).+?f\=\"([^\"]+)").findall(l2[0]+l3[0])
		#if cOrdNCS=="1":
			#lista = sorted(lista, key=lambda lista: lista[1])
		ST(lista)
		for img2,name2,url2 in lista:
			if name2!="Close":
				name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
				img2 = re.sub('-120x170.(jpg|png)', r'.\1', img2 )
				AddDir(name2 ,url2, 61, img2, img2, isFolder=True)
	except:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "", 0, isFolder=False)
def ListSNC(x): #61
	try:
		link = OpenURL(url).replace('\n','').replace('\r','').replace('<div class="soci">',"class='has-sub'").replace('\t',"")
		m = re.compile("(.emporada \w+)(.+?class\=\'has-sub\')").findall(link)
		info2 = re.compile("<h2>Synopsis<\/h2>+.+?[div|p].{0,15}?.+?(.+?)<\/").findall(link)
		info2 = re.sub('style\=.+?\>', '', info2[0] ) if info2 else " "
		i=0
		if "None" in background:
			for season,epis in m:
				AddDir("[B]["+season+"][/B]" ,url, 61, iconimage, iconimage, isFolder=True, background=i,info=info2)
				i+=1
		else:
			m2 = re.compile("href\=\"([^\"]+).+?(\d+) - (\d+)").findall( m[int(x)][1] )
			m3 = re.compile("icon-chevron-right\W+\w\W+([^\<]+)").findall( m[int(x)][1] )
			for url2,S,E in m2:
				AddDir("S"+S+"E"+E +" - "+m3[i],url2, 62, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info)
				i+=1
	except:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "", 0, isFolder=False)
def PlayS(): #62
	try:
		link = OpenURL(url).replace('\n','').replace('\r','')
		m = re.compile("\"play-.\".+?src=\"([^\"]+)").findall(link)
		listan = re.compile("\#play-...(\w*)").findall(link)
		i=0
		listaf=[]
		listal=[]
		for url2 in m:
			link3 = OpenURL(url2)
			m3 = re.compile("src\=\"(.+campanha[^\"]+)").findall(link3)
			if m3:
				red = OpenURL(m3[0])
				red2 = re.compile('redirecionar\.php\?data=([^"]+)').findall(red)
				link4 = OpenURL(red2[0])
				link4 = re.sub('window.location.href.+', '', link4)
				link4 = link4.replace("'",'"')
				m4= re.compile("http.+?mp4[^\"]+").findall(link4) 
				m4 = list(reversed(m4))
				for url4 in m4:
					listal.append(url4.replace("';",""))
					dubleg="[COLOR green]HD[/COLOR][/B]" if "ALTO" in url4 else "[COLOR red]SD[/COLOR][/B]"
					listaf.append("[B][COLOR blue]"+listan[i] +"[/COLOR] "+dubleg)
			else:
				red = OpenURL(url2)
				m3 = re.compile("src\=\"([^\"]+)").findall(red)
				red1 = OpenURL(m3[0])
				red2 = re.compile('redirecionar\.php\?data=([^"]+)').findall(red1)
				link4 = OpenURL(red2[0],headers={'Cookie': "autorizado=teste; "})
				m5 = re.compile("location.href=\'([^\']+p\=[^\']+)").findall(link4)
				for x in m5:
					if not "openload" in x:
						link5 = OpenURL(x)
				link5 = re.sub('window.location.href.+', '', link5)
				link5 = link5.replace("'",'"')
				m4= re.compile("http.+?mp4[^\"]+").findall(link5)
				m4 = list(reversed(m4))
				for url4 in m4:
					listal.append(url4.replace("';",""))
					dubleg="[COLOR green]HD[/COLOR][/B]" if "ALTO" in url4 else "[COLOR red]SD[/COLOR][/B]"
					listaf.append("[B][COLOR blue]"+listan[i] +"[/COLOR] "+dubleg)
			i+=1
		d = xbmcgui.Dialog().select("Escolha a resolução:", listaf)
		if d!= -1:
			listal[d] = re.sub('https', 'http', listal[d])
			PlayUrl(name, listal[d]+"|Referer=http://cdn.netcine.info&Connection=Keep-Alive&Accept-Language=en&User-Agent=Mozilla%2F5.0+%28compatible%3B+MSIE+10.6%3B+Windows+NT+6.1%3B+Trident%2F6.0%29", iconimage, info)
	except:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
		sys.exit()
# --------------------------------------
def MoviesNC(): #71
	AddDir("[COLOR yellow][B][Genero dos Filmes]:[/B] " + Clista3[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	CategoryOrdem("cOrdNCF")
	try:
		if int(cPageFNC) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPageFNC) ) +"[/B]][/COLOR]", cPageFNC , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPageFNC")
		else:
			AddDir("[COLOR blue][B]Proxima Pagina >>  ["+ str( int(cPageFNC) + 2 ) +"[/B]][/COLOR]", cPageFNC , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPageFNC")
		l = int(cPageFNC) * 4
		if Cat=="0":
			link = OpenURL("http://netcine.biz/page/"+str( l+1 )+"/?filmes").replace('\n','').replace('\r','')
			l1 = re.compile("box_movies(.+)").findall(link)
			link = OpenURL("http://netcine.biz/page/"+str( l+2 )+"/?filmes").replace('\n','').replace('\r','')
			l2 = re.compile("box_movies(.+)").findall(link)
			link = OpenURL("http://netcine.biz/page/"+str( l+3 )+"/?filmes").replace('\n','').replace('\r','')
			l3 = re.compile("box_movies(.+)").findall(link)
			link = OpenURL("http://netcine.biz/page/"+str( l+4 )+"/?filmes").replace('\n','').replace('\r','')
			l4 = re.compile("box_movies(.+)").findall(link)
			#link = OpenURL("http://netcine.biz/page/"+str( l+5 )+"/?filmes").replace('\n','').replace('\r','')
			#l5 = re.compile("box_movies(.+)").findall(link)
			lista = re.compile("img src\=\"([^\"]+).+?alt\=\"([^\"]+).+?f\=\"([^\"]+)").findall(l1[0]+l2[0]+l3[0]+l4[0])
		else:
			link = OpenURL("http://netcine.biz/category/"+Clista[int(Cat)] + "/page/"+str( l+1 )+"/").replace('\n','').replace('\r','')
			l1 = re.compile("box_movies(.+)").findall(link)
			link = OpenURL("http://netcine.biz/category/"+Clista[int(Cat)] + "/page/"+str( l+2 )+"/").replace('\n','').replace('\r','')
			l2 = re.compile("box_movies(.+)").findall(link)
			link = OpenURL("http://netcine.biz/category/"+Clista[int(Cat)] + "/page/"+str( l+3 )+"/").replace('\n','').replace('\r','')
			l3 = re.compile("box_movies(.+)").findall(link)
			link = OpenURL("http://netcine.biz/category/"+Clista[int(Cat)] + "/page/"+str( l+4 )+"/").replace('\n','').replace('\r','')
			l4 = re.compile("box_movies(.+)").findall(link)
			lista = re.compile("img src\=\"([^\"]+).+?alt\=\"([^\"]+).+?f\=\"([^\"]+)").findall(l1[0]+l2[0]+l3[0]+l4[0])
		if cOrdNCF=="1":
			lista = sorted(lista, key=lambda lista: lista[1])
		for img2,name2,url2 in lista:
			if name2!="Close":
				name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
				img2 = re.sub('-120x170.(jpg|png)', r'.\1', img2 )
				AddDir(name2 ,url2, 78, img2, img2, isFolder=True)
		AddDir("[COLOR blue][B]Proxima Pagina >>  ["+ str( int(cPageFNC) + 2 ) +"[/B]][/COLOR]", cPageFNC , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPageFNC")
	except:
		AddDir("Server NETCINE offline, tente novamente em alguns minutos" , "", 0, isFolder=False)
def ListMoviesNC(): #78
	try:
		link = OpenURL(url).replace('\n','').replace('\r','')
		m = re.compile("\"play-.\".+?src=\"([^\"]+)").findall(link)
		m2 = re.compile("\#play-...(\w*)").findall(link)
		info2 = re.compile("<h2>Synopsis<\/h2>+.+?[div|p].{0,15}?.+?(.+?)<\/").findall(link)
		info2 = re.sub('style\=.+?\>', '', info2[0] ) if info2 else ""
		i=0
		for name2 in m2:
			AddDir(name +" [COLOR blue]("+ name2 +")[/COLOR]", m[i], 79, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info2, background=url)
			i+=1
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, isFolder=False)
def PlayMNC(): #79
	global background
	#try:
	i=0
	listaf=[]
	listal=[]
	link = OpenURL(url)
	#red = re.compile('redirecionar\.php\?data=([^"]+)').findall(link)
	#ST(red)
	#if not red:
	red2 = re.compile('http[^"]+').findall(link)
	link2 = OpenURL(red2[0])
	red = re.compile('redirecionar\.php\?data=([^"]+)').findall(link2)
	if not "desktop" in red[0]:
		link2 = OpenURL(red[0])
		red = re.compile('location.href=\'([^\']+p\=[^\']+)').findall(link2)
	link3 = OpenURL(red[0],headers={'Cookie': "autorizado=teste; "})
	link3 = re.sub('window.location.+', '', link3)
	link3 = link3.replace("'",'"')
	m4= re.compile("http.+?mp4[^\"]{0,150}").findall(link3) 
	m4 = list(reversed(m4))
	for url4 in m4:
		if not "openload" in url4:
			listal.append(url4.replace("';",""))
			dubleg="[COLOR green]HD[/COLOR][/B]" if "ALTO" in url4 else "[COLOR red]SD[/COLOR][/B]"
			listaf.append("[B]"+dubleg)
	d = xbmcgui.Dialog().select("Escolha a resolução:", listaf)
	if d!= -1:
		background=background+";;;"+name+";;;NC"
		listal[d] = re.sub('https', 'http', listal[d])
		PlayUrl(name, listal[d]+"|Referer=http://cdn.netcine.info&Connection=Keep-Alive&Accept-Language=en&User-Agent=Mozilla%2F5.0+%28compatible%3B+MSIE+10.6%3B+Windows+NT+6.1%3B+Trident%2F6.0%29", iconimage, info)
	else:
		sys.exit()
	#except:
		#xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
		#sys.exit()
def Generos(): #80
	global Cat
	d = xbmcgui.Dialog().select("Escolha o Genero", Clista3)
	if d != -1:
		Addon.setSetting("Cat", str(d) )
		Cat = d
		Addon.setSetting("cPage", "0" )
		Addon.setSetting("cPageleg", "0" )
		xbmc.executebuiltin("Container.Refresh()")
# --------------  FIM NETCINE
# --------------  REDECANAIS FILMES
def MoviesRCD(): #90 Filme dublado
	AddDir("[COLOR yellow][B][Genero dos Filmes]:[/B] " + Clista3[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	CategoryOrdem("cOrdRCF")
	try:
		p= 1
		if int(cPage) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPage) ) +"[/B]][/COLOR]", cPage , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPage")
		l= int(cPage)*5
		exurl=['']
		if "imdb" in cadulto:
			AddDir("[COLOR maroon]Reload[/COLOR]" , "", 50, isFolder=False)
			dir = re.sub('CubePlay', 'CubePlayMeta', addon_data_dir )
			file = os.path.join(dir, 'imdb.txt')
			chList = ReadList(file)
			exurl = re.compile('\_[^\']+').findall(str(chList))
		for x in range(0, 5):
			l +=1
			link = OpenURL(proxy+"https://"+RC+"browse-filmes-dublado-videos-"+str(l)+"-"+cOrdRCF+".html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = OpenURL(proxy+"https://"+RC+"browse-"+Clista2[int(Cat)]+"-Filmes-videos-"+str(l)+"-"+cOrdRCF+".html")
			match = re.compile('href=\".{1,100}(\_[^\"]+).{0,10}title=\"([^\"]+)\".{20,350}echo=\"([^\"]+)').findall(link.replace('\n','').replace('\r',''))
			#match = re.compile('href=\"([^\"]+).{0,10}title=\"([^\"]+)\".{20,350}echo=\"([^\"]+)').findall(link.replace('\n','').replace('\r',''))
			if match:
				for url2,name2,img2 in match:
					url2 = re.sub('^\.', "https://"+RC, url2 )
					img2 = re.sub('^/', "https://"+RC, img2 )
					if cPlayD == "true" and "imdb" in cadulto:
						if not url2 in exurl:
							AddDir("[COLOR blue]"+name2+"[/COLOR]" ,url2, 350, img2, img2, info="", isFolder=False, IsPlayable=False)
					elif cPlayD == "true":
						AddDir(name2 ,url2, 96, img2, img2, info="", isFolder=False, IsPlayable=True)
					else:
						AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		#ST(p)
		if p >= 40:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPage) + 2) +"[/B]][/COLOR]", cPage , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPage")
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
def MoviesRCL(): #91 Filme Legendado
	AddDir("[COLOR yellow][B][Genero dos Filmes]:[/B] " + Clista3[int(Cat)] +"[/COLOR]", "url" ,80 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	CategoryOrdem("cOrdRCF")
	try:
		p= 1
		if int(cPageleg) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPageleg) ) +"[/B]][/COLOR]", cPageleg , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPageleg")
		l= int(cPageleg)*5
		for x in range(0, 5):
			l +=1
			link = OpenURL(proxy+"https://"+RC+"browse-filmes-legendado-videos-"+str(l)+"-"+cOrdRCF+".html")
			if Clista2[int(Cat)] != "Sem filtro (Mostrar Todos)":
				link = OpenURL(proxy+"https://"+RC+"browse-"+Clista2[int(Cat)]+"-Filmes-Legendado-videos-"+str(l)+"-"+cOrdRCF+".html")
			match = re.compile('href=\"([^\"]+).{0,10}title=\"([^\"]+)\".{20,350}echo=\"([^\"]+)').findall(link.replace('\n','').replace('\r',''))
			if match:
				for url2,name2,img2 in match:
					url2 = re.sub('^\.', "https://"+RC+"", url2 )
					img2 = re.sub('^/', "https://"+RC, img2 )
					if cPlayD == "true":
						AddDir(name2 ,url2, 96, img2, img2, info="", isFolder=False, IsPlayable=True)
					else:
						AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 40:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPageleg) + 2) +"[/B]][/COLOR]", cPageleg , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPageleg")
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
def MoviesRCN(): #92 Filmes Nacional
	CategoryOrdem("cOrdRCF")
	try:
		p= 1
		if int(cPagenac) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPagenac) ) +"[/B]][/COLOR]", cPagenac , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPagenac")
		l= int(cPagenac)*5
		for x in range(0, 5):
			l +=1
			link = OpenURL(proxy+"https://"+RC+"browse-filmes-nacional-videos-"+str(l)+"-"+cOrdRCF+".html")
			match = re.compile('href=\"([^\"]+).{0,10}title=\"([^\"]+)\".{20,350}echo=\"([^\"]+)').findall(link.replace('\n','').replace('\r',''))
			if match:
				for url2,name2,img2 in match:
					url2 = re.sub('^\.', "https://"+RC, url2 )
					img2 = re.sub('^/', "https://"+RC, img2 )
					if cPlayD == "true":
						AddDir(name2 ,url2, 96, img2, img2, info="", isFolder=False, IsPlayable=True)
					else:
						AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 40:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPagenac) + 2) +"[/B]][/COLOR]", cPagenac , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPagenac")
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0)
def MoviesRCR(): # Lancamentos
	#CategoryOrdem("cOrdRCF")
	try:
		p= 1
		if int(cPagelan) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(cPagelan) ) +"[/B]][/COLOR]", cPagelan , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPagelan")
		l= int(cPagelan)*5
		for x in range(0, 5):
			l +=1
			link = OpenURL(proxy+"https://"+RC+"browse-filmes-lancamentos-videos-"+str(l)+"-date.html")
			match = re.compile('href=\"([^\"]+).{0,10}title=\"([^\"]+)\".{20,350}echo=\"([^\"]+)').findall(link.replace('\n','').replace('\r',''))
			if match:
				for url2,name2,img2 in match:
					url2 = re.sub('^\.', "https://"+RC, url2 )
					img2 = re.sub('^/', "https://"+RC, img2 )
					if cPlayD == "true":
						AddDir(name2 ,url2, 96, img2, img2, info="", isFolder=False, IsPlayable=True) 
					else:
						AddDir(name2 ,url2, 95, img2, img2, info="")
					p += 1
			else:
				break
		if p >= 40:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(cPagelan) + 2) +"[/B]][/COLOR]", cPagelan , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPagelan")
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "", 0)
def PlayMRC(): #95 Play filmes
	url2 = re.sub('redecanais\.[^\/]+', RC, url.replace("http","https") )
	if not "redecanais" in url2:
		url2 = "https://"+RC+ url2
	try:
		link = OpenURL(proxy+url2.replace("http\:","https\:"))
		desc = re.compile('itemprop=\"?description\"?>\s.{0,10}?<p>(.+)<\/p>').findall(link)
		if desc:
			desc = html.unescape (desc[0])
		player = re.compile('<iframe.{1,50}src=\"(\/?p[^\"]+)\"').findall(link)
		if player:
			player = re.sub('^/', "https://"+RC, player[0])
			player = re.sub('\.php', "hlb.php", player)
			mp4 = OpenURL(player ,headers={'referer': "https://redecanais.cloud/"})
			file=re.compile('[^"|\']+\.mp4').findall(mp4)
			AddDir("[B][COLOR yellow]"+ name +" [/COLOR][/B]"  , file[0] + "?attachment=true|referer=https://lll.llllllllllllllllllllllllllllllllllllllll.fun/", 3, iconimage, iconimage, index=0, isFolder=False, IsPlayable=True, info=desc, background=url+";;;"+name+";;;RC")
		else:
			AddDir("[B]Ocorreu um erro[/B]"  , "", 0, iconimage, iconimage, index=0, isFolder=False, IsPlayable=False, info="Erro")
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
def PlayMRC2(): #96 Play filmes direto
	global background
	url2 = re.sub('redecanais\.[^\/]+', RC, url.replace("http\:","https\:") )
	if not "redecanais" in url2:
		url2 = "https://"+RC+ url2
	try:
		link = OpenURL(proxy+url2.replace("http\:","https\:"))
		desc = re.compile('itemprop=\"?description\"?>\s.{0,10}?<p>(.+)<\/p>').findall(link)
		if desc:
			desc = html.unescape(desc[0])
		else:
			desc = ""
		player = re.compile('<iframe.{1,50}src=\"(\/?p[^\"]+)\"').findall(link)
		if player:
			#mp4 = re.compile('server(f?\d*).+vid\=(\w+)').findall(player[0])
			#reg = "(.+)\\$rc"+mp4[0][0]
			#pb = OpenURL("https://pastebin.com/raw/FwSnnr65")
			#ss = re.compile('(.{1,65})RCFServer.{1,35}\.mp4').findall(pb)
			#pb = re.sub('\$s1\/', ss[0], pb )
			#pb = re.sub('\$s2\/', ss[1], pb )
			#m = re.compile(reg, re.IGNORECASE).findall(pb)
			#url2 = m[0]
			#file = url2 + mp4[0][1]+".mp4"
			#ST(player)
			#player = "https://redecanais.cloud//player3/serverf4hlb.php?vid=TGO"
			#return
			player = re.sub('^/', "https://"+RC, player[0])
			player = re.sub('\.php', "hlb.php", player)
			player = re.sub('redecanais\.[^\/]+', "homeingles.fun", player)
			mp4 = OpenURL(player ,headers={'referer': RCref})
			try:
				player = re.compile('href.{1,5}(mega[^"|\']*)').findall(mp4)
				mp42 = OpenURL("https://noticiasfix.fun/player3/"+player[0], headers={'referer': RCref})
				#ST(mp42)
				source = re.compile('source.+').findall(mp42)
				file=re.compile('[^"|\']+\.mp4[^"|\'|\n]*').findall(source[0])
				file[0] = re.sub('https', 'http', file[0])
				tf = testfile(file[0])
				if tf == True:
					NF(2)
				else:
					f="1"+1
			except:
				NF(1)
				file=re.compile('src..(http.{1,200}\.mp4[^"|\']*)').findall(mp4)
			#exp = re.compile('expires\=([^\'|\"]+)').findall(auth)
			#player = re.sub('\.php', "hlb.php", player)
			#file=re.compile('[^"|\']+\.mp4.{1,15}.m3u8').findall(mp4)
			#return
			#mp4 = OpenURL(player + "&expires=" + exp[0] ,headers={'referer': "https://redecanais.cloud/"})
			background=url+";;;"+name+";;;RC"
			file[0] = re.sub('\n', '', file[0])
			#file[0] = re.sub('https', 'http', file[0])
			PlayUrl("[B][COLOR white]"+ name +" [/COLOR][/B]", file[0] +"|Referer=https://homeingles.fun&Connection=Keep-Alive&Accept-Language=en&User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0", iconimage, desc) #aqui
		else:
			AddDir("[B]Ocorreu um erro[/B]"  , "", 0, iconimage, iconimage, index=0, isFolder=False, IsPlayable=False, info="Erro")
	except:
		xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
		sys.exit()
# ----------------- FIM REDECANAIS
# --------------  REDECANAIS SERIES,ANIMES,DESENHOS
def PlaySRC(): #133 Play series
	try:
		url2 = re.sub('redecanais\.[^\/]+', RC, url.replace("http\:","https\:") )
		link = OpenURL(proxy+url2)
		player = re.compile('<iframe.{1,50}src=\"(\/?p[^\"]+)\"').findall(link)
		if player:
			""" mp4 = re.compile('server(f?\d*).+vid\=(\w+)').findall(player[0])
			reg = "(.+)\\$rc"+mp4[0][0]
			pb = OpenURL("https://pastebin.com/raw/FwSnnr65")
			ss = re.compile('(.{1,65})RCF?Server.{1,35}\.mp4').findall(pb)
			try:
				pb = re.sub('\$s1\/', ss[2], pb )
			except:
				pb = re.sub('\$s1\/', ss[0], pb )
			try:
				pb = re.sub('\$s2\/', ss[3], pb )
			except:
				pb = re.sub('\$s2\/', ss[1], pb )
			m = re.compile(reg, re.IGNORECASE).findall(pb)
			url2 = m[0]
			file = url2 + mp4[0][1]+".mp4"
			player = re.sub('.php', "playerfree.php", player[0] ) """
			player = re.sub('^/', "https://"+RC, player[0])
			player = re.sub('\.php', "hlb.php", player)
			player = re.sub('redecanais\.[^\/]+', "homeingles.fun", player)
			mp4 = OpenURL(player ,headers={'referer': RCref})
			try:
				player = re.compile('href.{1,5}(mega[^"|\']*)').findall(mp4)
				mp42 = OpenURL("https://homeingles.fun/player3/"+player[0] ,headers={'referer': RCref})
				source = re.compile('source.+').findall(mp42)
				file=re.compile('[^"|\']+\.mp4[^"|\'|\n]*').findall(source[0])
				file[0] = re.sub('https', 'http', file[0])
				tf = testfile(file[0])
				if tf == True:
					NF(2)
				else:
					f="1"+1
			except:
				NF(1)
				file=re.compile('src..(http.{1,200}\.mp4[^"|\']*)').findall(mp4)
			file[0] = re.sub('\n', '', file[0])	
			PlayUrl(name, file[0] + "|Referer=https://homeingles.fun&Connection=Keep-Alive&Accept-Language=en&User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0", iconimage, name)
		else:
			xbmcgui.Dialog().ok('Cube Play', 'Erro, tente novamente em alguns minutos')
	except:
		xbmcgui.Dialog().ok('Cube Play', 'Erro 2, tente novamente em alguns minutos')
		sys.exit()
def TemporadasRC(x): #135 Episodios
	url2 = re.sub('redecanais\.[^\/]+', RC, url.replace("http\:","https\:") )
	if not "redecanais" in url2:
		url2 = "https://"+RC+ url2
	link = OpenURL(proxy+url2).replace('\n','').replace('\r','').replace('</html>','<span style="font').replace("http\:","https\:")
	link = re.sub('<span style="font-size: x-large;">+.+?windows', "", link )
	temps = re.compile('(<span style="font-size: x-large;">(.+?)<\/span>)').findall(link)
	i= 0
	if background=="None":
		for b,tempname in temps:
			tempname = re.sub('<[\/]{0,1}strong>', "", tempname)
			tempname = html.unescape(tempname)
			if not "ilme" in tempname:
				AddDir("[B]["+tempname+"][/B]" , url, 135, iconimage, iconimage, info="", isFolder=True, background=i)
			i+=1
		AddDir("[B][Todos Episódios][/B]" ,url, 139, iconimage, iconimage, info="")
	else:
		temps2 = re.compile('size: x-large;\">.+?<span style\=\"font').findall(link)
		epi = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(temps2[int(x)])
		for name2,url2,brp in epi:
			name3 = re.compile('\d+').findall(name2)
			if name3:
				name3=name3[0]
			else:
				name3=name2
			urlm = re.compile('href\=\"(.+?)\"(.+?(Dub|Leg))?').findall(url2)
			url2 = re.sub('(\w)-(\w)', r'\1 \2', url2)
			namem = html.unescape( re.compile('([^\-]+)').findall(url2)[0])
			namem = re.sub('<[\/]{0,1}strong>', "", namem)
			if "<" in namem:
				namem = ""
			#if urlm:
				#urlm[0][0] = "http://www." + RC + urlm[0][0] if "http" not in urlm[0][0] else urlm[0][0]
			#if len(urlm) > 1:
				#urlm[0][1] = "http://www." + RC + urlm[0][1] if "http" not in urlm[0][1] else urlm[0][1]
				#AddDir("[COLOR yellow][Dub][/COLOR] "+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
				#AddDir("[COLOR blue][Leg][/COLOR] "+ name3 +" "+namem ,urlm[1], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			try:
				urlm2 = "https://" + RC + urlm[0][0] if "http" not in urlm[0][0] else urlm[0][0]
				dubleg=""
				if "Dub" in urlm[0][2]:
					dubleg = "[COLOR yellow][D][/COLOR] "
				elif "Leg" in urlm[0][2]:
					dubleg = "[COLOR blue][L][/COLOR] "
				AddDir(dubleg + name3 +" "+namem, urlm2, 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
				#AddDir(urlm2, urlm2, 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			except:
				pass				
			try:
				urlm2 = "https://" + RC + urlm[1][0] if "http" not in urlm[1][0] else urlm[1][0]
				dubleg=""
				if "Dub" in urlm[1][2]:
					dubleg = "[COLOR yellow][D][/COLOR] "
				elif "Leg" in urlm[1][2]:
					dubleg = "[COLOR blue][L][/COLOR] "
				AddDir(dubleg + name3 +" "+namem, urlm2, 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			except:
				pass
def SeriesRC(urlrc,pagina2, page1=135): #130 Lista as Series RC
	try:
		CategoryOrdem("cOrdRCS")
		pagina=eval(pagina2)
		p= 1
		if int(pagina) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
		l= int(pagina)*5
		for x in range(0, 5):
			l +=1
			link = OpenURL(proxy+"https://" + RC + "browse-"+urlrc+"-videos-"+str(l)+"-"+cOrdRCS+".html")
			match = re.compile('href=\"([^\"]+).{0,10}title=\"([^\"]+)\".{20,350}echo=\"([^\"]+)').findall(link.replace('\n','').replace('\r',''))
			if match:
				for url2,name2,img2 in match:
					url2 = re.sub('^\.', "https://"+ RC , url2 )
					img2 = re.sub('^/', "https://"+RC, img2 )
					if not "index.html" in url2:
						AddDir(name2 ,url2, page1, img2, img2, info="")
						p += 1
			else:
					break
		if p >= 40:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except:
		AddDir("Server error, tente novamente em alguns minutos" , url, 0, "", "")
def AllEpisodiosRC(): #139 Mostrar todos Epi
	url2 = re.sub('redecanais\.[^\/]+', RC, url.replace("http\:","https\:") )
	if not "redecanais" in url2:
		url2 = "https://"+ RC + url2
	link = OpenURL(url2)
	match = re.compile('<strong>(E.+?)<\/strong>(.+?)(<br|<\/p)').findall(link)
	S= 0
	if match:
		for name2,url2,brp in match:
			name3 = re.compile('\d+').findall(name2)
			if name3:
				name3=name3[0]
				if int(name3) == 1:
					S = S + 1
			else:
				name3=name2
			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			namem = html.unescape( re.compile('([^\-]+)').findall(url2)[0])
			if "<" in namem:
				namem = ""
			if urlm:
				if "http" not in urlm[0]:
					urlm[0] = "https://"+ RC + urlm[0]
			if len(urlm) > 1:
				if "http" not in urlm[1]:
					urlm[1] = "https://"+ RC  + urlm[1]
				AddDir("[COLOR yellow][Dub][/COLOR] S"+str(S)+" E"+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
				AddDir("[COLOR blue][Leg][/COLOR] S"+str(S)+" E"+ name3 +" "+namem ,urlm[1], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
			elif urlm:
				AddDir("S"+str(S)+" E"+ name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
def ListaNovRC():
	url2 = re.sub('redecanais\.[^\/]+', RC, url.replace("http\:","https\:") )
	if not "redecanais" in url2:
		url2 = "https://"+ RC + url2
	link = OpenURL(url2)
	match = re.compile('<strong>(C.+?)<\/strong>(.+?)(<br|<\/p)').findall(link)
	S= 0
	if match:
		for name2,url2,brp in match:
			name3 = re.compile('\d+').findall(name2)
			if name3:
				name3=name3[0]
				if int(name3) == 1:
					S = S + 1
			else:
				name3=name2
			urlm = re.compile('href\=\"(.+?)\"').findall(url2)
			namem = html.unescape( re.compile('([^\-]+)').findall(url2)[0] )
			if "<" in namem:
				namem = ""
			if urlm:
				if "http" not in urlm[0]:
					urlm[0] = "https://"+ RC + urlm[0]
			AddDir(name3 +" "+namem ,urlm[0], 133, iconimage, iconimage, info="", isFolder=False, IsPlayable=True)
# ----------------- FIM REDECANAIS SERIES,ANIMES,DESENHOS
# ----------------- #BUSCA
def Busca(): #160
	AddDir("[COLOR pink][B][Nova Busca][/B][/COLOR]", "" , 50 ,"", isFolder=False)
	d = xbmcgui.Dialog().input("Busca (poder demorar a carregar os resultados)").replace(" ", "+")
	#d = "orfa"
	d = quote_plus(d)
	progress = xbmcgui.DialogProgress()
	progress.create('Buscando...')
	progress.update(0, "Redecanais")
	if not d:
		return Categories()
		sys.exit(int(sys.argv[1]))
	'''try:
		p= 1
		AddDir("[COLOR blue][B][RedeCanais][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		l= 0
		for x in range(0, 5):
			link = OpenURL("https://www.google.com/search?q="+d+"+site:redecanais.cloud&hl=pt-BR&&start="+str(l))
			l +=10
			match = re.compile('href\=\"(https?\:.{0,50}redecanais[^\"]+)\".{50,200}\>([^\<]+)').findall(link.replace('\n','').replace('\r',''))
			if match:
				for url2,name2 in match:
					if "lista" in url2 or "Lista" in name2:
						AddDir("[COLOR blue]" +name2+ "[/COLOR]" ,url2, 135, " ", " ", info="", isFolder=True, IsPlayable=False)
					else:
						AddDir("[COLOR blue]" +name2+ "[/COLOR]" ,url2, 96, " ", " ", info="", isFolder=False, IsPlayable=True)
	except:
		pass'''
	try:
		p= 1
		AddDir("[COLOR blue][B][RedeCanais][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		l= 0
		for x in range(0, 20):
			l +=1
			progress.update(int(l*10/2),"Redecanais "+str(l*10/2)+"%")
			#AddDir("[COLOR blue]" +str(l)+ "[/COLOR]" ,"", 135, "", "")
			link = OpenURL(proxy+"https://" + RC +"search.php?keywords="+d+"&page="+str(l))
			match = re.compile('data\-echo\=\"([^\"]+).{10,150}href=\"([^\"]+).{0,10}title=\"([^\"]+)\"').findall(link.replace('\n','').replace('\r',''))
			if match:
				for img2,url2,name2 in match:
					#url2 = re.sub('^\.', "http://www." + RC, url2 )
					url2 = "https://" + RC + url2
					img2 = re.sub('^/', "https://"+RC, img2 )
					if re.compile('\d+p').findall(name2):
						if cPlayD == "true":
							AddDir("[COLOR blue]" +name2+ "[/COLOR]" ,url2, 96, img2, img2, info="", isFolder=False, IsPlayable=True)
						else:
							AddDir("[COLOR blue]" +name2+ "[/COLOR]" ,url2, 95, img2, img2)
					elif "Lista" in name2:
						AddDir("[COLOR blue]" +name2+ "[/COLOR]" ,url2, 135, img2, img2)
			else:
				break
	except:
		pass
	progress.update(100, "Netcine")
	try:
		AddDir("[COLOR yellow][B][NetCine.us][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		link2 = OpenURL("http://netcine.biz/?s="+d).replace('\n','').replace('\r','')
		lista = re.compile("img src\=\"([^\"]+).+?alt\=\"([^\"]+).+?f\=\"([^\"]+)").findall(link2)
		for img2,name2,url2 in lista:
			if name2!="Close" and name2!="NetCine":
				name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
				img2 = re.sub('-120x170.(jpg|png)', r'.\1', img2 )
				if "tvshows" in url2:
					AddDir("[COLOR yellow]" +name2+ "[/COLOR]",url2, 61, img2, img2, isFolder=True)
				else:
					AddDir("[COLOR yellow]" +name2+ "[/COLOR]",url2, 78, img2, img2, isFolder=True)
	except:
		pass
	'''progress.update(66, "66%", "MMfilmes", "")
	l=0
	i=0
	try:
		AddDir("[COLOR cyan][B][MMfilmes.tv][/B][/COLOR]", "" , 0 ,"", isFolder=False)
		links = OpenURL("http://www.mmfilmes.tv/series/")
		ms = re.compile('href\=\"(.+www.mmfilmes.tv.+)\" rel\=\"bookmark\"').findall(links)
		for x in range(0, 3):
			l+=1
			link = OpenURL("http://www.mmfilmes.tv/page/"+str(l)+"/?s="+d)
			m = re.compile('id\=\"post\-\d+\".+?\=.([^\"]+)\h*(?s)(.+?)(http[^\"]+)').findall(link)
			res = re.compile('audioy..([^\<]*)').findall(link)
			jpg = re.compile('src=\"(http.+?www.mmfilmes.tv\/wp-content\/uploads[^\"]+)').findall(link)
			dubleg = re.compile('boxxer.+\s.+boxxer..([^\<]*)').findall(link)
			if m:
				for name2,b,url2 in m:
					name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
					if not url2 in ms:
						AddDir("[COLOR cyan]" +name2+ "[/COLOR] [COLOR yellow]"+res[i]+"[/COLOR] [COLOR blue]"+dubleg[i]+"[/COLOR]", url2, 181, jpg[i], jpg[i],isFolder=True,IsPlayable=False)
					else:
						AddDir("[COLOR cyan]" +name2+ "[/COLOR]", url2, 191, jpg[i], jpg[i], isFolder=True,IsPlayable=False)
					i+=1
			i=0
	except:
		pass'''
	''' progress.update(75, "75%", " SuperFlix", "")
	AddDir("[COLOR lightgreen][B][Superflix][/B][/COLOR]", "" , 0 ,"", isFolder=False)
	for x in range(1, 5):
		try:
			l = OpenURL("http://www.superflix.net/page/"+str(x)+"/?s="+d)
			m = re.compile('li class\=\"TPostMv\"(.+?)\<.li\>').findall(l)
			for ll in m:
				mm = re.compile('href\=\"([^\"]+).{1,150}src=\"([^\"]+).{1,200}.alt\=\"([^\"]+).{1,50}class\=\"([^\"]+)').findall(ll)
				for url2,img2,name2,tvmovie in mm:
					img2 = "http:"+img2 if not "http" in img2 else img2
					name2 = name2.replace("#038;","").replace("&#8211;","-").replace("Imagem ","")
					if "itle" in tvmovie:
						AddDir("[COLOR lightgreen]"+name2+"[/COLOR]", url2, 405, img2, img2,isFolder=False,IsPlayable=True)
					else:
						AddDir("[COLOR lightgreen]"+name2+"[/COLOR]", url2, 402, img2, img2,isFolder=True,IsPlayable=False)
		except:
			pass '''
	progress.update(100)
	progress.close()
	#l=0
	#i=0
	#try:
	#	AddDir("[COLOR maroon][B][Gofilmes.me][/B][/COLOR]", "" , 0 ,"", isFolder=False)
	#	for x in range(0, 3):
	#		l+=1
	#		link = OpenURL("http://gofilmes.me/search?s="+d+"&p="+str(l)).replace("</div><div","\r\n")
	#		m = re.compile('href=\"([^\"]+)\" title\=\"([^\"]+).+b\" src\=\"([^\"]+).+').findall(link)
	#		for url2,name2,img2 in m:
	#			AddDir(name2, url2, 211, img2, img2, isFolder=False, IsPlayable=True)
	#except:
	#	pass
# ----------------- FIM BUSCA
# ----------------- TV Cubeplay
def PVR(): #109
	try:
		l = OpenURL("https://pastebin.com/raw/icwdED6L")
		Path = re.sub('Addons', 'userdata', addonDir, flags=re.IGNORECASE)
		Path = re.sub('plugin.video.CubePlay', '', Path, flags=re.IGNORECASE)
		Path = os.path.join( Path, "addon_data")
		Path = os.path.join( Path, "pvr.iptvsimple")
		Path = os.path.join( Path, "settings.xml")
		file = open(Path, "w")
		file.write(l)
		NF("Configurado. Reinicie o Kodi")
	except:
		NF("Instale o addon PVR Simple Client")
		pass
def TVCB(x): #102
	if "imdb" in cadulto:
		AddDir("Drive Test", "plugin://plugin.video.crunchyroll/?plotoutline=1&tvshowtitle=D&aired=2&episode_id=799907&series_id=2&duration=1&collection_id=2&plot=.&episode=799907&thumb=g&title=D&fanart=g&premiered=2&mode=videoplay&playcount=0&status=Continuing&season=0&studio=T&genre=anime", 3, "", "", isFolder=False, IsPlayable=True, info="")
	#AddDir("reload", "", 50, "", "", isFolder=False, IsPlayable=False, info="")
	AddDir("Configurar PVR Simple Client", "", 109, "", "", isFolder=False, IsPlayable=False, info="")
	link = OpenURL("https://pastebin.com/raw/a5aLGgim").replace("\r\n","")
	if cadulto!="8080":
		link = re.sub('Adulto.+', "", link)
	m = re.compile('url="(.+?)".mg="(.+?)".ame="(.+?)"').findall(link)
	#ST(link)
	#ST(m)
	for url2,img2,name2 in m:
		AddDir(name2 , url2, 103, img2, img2, isFolder=False, IsPlayable=True)
	#try:
	#AddDir("Play", m[0], 50, "", "", isFolder=False, IsPlayable=True, info="")
	#	link = OpenURL(x)
	#	link = re.sub('^.{3}', "", link )
	#	m = re.compile('(.+)\?(.+)').findall(link)
	#	i=0
	#	for name2,url2 in m:
	#		if cadulto=="8080":
	#			AddDir(getmd5(name2), url2, 103, " ", " ", isFolder=False, IsPlayable=True, info="")
	#			i+=1
	#		elif not "dulto" in getmd5(name2):
	#			AddDir(getmd5(name2), url2, 103, " ", " ", isFolder=False, IsPlayable=True, info="")
	#			i+=1
	#except:
	#	AddDir("Servidor offline, tente novamente em alguns minutos" , "", 0, "", "", 0)
def PlayTVCB(): #103
	#link = OpenURL("https://redecanais.cloud/player3/serverf4-bk.php?vid=JRSCWRLDRNOAMCDO", headers={'referer': "https://homeingles.com/"})
	#ST(link)
	#return
	try:
		link = OpenURL("https://redecanaistv.com/"+url)
		#link = OpenURL("https://canaisgratis.top/assistir-max-prime-online-24-horas-ao-vivo_8586fbbe2.html")
		player = re.compile('<iframe.{1,50}src=\"([^\"]+)\"').findall(link)
		player = re.sub('^/', "https://homeingles.fun/" , player[0] )
		player = re.sub('.php', "hlb.php", player )
		#if "canal=" in url:
		#	c = re.compile('canal\=(.+)').findall(url)
		#	player = re.sub('canal=bbb', "canal="+c[0], "https://redecanaistv.com" )
		#player = re.sub('\.php', "hlb.php", player)
		m3u = OpenURL(player,headers={'referer': "https://homeingles.fun/"})
		m = re.compile('[^"|\']+m3u8[^"|\']*').findall(m3u)
		#m[0] = re.sub('https', 'http', m[0] )
		m[0] = re.sub( '\'|"', '', m[0] )
		#PlayUrl(name, m[0] + "|Referer=https://homeingles.fun&Connection=Keep-Alive&Accept-Language=en&User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0", iconimage, name, "")
		#link3 = OpenURL("http://cbplay.000webhostapp.com/rc/_grc.php?u="+m[0])
	except:
		NF("erro")
	PlayUrl(name, m[0] + "|Referer=https://homeingles.fun&Connection=Keep-Alive&Accept-Language=en&User-Agent=Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0", iconimage, name, "")
	#ST(m[0])
	#AddDir("play", m[0] + "?play|Referer=https://cometa.top", 3, isFolder=False, IsPlayable=True, info="")
	
	#AddDir("Play", m[0], 50, "", "", isFolder=False, IsPlayable=True, info="")
	#try:
	#	PlayUrl(name, getmd5(url), "", "", "")
	#except:
	#	xbmcgui.Dialog().ok('Cube Play', "Servidor offline, tente novamente em alguns minutos")
# ----------------- Fim TV Cubeplay
# ----------------- REDECANAIS TV
def Acento(x):
	x = x.replace("\xe7","ç").replace("\xe0","à").replace("\xe1","á").replace("\xe2","â").replace("\xe3","ã").replace("\xe8","è").replace("\xe9","é").replace("\xea","ê").replace("\xed","í").replace("\xf3","ó").replace("\xf4","ô").replace("\xf5","õ").replace("\xfa","ú")
	return x
def TVRC(): #100
	AddDir("[COLOR maroon]Reload[/COLOR]" , "", 50, isFolder=False)
	#import ssl
	#request = urllib2.Request("https://51.178.220.155/ch.php?usercode=6017538676")
	#request = urllib2.Request("http://s1.top2.ws/v21/ch.php?usercode=885457698421&pid=1&mac=48EC30E11015&sn=70313044&customer=google&lang=eng&cs=amlogic&check=3983743268")
	#request = urllib2.Request("http://satv.itvhotline.info/dqtv/eliptv_portal.php?a=get_list&p=fa8bfb8f8a8efdfbf68283f3b887f486fcfff98888fb8d8ee0adbebaa2b0b8")
	#t = urllib2.urlopen(request, context=ssl._create_unverified_context()).read()
	t = OpenURL("http://satv.itvhotline.info/dqtv/eliptv_portal.php?a=get_list&p=fa8bfb8f8a8efdfbf68283f3b887f486fcfff98888fb8d8ee0adbebaa2b0b8")
	jq_ = json.loads(t)
	try:
		jq = sorted(jq_['channel_info'], key=lambda jq_: jq_['name'])
	except:
		jq = jq_['channel_info']
	#ST(jq)
	#return
	#ST(jq[0])
	for jq1 in jq:
		if not "SD" in jq1['name']:
			try:
				AddDir( "[COLOR white]" + jq1['name'] + "[/COLOR]", jq1['id'] , 101, jq1['icon'], jq1['icon'], isFolder=False, IsPlayable=True, info="")
				#ST('#EXTINF:-1 tvg-ID="" tvg-name="" tvg-logo="'+jq1['logo']+'" group-title="Brasil (1)", '+jq1['name']+ ' (1)', "1")
				#ST("\n", "1")
				#ST("plugin://plugin.video.CubePlay/?info=&logos=&metah=&cache=0&name="+quote_plus(jq1['name'])+"&background=None&url="+quote_plus(jq1['id'])+"&iconimage=&mode=101", "1")
				#ST("\n", "1")
			except:
				pass

def PlayTVRC(): #101
	t = OpenURL("http://satv.itvhotline.info/dqtv/eliptv_portal.php?a=get_list&p=fa8bfb8f8a8efdfbf68283f3b887f486fcfff98888fb8d8ee0adbebaa2b0b8")
	jq_ = json.loads(t)
	for jq1 in jq_['channel_info']:
		if jq1['id'] == url:
			PlayUrl(jq1['name'], jq1['url'],jq1['icon'],"")
# ----------------- FIM REDECANAIS TV
# ----------------- Inicio Filmes Online
def GenerosFO(): #85
	global Cat
	d = xbmcgui.Dialog().select("Escolha o Genero", Clistafo1)
	if d != -1:
		Addon.setSetting("Catfo", str(d) )
		Cat = d
		Addon.setSetting("cPagefo1", "0" )
		xbmc.executebuiltin("Container.Refresh()")
		
def MoviesFO(urlfo,pagina2): #170
	AddDir("[COLOR yellow][B][Gênero dos Filmes]:[/B] " + Clistafo1[int(Catfo)] +"[/COLOR]", "url" ,85 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	CategoryOrdem("cOrdFO")
	try:
		pagina=eval(pagina2)
		l= int(pagina)*5
		p= 1
		if int(pagina) > 0:
			AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
		for x in range(0, 5):
			l +=1
			ordem = "asc" if cOrdFO=="title" else "desc"
			link = OpenURL("https://filmesonline.online/index.php?do=search&subaction=search&search_start="+str(l)+"&story="+urlfo+"&sortby="+cOrdFO+"&resorder="+ordem+"&catlist[]="+Clistafo0[int(Catfo)]).replace("\r","").replace("\r\n","")
			link = re.sub('Novos Filmes.+', '', link)
			m = re.compile('src=\"(.upload[^\"]+).+?alt=\"([^\"]+).+?href=\"([^\"]+)').findall(link)
			m2 = re.compile('numb-serial..(.+?)\<.+?afd..(\d+)').findall(link)
			i=0
			if m:
				#xbmcgui.Dialog().ok('Cube Play', str(m))
				for img2,name2,url2 in m:
					AddDir(name2 + " ("+m2[i][0]+") - " + m2[i][1], url2, 171, "https://filmesonline.zone/"+img2, "https://filmesonline.zone/"+img2, info="", background=url)
					p+=1
					i+=1
		if p >= 80:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except:
		AddDir("Server error, tente novamente em alguns minutos" , "", 0, "", "")
		
def PlayMFO1(): #172
	global background
	if re.compile('\d+').findall(str ( background )) :
		s = background.split(",")
		sel = xbmcgui.Dialog().select("Selecione a resolução", s)
		if sel!=-1:
			link = OpenURL(url+"?q="+s[sel] )
			#ST(link)
			m = re.compile('https[^\"]+\.mp4').findall(link)
			background="None"
			PlayUrl(name, m[0],"",info)
	else:
		link = OpenURL(url)
		m = re.compile('https[^\"]+\.mp4').findall(link)
		background = "None"
		PlayUrl(name, m[0],"",info)
		
def GetMFO1(): #171
	try:
		link = OpenURL( url )
		m = re.compile('href\=\"(.+?\#Rapid)').findall(link)
		t = re.compile('class=\"titleblock\"\>\s\<h1\>([^\<]+)').findall(link)
		i = re.compile('class=\"p-info-text\"\>\s\<span\>([^\<]+)').findall(link)
		if m:
			link2 = OpenURL( "https://filmesonline.online"+m[0] )
			m2 = re.compile('iframe.+?src\=\"([^\"]+)').findall(link2)
			#ST(m2)
			if m2:
				title = t[0] if t else name
				info = i[0] if i else ""
				link3 = OpenURL("https:"+m2[0] )
				#ST(link3 )
				m3 = re.compile('https[^\"]+\.mp4').findall(link3)
				if m3:
					pp = re.compile('q=(\d+p)').findall(link3)
					pp = list(reversed(pp))
					AddDir( title , "https:"+m2[0], 172, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info, background= ",".join(pp))
					AddDir( "Resoluções: "+", ".join(pp), "https:"+m2[0], 0, iconimage, iconimage, isFolder=False, info="Clique no título do filme para dar play")
				else:
					AddDir( "Video offline!!" ,"", 0, "", "", isFolder=False)
	except:
		AddDir( "Video offline" ,"", 0, "", "", isFolder=False)
# ----------------- FIM Filmes Online
# ----------------- Inicio MM filmes
def GenerosMM(): #189
	global Cat
	d = xbmcgui.Dialog().select("Escolha o Genero", ClistaMM1)
	if d != -1:
		Addon.setSetting("CatMM", str(d) )
		Cat = d
		Addon.setSetting("cPageMMf", "0" )
		xbmc.executebuiltin("Container.Refresh()")
def ListFilmeLancMM(): #184
	l=0
	i=0
	try:
		links = OpenURL("http://www.mmfilmes.tv/series/")
		ms = re.compile('href\=\"(.+www.mmfilmes.tv.+)\" rel\=\"bookmark\"').findall(links)
		for x in range(0, 5):
			l+=1
			link = OpenURL("http://www.mmfilmes.tv/ultimos/page/"+str(l)+"/")
			m = re.compile('id\=\"post\-\d+\".+?\=.([^\"]+)\h*(?s)(.+?)(http[^\"]+)').findall(link)
			res = re.compile('audioy..([^\<]*)').findall(link)
			jpg = re.compile('src=\"(http.+?www.mmfilmes.tv\/wp-content\/uploads[^\"]+)').findall(link)
			dubleg = re.compile('boxxer.+\s.+boxxer..([^\<]*)').findall(link)
			if m:
				for name2,b,url2 in m:
					name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
					if not url2 in ms:
						AddDir(name2+ " [COLOR yellow]"+res[i]+"[/COLOR] [COLOR blue]"+dubleg[i]+"[/COLOR]", url2, 181, jpg[i], jpg[i],isFolder=True,IsPlayable=False)
					i+=1
			i=0
	except:
		pass
def ListFilmeMM(pagina2): #180
	AddDir("[COLOR yellow][B][Gênero dos Filmes]:[/B] " + ClistaMM1[int(CatMM)] +"[/COLOR]", "url" ,189 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	pagina=eval(pagina2)
	l= int(pagina)*5
	p=1
	i=0
	if int(pagina) > 0:
		AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
	try:
		links = OpenURL("http://www.mmfilmes.tv/series/")
		ms = re.compile('href\=\"(.+www.mmfilmes.tv.+)\" rel\=\"bookmark\"').findall(links)
		for x in range(0, 5):
			l+=1
			link = OpenURL("http://www.mmfilmes.tv/category/"+ ClistaMM0[int(CatMM)] +"/page/"+str(l)+"/")
			m = re.compile('id\=\"post\-\d+\".+?\=.([^\"]+)\h*(?s)(.+?)(http[^\"]+)').findall(link)
			res = re.compile('audioy..([^\<]*)').findall(link)
			jpg = re.compile('src=\"(http.+?www.mmfilmes.tv\/wp-content\/uploads[^\"]+)').findall(link)
			dubleg = re.compile('boxxer.+\s.+boxxer..([^\<]*)').findall(link)
			if m:
				for name2,b,url2 in m:
					name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
					if not url2 in ms:
						AddDir(name2+ " [COLOR yellow]"+res[i]+"[/COLOR] [COLOR blue]"+dubleg[i]+"[/COLOR]", url2, 181, jpg[i], jpg[i],isFolder=True,IsPlayable=False)
					i+=1
					p+=1
			i=0
			if p >= 50:
				AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except:
		pass
def OpenLinkMM(): #181
	link = OpenURL(url)
	m = re.compile('boxp\(.([^\']+)').findall(link)
	info2 = re.compile('mCSB_container..\s(\h*(?s)(.+?))\<\/div').findall(link)
	info2= info2[0][0].replace("\t","") if info2 else ""
	if m:
		link2 = OpenURL(m[0],headers={'referer': "http://www.mmfilmes.tv/"})
		m2 = re.compile('opb\(.([^\']+).+?.{3}.+?[^\\>]+.([^\<]+)').findall(link2)
		if m2:
			name2 = re.sub(' \[.+', '', name )
			for link,dubleg in m2:
				AddDir( name2 +" [COLOR blue]("+dubleg+")[/COLOR]" ,link, 182, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info2, background=url)
def PlayLinkMM(): #182
	global background
	link = OpenURL(url,headers={'referer': "http://www.mmfilmes.tv/"})
	m = re.compile('addiframe\(\'([^\']+)').findall(link)
	if m:
		try:
			m[0] = "https://player.mrhd.tv/" + m[0] if not "http" in m[0] else m[0]
			link2 = OpenURL(re.sub('(\/.{1,25}\/).{1,10}\/', r'\1', m[0]),headers={'referer': "http://player.mmfilmes.tv"}).replace("file","\nfile")
			m2 = re.compile('file.+?(h[^\']+).+?(\d+p)\'').findall(link2)
			legenda = re.compile('([^\']+\.(vtt|srt|sub|ssa|txt|ass))').findall(link2)
			listar=[]
			listal=[]
			for link,res in m2:
				listal.append(link)
				listar.append(res)
			if len(listal) <1:
				xbmcgui.Dialog().ok('Cube Play', 'Erro, video não encontrado')
				sys.exit(int(sys.argv[1]))
			d = xbmcgui.Dialog().select("Selecione a resolução", listar)
			if d!= -1:
				url2 = re.sub(' ', '%20', listal[d] )
				background=background+";;;"+name+";;;MM"
				if legenda:
					legenda = re.sub(' ', '%20', legenda[0][0] )
					if not "http" in legenda:
						legenda = "https://player.mrhd.tv/" + legenda
					PlayUrl(name, url2, iconimage, info, sub=legenda)
				else:
					PlayUrl(name, url2, iconimage, info)
		except:
			xbmcgui.Dialog().ok('Cube Play', 'Erro, servidor offline')
			sys.exit()
# -----------------
def ListSerieMM(): #190
	try:
		link = OpenURL("http://www.mmfilmes.tv/series/")
		m = re.compile('id\=\"post\-\d+\".+?\=.([^\"]+)\h*(?s)(.+?)(http[^\"]+)').findall(link)
		jpg = re.compile('src=\"(http.+?www.mmfilmes.tv\/wp-content\/uploads[^\"]+)').findall(link)
		i=0
		m2=[]
		if m:
			for name2,b,url2 in m:
				m2.append([name2,url2,jpg[i]])
				i+=1
			m2 = sorted(m2, key=lambda m2: m2[0])
			for name2,url2,jpg2 in m2:
				name2 = name2.replace("&#8211;","-").replace("&#038;","&").replace("&#8217;","\'")
				AddDir(name2, url2, 191, jpg2, jpg2, isFolder=True,IsPlayable=False)
	except:
		AddDir( "Server offline" ,"", 0, "", "", isFolder=False)
def ListSMM(x): #191
	link = OpenURL(url)
	m = re.compile('boxp\(.([^\']+)').findall(link)
	info2= re.compile('mCSB_container..\s(\h*(?s)(.+?))\<\/div').findall(link)
	info2= info2[0][0].replace("\t","") if info2 else ""
	i=0
	if m:
		if x=="None":
			link2 = OpenURL(m[0],headers={'referer': "http://www.mmfilmes.tv/"})
			m2 = re.compile('opb\(.([^\']+).+?.{3}.+?[^\\>]+.([^\<]+)').findall(link2)
			listar=[]
			listal=[]
			for link,res in m2:
				listal.append(link)
				listar.append(res)
			if len(listar)==1:
				d=0
			else:
				d = xbmcgui.Dialog().select("Selecione o server:", listar)
			if d== -1:
				d= 0
			if m2:
				link3 = OpenURL(m2[0][0],headers={'referer': "http://www.mmfilmes.tv/"}).replace("\r\n","").replace("\r","").replace('".Svplayer"',"<end>").replace('\t'," ")
				link3 = re.sub('(\(s \=\= \d+\))', r'<end>\1', link3 )
				m3 = re.compile('s \=\= (\d+)(.+?\<end\>)').findall(link3)
				for temp in m3:
					AddDir("[B][Temporada "+ temp[0] +"][/B]" ,listal[d], 192, iconimage, iconimage, isFolder=True, info=info2, background=i)
					i+=1
def ListEpiMM(x): #192
	link3 = OpenURL(url,headers={'referer': "http://www.mmfilmes.tv/"}).replace("\r\n","").replace("\r","").replace('".Svplayer"',"<end>").replace('\t'," ")
	link3 = re.sub('(\(s \=\= \d+\))', r'<end>\1', link3 )
	m3 = re.compile('s \=\= (\d+)(.+?\<end\>)').findall(link3)
	r=-1
	p=1
	dubleg = re.compile("t \=\= \'([^\']+)(.+?\})").findall( m3[int(x)][1] )
	epi = re.compile("e \=\= (\d+).+?addiframe\(\'([^\']+)").findall( m3[int(x)][1] )
	for e,url2 in epi:
		url2 = "https://player.mrhd.tv/" + url2 if not "http" in url2 else url2
		if p == int(e) :
			r+=1
		if len(dubleg[r][1]) < 30:
			r+=1
		name2 = "[COLOR yellow](Dub)[/COLOR]" if "dub" in dubleg[r][0] else "[COLOR blue](Leg)[/COLOR]"
		AddDir("Episódio "+ e + " [COLOR blue]" + name2 ,url2, 194, iconimage, iconimage, isFolder=False, IsPlayable=True, info=info)
def PlaySMM(): #194
	if "drive.google" in url:
		#xbmcgui.Dialog().ok('Cube Play', 'Erro, video não encontrado, drive')
		PlayUrl(name, "plugin://plugin.video.gdrive?mode=streamURL&amp;url="+url.encode('utf-8'), iconimage, info)
		sys.exit()
	cdn = re.compile('(\d+)\=(.+?.mp4)|\&l\=(.+)').findall(url)
	if cdn:
		cdn = list(reversed(cdn))
		listar=[]
		listal=[]
		legenda=""
		for res,link,leg in cdn:
			if link != "":
				listal.append(link)
				listar.append(res)
			if leg:
				legenda = leg
				if not "http" in legenda:
					legenda = "https://player.mrhd.tv/" + legenda
				legenda = re.sub(' ', '%20', legenda )
		d = xbmcgui.Dialog().select("Selecione a resolução, cdn", listar)
		if d!= -1:
			url2 = re.sub(' ', '%20', listal[d] )
			PlayUrl(name, url2, iconimage, info, sub=legenda)
	else:
		link2 = OpenURL( re.sub('(\/.{1,25}\/).{1,10}\/', r'\1', url) ,headers={'referer': "http://player.mmfilmes.tv"}).replace('"',"'")
		m2 = re.compile('(h[^\']+).+?label...(\w+)').findall(link2)
		legenda = re.compile('([^\']+\.(vtt|srt|sub|ssa|txt|ass))').findall(link2)
		listar=[]
		listal=[]
		for link,res in m2:
			listal.append(link)
			listar.append(res)
		if len(listal) < 1:
			xbmcgui.Dialog().ok('Cube Play', 'Erro!')
			sys.exit(int(sys.argv[1]))
		d = xbmcgui.Dialog().select("Selecione a resolução", listar)
		if d!= -1:
			url2 = re.sub(' ', '%20', listal[d] )
			if legenda:
				legenda = re.sub(' ', '%20', legenda[0][0] )
				if not "http" in legenda:
					legenda = "http://player.mmfilmes.tv/" + legenda
				PlayUrl(name, url2, iconimage, info, sub=legenda)
			else:
				PlayUrl(name, url2, iconimage, info)
# ----------------- Fim MM filmes
# ----------------- Inicio Go Filmes
def GenerosGO(): #219
	global Cat
	d = xbmcgui.Dialog().select("Escolha o Genero", ClistaGO1)
	if d != -1:
		Addon.setSetting("CatGO", str(d) )
		Cat = d
		Addon.setSetting("cPageGOf", "0" )
		xbmc.executebuiltin("Container.Refresh()")
def ListGO(pagina2): #210
	AddDir("[COLOR yellow][B][Gênero dos Filmes]:[/B] " + ClistaGO1[int(CatGO)] +"[/COLOR]", "url" ,219 ,"https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", "https://lh5.ggpht.com/gv992ET6R_InCoMXXwIbdRLJczqOHFfLxIeY-bN2nFq0r8MDe-y-cF2aWq6Qy9P_K-4=w300", isFolder=False)
	pagina=eval(pagina2)
	l= int(pagina)*5
	p=1
	i=0
	if int(pagina) > 0:
		AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background=pagina2)
	try:
		for x in range(0, 5):
			l+=1
			if ClistaGO0[int(CatGO)] == "all":
				link = OpenURL("http://gofilmes.me/?p="+str(l)).replace("</div></div>","\r\n")
			else:
				link = OpenURL("http://gofilmes.me/genero/"+ClistaGO0[int(CatGO)]+"?p="+str(l)).replace("</div></div>","\r\n")
			m = re.compile('href=\"([^\"]+)\" title\=\"([^\"]+).+b\" src\=\"([^\"]+).+n\">([^\<]+)').findall(link)
			for url2,name2,img2,info2 in m:
				info2= html.unescape(info2)
				name2 = name2.replace("Assistir ","").replace(" Online"," -")
				AddDir(name2, url2, 211, img2, img2, isFolder=False, IsPlayable=True, info=info2)
				p+=1
		if p >= 120:
			AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background=pagina2)
	except:
		AddDir( "Server offline" ,"", 0, "", "", isFolder=False)
def PlayGO(): #211
	try:
		link = OpenURL(url)
		m = re.compile('iframe src\="([^\"]+)').findall(link)
		link2 = OpenURL(m[0])
		m2 = re.compile('href=\"([^\"]+)\".+?\"\>([^\<]+)').findall(link2)
		listu=[]
		listn=[]
		i=0
		for url3,dl3 in m2:
			link3 = OpenURL("http://sokodi.net/play/moon.php?url="+url3)
			m3 = re.compile('\=(.+?x[^,]+).+\s(.+)').findall(link3)
			m3 = sorted(m3, key=lambda m3: m3[0])
			for res4,url4 in m3:
				listn.append("[COLOR blue]"+ m2[i][1] +"[/COLOR] " + "[COLOR yellow]"+ res4 +"[/COLOR]")
				listu.append(url4)
			i+=1
		if len(listn) >=1:
			d = xbmcgui.Dialog().select("Selecione a resolução", listn)
			if d!= -1:
				PlayUrl(name, listu[d], iconimage, info)
		else:
			xbmcgui.Dialog().ok("Cube Play", "Não foi possível carregar o vídeo")
	except:
		xbmcgui.Dialog().ok("Cube Play", "Não foi possível carregar o vídeo")
# ----------------- Fim Go Filmes
# ----------------- Inicio Superflix
def ListSerieSF(): #401:
	pagina = "0" if not cPageserSF else cPageserSF
	if int(pagina) > 0:
		AddDir("[COLOR blue][B]<< Pagina Anterior ["+ str( int(pagina) ) +"[/B]][/COLOR]", pagina , 120 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Previous-icon.png", isFolder=False, background="cPageserSF")
	y= int(pagina)*5
	for x in range(0, 5):
		try:
			y +=1
			l = OpenURL("http://www.superflix.net/assistir-series-online/page/"+str(y))
			m = re.compile('li class\=\"TPostMv\"(.+?)\<.li\>').findall(l)
			for ll in m:
				mm = re.compile('href\=\"([^\"]+).{1,150}src=\"([^\"]+).{1,200}itle\"\>([^\<]+).{1,150}ear\"\>([^\<]+)').findall(ll)
				for url2,img2,name2,year2 in mm:
					img2 = "http:"+img2 if not "http" in img2 else img2
					name2 = name2.replace("#038;","").replace("&#8211;","-")
					AddDir(name2+" ("+year2+")", url2, 402, img2, img2,isFolder=True,IsPlayable=False)
		except:
			pass
	AddDir("[COLOR blue][B]Proxima Pagina >> ["+ str( int(pagina) + 2) +"[/B]][/COLOR]", pagina , 110 ,"http://icons.iconarchive.com/icons/iconsmind/outline/256/Next-2-2-icon.png", isFolder=False, background="cPageserSF")
def ListTempSF(): #402
	l = OpenURL(url).replace("\r\n","").replace("\r","")
	m = re.compile('Temporada ?.{5,6}(\d+)(.+?)\<\/Season\>').findall(l)
	for temp2,cont2 in m:
		AddDir("Temporada "+ temp2 +" [COLOR lightgreen][SF][/COLOR]" ,cont2, 403, iconimage, iconimage, isFolder=True)
def ListEpiSF(): #403
	epis = re.compile('Num.{1,2}(\d+).+?(http:[^\"]+)').findall(url)
	#ST(url)
	for E,url2 in epis:
		AddDir("Episódio "+E,url2, 405, iconimage, iconimage, isFolder=False, IsPlayable=True)
def ListMovieSF(): #411:
	for x in range(1, 11):
		try:
			l = OpenURL("http://www.superflix.net/categoria/assistir-filmes-lancamentos-2019-online/page/"+str(x))
			m = re.compile('li class\=\"TPostMv\"(.+?)\<.li\>').findall(l)
			for ll in m:
				mm = re.compile('href\=\"([^\"]+).{1,100}src=\"([^\"]+).{1,100}itle\"\>([^\<]+).{1,100}ear\"\>([^\<]+)').findall(ll)
				for url2,img2,name2,year2 in mm:
					img2 = "http:"+img2 if not "http" in img2 else img2
					name2 = name2.replace("#038;","").replace("&#8211;","-")
					AddDir(name2+" ("+year2+")", url2, 405, img2, img2,isFolder=False,IsPlayable=True)
		except:
			pass
# -----------------
def PlaySSF(): #405
	try:
		l = OpenURL(url)
		m = re.compile("\<iframe.{1,100}src\=\"([^\"]+trid[^\"]+)").findall(l)
		trem = re.compile("http.{10,50}trembed[^\"| ]+").findall(l)
		legsub = re.compile("data-tplayernv.+?<span>([^\<]+)").findall(l.replace("<span>SuperFlix</span>",""))
		if not legsub:
			xbmcgui.Dialog().ok('Cube Play', "Episódio ainda não disponível")
			sys.exit()
		if len(legsub) == 1:
			d = 0
		else:
			d = xbmcgui.Dialog().select("Escolha:", legsub)
		if not d == -1:
			trem2 = trem[d].replace("#038;","").replace("&amp;","&")
			l2 = OpenURL(trem2)
			m2 = re.compile("(http.+?(\w{28,35}))").findall(l2)
			msub = re.compile("vlsub\=([^\"|?]+)").findall(l2)
			if not m2:
				PlaySSF2(l2)
				sys.exit()
		leg = "https://sub.sfplayer.net/subdata/"+msub[0] if msub else ""
		mp4 = RetLinkSF(m2[0][0],m2[0][1])
		if not mp4:
			sys.exit()
		mp4m = re.compile("RESOLUTION\=.+x([^\s]+)\n(.+)").findall(mp4[1])
		if not mp4m:
			mp42 = mp4[0]+"/hls/"+m2[0][1]+".playlist.m3u8"
			PlayUrl(name, mp42, iconimage, info, sub=leg)
			sys.exit()
		#mp4m.sort()
		mp4m = sorted(mp4m, key=lambda k: k[0], reverse=True)
		mp4r=[]
		mp4u=[]
		for res2,url2 in mp4m:
			mp4r.append(res2.replace("999","1080")+"p")
			mp4u.append(url2)
		d2 = xbmcgui.Dialog().select("Escolha a resolução:", mp4r)
		if not d2 == -1:
			NF("plus")
			#ST("http://pat-197972:8080/sf/merge2.php?l="+mp4[0]+mp4u[d2]+"&sub="+leg)
			v = baixarsf(mp4[0]+mp4u[d2])
			if v:
				PlayUrl(name, v, iconimage, info, sub=leg)
		system.exit()
		#PlayUrl(name, "plugin://plugin.video.gdrive?mode=streamURL&amp;url="+"https://slave2.sfplayer.net/hls/a6ebb20cd567cc52309a965ee2cd82b7.playlist.m3u8", iconimage, info, sub=leg)
	except:
		sys.exit()
def RetLinkSF(link,x):
	plus = "hls"
	for s in range(1, 8):
		x2 = "https://lbhls.sfplayer.net/hls/"+x+"/"+x+".m3u8"
		ST(x2)
		try:
			NF(s,t=500)
			l = OpenURL(x2, headers={'referer': "https://www.superflix.net/"})
			if len(l) > 20:
				return ["https://slave"+str(s)+plus+".sfplayer.net",l.replace("1080","999")]
		except:
			NF("offline")
			return ""
def PlaySSF2(x):
	api = re.compile("http[^\"]+api[^\"]+").findall(x)
	if not api:
		sys.exit()
	l = OpenURL(api[0])
	m = re.compile("iframe.{1,10}(http[^\"]+api[^\"]+)").findall(l)
	l2 = OpenURL(m[0])
	m2 = re.compile('http[^\"]+file.{1,5}\/([^\/"]+)').findall(l2)
	url2 = "https://drive.google.com/file/d/"+m2[0]+"/edit"
	PlayUrl(name, "plugin://plugin.video.gdrive?mode=streamURL&amp;url="+url2.encode('utf-8'), iconimage, info)
def baixarsf(link=""):
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') ).decode("utf-8")
	py = os.path.join( Path, "vid.mp4")
	file = open(py, "w")
	file.write("\n")
	if link == "":
		return
	m3u = OpenURL(link, headers={'referer': "https://www.superflix.net/"})
	m = re.compile("http.+").findall(m3u)
	q = 0
	progress = xbmcgui.DialogProgress()
	progress.create('Downloading...')
	b = 0
	for s in m:
		if (progress.iscanceled()):
			baixarsf()
			return
		q+=1
		try:
		#if q == 15:	break
			per = int(q*100/len(m))
			filedata = urllib2.urlopen(s).read()
			b += len(filedata)
			progress.update(per, convert_size( b ), "", str(per) +'%')
			file = open(py, "ab+")
			file.write(filedata)
		except:
			progress.close()
			NF("erro")
			return
	progress.close()
	return py
# ----------------- Fim Superflix
def testfile(url):
	try:
		req = Request(url)
		req.headers['Range'] = 'bytes=%s-%s' % (100, 350)
		#ST(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100110 Firefox/11.0')
		req.add_header('referer', RCref)
		resp = urlopen(req)
		resp.getcode()
		#ST(resp)
		return False
	except:
		return False
def GetChoice(choiceTitle, fileTitle, urlTitle, choiceFile, choiceUrl, choiceNone=None, fileType=1, fileMask=None, defaultText=""):
	choice = ''
	choiceList = [getLocaleString(choiceFile), getLocaleString(choiceUrl)]
	if choiceNone is not None:
		choiceList = [getLocaleString(choiceNone)] + choiceList
	method = GetSourceLocation(getLocaleString(choiceTitle), choiceList)	
	if choiceNone is None and method == 0 or choiceNone is not None and method == 1:
		if not defaultText.startswith('http'):
			defaultText = ""
		choice = GetKeyboardText(getLocaleString(fileTitle), defaultText).strip().decode("utf-8")
	elif choiceNone is None and method == 1 or choiceNone is not None and method == 2:
		if defaultText.startswith('http'):
			defaultText = ""
		choice = xbmcgui.Dialog().browse(fileType, getLocaleString(urlTitle), 'files', fileMask, False, False, defaultText).decode("utf-8")
	return choice			
def PlayUrl(name, url, iconimage=None, info='', sub='', metah=''):
	#try:
	#	f = OpenURL("http://sstor.000webhostapp.com/imdb/i.txt")
	#	if "year" in f:
	#		metah = eval(f)
	#		f = OpenURL("http://sstor.000webhostapp.com/imdb/deleta.php")
	#except:
	#	pass
	if ";;;" in background:
		b = background.split(";;;")
		if "RC" in b[2]:
			AddFavorites(b[0], iconimage, b[1], "95", "historic.txt")
		elif "NC" in b[2]:
			AddFavorites(b[0], iconimage, b[1], "78", "historic.txt")
		elif "MM" in b[2]:
			AddFavorites(b[0], iconimage, b[1], "181", "historic.txt")
	#url = re.sub('\.mp4$', '.mp4?play', url)
	#url = common.getFinalUrl(url)
	xbmc.log('--- Playing "{0}". {1}'.format(name, url), 2)
	#ST(url)
	listitem = xbmcgui.ListItem(path=url)
	if cSIPTV:
		urllib2.urlopen( "http://cubeplay.000webhostapp.com/siptv/index.php?u="+cSIPTV+"&"+url ).read()
	if metah:
		listitem.setInfo(type="Video", infoLabels=metah)
	else:
		listitem.setInfo(type="Video", infoLabels={"mediatype": "video", "Title": name, "Plot": info })
	if sub!='':
		listitem.setSubtitles(['special://temp/example.srt', sub ])
	if iconimage is not None:
		try:
			listitem.setArt({'thumb' : iconimage})
		except:
			listitem.setThumbnailImage(iconimage)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

def AddDir(name, url, mode, iconimage='', logos='', index=-1, move=0, isFolder=True, IsPlayable=False, background=None, cacheMin='0', info='', metah=''):
	urlParams = {'name': name, 'url': url, 'mode': mode, 'iconimage': iconimage, 'logos': logos, 'cache': cacheMin, 'info': info, 'background': background, 'metah': metah}
	liz = xbmcgui.ListItem(name )
	if metah:
		liz.setInfo(type="Video", infoLabels=metah)
		liz.setArt({"thumb": metah['cover_url'], "poster": metah['cover_url'], "banner": metah['cover_url'], "fanart": metah['backdrop_url'] })
	else:
		liz.setInfo(type="Video", infoLabels={ "Title": name, "Plot": info })
		#liz.setProperty("Fanart_Image", logos)
		liz.setArt({"poster": iconimage, "banner": logos, "fanart": logos })
	#listMode = 21 # Lists
	if IsPlayable:
		liz.setProperty('IsPlayable', 'true')
	items = []
	if mode == 1 or mode == 2:
		items = []
	elif mode== 61 and info=="":
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=31&iconimage={2}&name={3})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name)))])
	elif mode== 78:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=72&iconimage={2}&name={3})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name)))])
	elif (mode== 95 or mode== 96) and "imdb" in cadulto:
		liz.addContextMenuItems(items = [("IMDB", 'XBMC.RunPlugin({0}?url={1}&mode=350&iconimage={2}&name={3})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name))),
		("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=93&iconimage={2}&name={3})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name)))])
	elif mode== 95 or mode== 96:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=93&iconimage={2}&name={3})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name)))])
	elif mode== 135:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=131&iconimage={2}&name={3})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name)))])
	elif mode== 171:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=175&iconimage={2}&name={3})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name)))])
	elif mode== 181:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=185&iconimage={2}&name={3})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name)))])
	elif mode== 191:
		liz.addContextMenuItems(items = [("Add ao fav. do Cube Play", 'XBMC.RunPlugin({0}?url={1}&mode=195&iconimage={2}&name={3})'.format(sys.argv[0], quote_plus(url), quote_plus(iconimage), quote_plus(name)))])
	if info=="Filmes Favoritos":
		items = [("Remover dos favoritos", 'XBMC.RunPlugin({0}?index={1}&mode=333)'.format(sys.argv[0], index)),
		(getLocaleString(30030), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=-1)'.format(sys.argv[0], index, 338)),
		(getLocaleString(30031), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=1)'.format(sys.argv[0], index, 338)),
		(getLocaleString(30032), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=0)'.format(sys.argv[0], index, 338))]
		liz.addContextMenuItems(items)
	if info=="Séries Favoritas":
		items = [("Remover dos favoritos", 'XBMC.RunPlugin({0}?index={1}&mode=334)'.format(sys.argv[0], index)),
		(getLocaleString(30030), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=-1)'.format(sys.argv[0], index, 339)),
		(getLocaleString(30031), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=1)'.format(sys.argv[0], index, 339)),
		(getLocaleString(30032), 'XBMC.RunPlugin({0}?index={1}&mode={2}&move=0)'.format(sys.argv[0], index, 339))]
		liz.addContextMenuItems(items)
	if mode == 10:
		urlParams['index'] = index
	u = '{0}?{1}'.format(sys.argv[0], urllib.parse.urlencode(urlParams))
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isFolder)

def GetKeyboardText(title = "", defaultText = ""):
	keyboard = xbmc.Keyboard(defaultText, title)
	keyboard.doModal()
	text = "" if not keyboard.isConfirmed() else keyboard.getText()
	return text

def GetSourceLocation(title, chList):
	dialog = xbmcgui.Dialog()
	answer = dialog.select(title, chList)
	return answer
def Imdbreturn(n):
	n = urllib.quote(n)
	urlq = OpenURL("http://api.themoviedb.org/3/search/movie?api_key=bd6af17904b638d482df1a924f1eabb4&query="+n+"&language=pt-BR")
	jq = json.loads(urlq)
	return jq

def AddImdb(url): #350
	urlm= re.compile("_.+?html$").findall(url)
	urlm = urlm[0]
	dir = re.sub('CubePlay', 'CubePlayMeta', addon_data_dir )
	file = os.path.join(dir, 'imdb.txt')
	file2 = os.path.join(dir, Cat+'\\imdb'+cPage+'.txt')
	favList = ReadList(file)
	for item in favList:
		if item["url"].lower() == urlm.decode("utf-8").lower():
			if "imdb" in file:
				xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30011), icon))
			return	
	q = re.sub(' ?\((Dub|Leg|Nac).+', '', name )
	q = re.sub('\[\/?COLOR.{0,10}\]', '', q )
	#q = "xmen"
	nomes=[]
	Ano=""
	Vote = 0.0
	jq = Imdbreturn(q)
	for x in jq['results']:
		try:
			rd = re.sub('\d{2}(\d{2})\-.+', r'\1', x['release_date'] )
			nomes.append("["+ str(rd) + "] " +x['title'].encode("utf-8") + " [COLOR blue]("+x['original_title'].encode("utf-8")+")[/COLOR]")
		except:
			nomes.append("[xx]"+x['title'].encode("utf-8") + " [COLOR blue]("+x['original_title'].encode("utf-8")+")[/COLOR]")
	s=-1
	if nomes:
		s = xbmcgui.Dialog().select(name, nomes)
	if s == -1:
		nomes=[]
		d = xbmcgui.Dialog().input("TheMovie id")
		if re.compile("[a-zA-Z]").findall(d):
			jq = Imdbreturn(d)
			if jq['total_results']==0:
				xbmc.executebuiltin("Notification({0}, {1}, 5000, {2})".format(AddonName, "Nada encontrado".encode("utf-8"), icon))
				return
			for x in jq['results']:
				try:
					rd = re.sub('\d{2}(\d{2})\-.+', r'\1', x['release_date'] )
					nomes.append("["+ str(rd) + "] " +x['title'].encode("utf-8") + " [COLOR blue]("+x['original_title'].encode("utf-8")+")[/COLOR]")
				except:
					nomes.append("[xx]"+x['title'].encode("utf-8") + " [COLOR blue]("+x['original_title'].encode("utf-8")+")[/COLOR]")
			if nomes:
				s = xbmcgui.Dialog().select(name, nomes)
			if s == -1:
				return
		else:
			#d = "503314"
			if not d:
				return
			url2 = OpenURL("http://api.themoviedb.org/3/movie/"+d+"?api_key=bd6af17904b638d482df1a924f1eabb4&language=pt-BR")
			j = json.loads(url2)
			url3 = OpenURL("http://api.themoviedb.org/3/movie/"+str(j['id'])+"?api_key=bd6af17904b638d482df1a924f1eabb4&language=en-US")
			j3 = json.loads(url3)
			Nome=j['title']
			Id=d
			Name=j3['title']
			Ano = j['release_date']
			d2 = xbmcgui.Dialog().yesno("Kodi",Nome+" ?")
			if not d2:
				return
			jq = ""
	if jq:
		Nome=jq['results'][s]['title']
		Id=str(jq['results'][s]['id'])
		Name=jq['results'][s]['original_title']
		Ano = jq['results'][s]['release_date']
		Vote = jq['results'][s]['vote_average']
		if jq['results'][s]['original_language'] != 'en':
			url2 = OpenURL("http://api.themoviedb.org/3/movie/"+str(jq['results'][s]['id'])+"?api_key=bd6af17904b638d482df1a924f1eabb4&language=en-US")
			j2 = json.loads(url2)
			Name=j2['title']
	Ano = re.sub('\-.+', '', Ano )
	chList = []
	for channel in chList:
		if channel["name"].lower() == name.decode("utf-8").lower():
			urlm = channel["url"].encode("utf-8")
			break
	data = {"url": urlm.decode("utf-8"), "id": Id, "nome": Nome, "name": Name, "ano": Ano, "vote": Vote}
	#ST(data)
	#return
	favList.append(data)
	SaveList(file, favList)
	SaveList(file2, favList)
	if "imdb" in file:
		xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, Nome.encode("utf-8"), getLocaleString(30012), icon))

def AddFavorites(url, iconimage, name, mode, file):
	file = os.path.join(addon_data_dir, file)
	favList = ReadList(file)
	for item in favList:
		if item["url"].lower() == url.decode("utf-8").lower():
			if "favorites" in file:
				xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30011), icon))
			return
	chList = []	
	for channel in chList:
		if channel["name"].lower() == name.decode("utf-8").lower():
			url = channel["url"].encode("utf-8")
			iconimage = channel["image"].encode("utf-8")
			break
	if not iconimage:
		iconimage = ""
	data = {"url": url, "image": iconimage, "name": name, "mode": mode}
	favList.append(data)
	SaveList(file, favList)
	if "favorites" in file:
		xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, name, getLocaleString(30012), icon))
	
def ListFavorites(file, info):
	file = os.path.join(addon_data_dir, file)
	chList = ReadList(file)
	i = 0
	for channel in chList:
		if cPlayD == "true" and channel["mode"]=="95":
			AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), "96", channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), isFolder=False, IsPlayable=True, info=info)
		else:
			AddDir(channel["name"].encode("utf-8"), channel["url"].encode("utf-8"), channel["mode"], channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), index=i, isFolder=True, IsPlayable=False, info=info)
		i += 1
		
def ListHistoric(file, info):
	file = os.path.join(addon_data_dir, file)
	chList = ReadList(file)
	for channel in reversed(chList):
		channel["image"] = re.sub('redecanais.{1,5}\/', 'redecanais.cloud/', channel["image"] )
		if cPlayD == "true" and channel["mode"]=="95":
			AddDir(channel["name"].encode("utf-8"), channel["url"], "96", channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), isFolder=False, IsPlayable=True, info="")
		else:
			AddDir(channel["name"].encode("utf-8"), channel["url"], channel["mode"], channel["image"].encode("utf-8"), channel["image"].encode("utf-8"), isFolder=True, IsPlayable=False, info="")
		
def RemoveFromLists(index, listFile):
	chList = ReadList(listFile) 
	if index < 0 or index >= len(chList):
		return
	del chList[index]
	SaveList(listFile, chList)
	xbmc.executebuiltin("Container.Refresh()")

def AddNewFavorite(file):
	file = os.path.join(addon_data_dir, file)
	chName = GetKeyboardText(getLocaleString(30014))
	if len(chName) < 1:
		return
	chUrl = GetKeyboardText(getLocaleString(30015))
	if len(chUrl) < 1:
		return
	image = GetChoice(30023, 30023, 30023, 30024, 30025, 30021, fileType=2)
		
	favList = ReadList(file)
	for item in favList:
		if item["url"].lower() == chUrl.decode("utf-8").lower():
			xbmc.executebuiltin("Notification({0}, '{1}' {2}, 5000, {3})".format(AddonName, chName, getLocaleString(30011), icon))
			return			
	data = {"url": chUrl.decode("utf-8"), "image": image, "name": chName.decode("utf-8")}	
	favList.append(data)
	if SaveList(file, favList):
		xbmc.executebuiltin("Container.Refresh()")
	
def MoveInList(index, step, listFile):
	theList = ReadList(listFile)
	if index + step >= len(theList) or index + step < 0:
		return
	if step == 0:
		step = GetIndexFromUser(len(theList), index)
	if step < 0:
		tempList = theList[0:index + step] + [theList[index]] + theList[index + step:index] + theList[index + 1:]
	elif step > 0:
		tempList = theList[0:index] + theList[index +  1:index + 1 + step] + [theList[index]] + theList[index + 1 + step:]
	else:
		return
	SaveList(listFile, tempList)
	xbmc.executebuiltin("Container.Refresh()")

def GetNumFromUser(title, defaultt=''):
	dialog = xbmcgui.Dialog()
	choice = dialog.input(title, defaultt=defaultt, type=xbmcgui.INPUT_NUMERIC)
	return None if choice == '' else int(choice)

def GetIndexFromUser(listLen, index):
	dialog = xbmcgui.Dialog()
	location = GetNumFromUser('{0} (1-{1})'.format(getLocaleString(30033), listLen))
	return 0 if location is None or location > listLen or location <= 0 else location - 1 - index

def Refresh():
	xbmc.executebuiltin("Container.Refresh()")

def TogglePrevious(url, background):
	Addon.setSetting(background, str(int(url) - 1) )
	xbmc.executebuiltin("Container.Refresh()")

def ToggleNext(url, background):
	#xbmcgui.Dialog().ok('Cube Play', url + " " +background)
	Addon.setSetting(background, str(int(url) + 1) )
	xbmc.executebuiltin("Container.Refresh()")

def getmd5(t):
	value_altered = ''.join(chr(ord(letter)-1) for letter in t)
	return value_altered

def CheckUpdate(msg): #200
	try:
		uversao = OpenURL( "https://raw.githubusercontent.com/D4anielCB/CBmatrix/master/version.txt" ).replace('\n','').replace('\r','')
		uversao = re.compile('[a-zA-Z\.\d]+').findall(uversao)[0]
		#xbmcgui.Dialog().ok(Versao, uversao)
		if uversao != Versao:
			Update()
			xbmc.executebuiltin("Container.Refresh()")
		elif msg==True:
			xbmcgui.Dialog().ok('Cube Play', "O addon já esta na última versao: "+Versao+"\nAs atualizações normalmente são automáticas\nUse esse recurso caso nao esteja recebendo automaticamente")
			xbmc.executebuiltin("Container.Refresh()")
	except:
		if msg==True:
			xbmcgui.Dialog().ok('Cube Play', "Não foi possível checar")

def Update():
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') )
	try:
		fonte = OpenURL( "https://raw.githubusercontent.com/D4anielCB/CBmatrix/master/default.py" )
		prog = re.compile('#checkintegritymatrix25852').findall(fonte)
		if prog:
			py = os.path.join( Path, "default.py")
			file = open(py, "w", encoding='utf8')
			file.write(fonte)
			file.close()
		fonte = OpenURL( "https://raw.githubusercontent.com/D4anielCB/CBmatrix/master/resources/settings.xml" )
		prog = re.compile('</settings>').findall(fonte)
		if prog:
			py = os.path.join( Path, "resources/settings.xml")
			file = open(py, "w", encoding='utf8')
			file.write(fonte)
			file.close()
		fonte = OpenURL( "https://raw.githubusercontent.com/D4anielCB/CBmatrix/master/addon.xml" )
		prog = re.compile('</addon>').findall(fonte)
		if prog:
			py = os.path.join( Path, "addon.xml")
			file = open(py, "w", encoding='utf8')
			file.write(fonte)
			file.close()
		xbmc.executebuiltin("Notification({0}, {1}, 9000, {2})".format(AddonName, "Atualizando o addon. Aguarde um momento!", icon))
		xbmc.sleep(2000)
	except:
		xbmcgui.Dialog().ok('Cube Play', "Ocorreu um erro, tente novamente mais tarde")
		
def convert_size(size_bytes):
	if size_bytes == 0:
		return "0B"
	size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
	i = int(math.floor(math.log(size_bytes, 1024)))
	p = math.pow(1024, i)
	s = round(size_bytes / p, 2)
	return "%s %s" % (s, size_name[i])
		
def NF(x, t=5000):
	xbmc.executebuiltin("Notification({0}, {1}, {3}, {2})".format(AddonName, str(x), icon, t))

def ST(x, o="w+"):
	if o == "1":
		o = "ab+"
	x = str(x)
	Path = xbmc.translatePath( xbmcaddon.Addon().getAddonInfo('path') )
	py = os.path.join( Path, "study.txt")
	file = open(py, o)
	#file = open(py, "ab+")
	file.write(x)
	file.close()

params =  urllib.parse.parse_qs( sys.argv[2][1:] ) 
url = params.get('url',[None])[0]
logos = params.get('logos',[None])[0]
name = params.get('name',[None])[0]
iconimage = params.get('iconimage',[None])[0]
cache = int(params.get('cache', '0')[0]) if params.get('cache') else 0
index = int(params.get('index', '-1')[0]) if params.get('index') else -1
move = int(params.get('move', '0')[0]) if params.get('move') else 0
mode = int(params.get('mode', '0')[0]) if params.get('mode') else 0
info = params.get('info',[None])[0]
background = params.get('background',[None])[0]
metah = params.get('metah',[None])[0]

if mode == 0:
	Categories()
	setViewM()
	if not "update" in cadulto:
		CheckUpdate(False)
elif mode == -1: MCanais()
elif mode == -2: MFilmes()
elif mode == -3: MSeries()
elif mode == 3 or mode == 32:
	PlayUrl(name, url, iconimage, info)
elif mode == 301:
	ListFavorites('favoritesf.txt', "Filmes Favoritos")
	setViewS()
elif mode == 302:
	ListFavorites('favoritess.txt', "Séries Favoritas")
	setViewM()
elif mode == 305:
	ListHistoric('historic.txt', "Historico")
	setViewM()
elif mode == 31: 
	AddFavorites(url, iconimage, name, "61", 'favoritess.txt')
elif mode == 72: 
	AddFavorites(url, iconimage, name, "78", 'favoritesf.txt')
elif mode == 93: 
	AddFavorites(url, iconimage, name, "95", 'favoritesf.txt')
elif mode == 131: 
	AddFavorites(url, iconimage, name, "135", 'favoritess.txt')
elif mode == 175: 
	AddFavorites(url, iconimage, name, "171", 'favoritesf.txt')
elif mode == 185: 
	AddFavorites(url, iconimage, name, "181", 'favoritesf.txt')
elif mode == 195: 
	AddFavorites(url, iconimage, name, "191", 'favoritess.txt')
elif mode == 333:
	RemoveFromLists(index, favfilmesFile)
elif mode == 338:
	MoveInList(index, move, favfilmesFile)
elif mode == 334:
	RemoveFromLists(index, favseriesFile)
elif mode == 339:
	MoveInList(index, move, favseriesFile)
elif mode == 38:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Cube Play', 'Deseja mesmo deletar todos os filmes favoritos?')
	if ret:
		common.DelFile(favfilmesFile)
		sys.exit()
elif mode == 39:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Cube Play', 'Deseja mesmo deletar todos os seriados favoritos?')
	if ret:
		common.DelFile(favseriesFile)
		sys.exit()
elif mode == 40:
	dialog = xbmcgui.Dialog()
	ret = dialog.yesno('Cube Play', 'Deseja mesmo deletar todo o historico?')
	if ret:
		common.DelFile(historicFile)
		sys.exit()
elif mode == 50:
	Refresh()
elif mode == 60:
	Series()
	setViewS()
elif mode == 61:
	ListSNC(background)
	setViewS()
elif mode == 62:
	PlayS()
	setViewS()
elif mode == 71:
	MoviesNC()
	setViewM()
elif mode == 78:
	ListMoviesNC()
	setViewS()
elif mode == 79:
	PlayMNC()
	setViewS()
elif mode == 80:
	Generos()
elif mode == 81:
	CategoryOrdem2(url)
elif mode == 90:
	MoviesRCD()
	setViewM()
elif mode == 91:
	MoviesRCL()
	setViewM()
elif mode == 92:
	MoviesRCN()
	setViewM()
elif mode == 95:
	PlayMRC()
	setViewM()
elif mode == 96:
	PlayMRC2()
elif mode == 100:
	TVRC()
	setViewM()
elif mode == 101:
	PlayTVRC()
elif mode == 102:
	TVCB(url)
	setViewS()
elif mode == 103:
	PlayTVCB()
elif mode == 105:
	Addon.setSetting("cEPG", "1")
	xbmc.executebuiltin("Container.Refresh()")
elif mode == 109:
	PVR()
elif mode == 110:
	ToggleNext(url, background)
elif mode == 120:
	TogglePrevious(url, background)
elif mode == 130:
	SeriesRC("series","cPageser")
	setViewS()
elif mode == 230:
	SeriesRC("novelas","cPagenov", 231)
	setViewS()
elif mode == 231:
	ListaNovRC()
	setViewS()
elif mode == 135:
	TemporadasRC(background)
	setViewS()
elif mode == 133:
	PlaySRC()
	setViewS()
elif mode == 139:
	AllEpisodiosRC()
	setViewS()
elif mode == 140:
	SeriesRC("animes","cPageani")
	setViewS()
elif mode == 150:
	SeriesRC("desenhos","cPagedes")
	setViewS()
elif mode == 160:
	Busca()
	setViewM()
elif mode == 170:
	MoviesFO("Rapidvideo","cPagefo1")
	setViewM()
elif mode == 171:
	GetMFO1()
	setViewM()
elif mode == 172:
	PlayMFO1()
elif mode == 85:
	GenerosFO()
elif mode == 180:
	ListFilmeMM("cPageMMf")
	setViewM()
elif mode == 181:
	OpenLinkMM()
	setViewM()
elif mode == 182:
	PlayLinkMM()
elif mode == 184:
	ListFilmeLancMM()
	setViewM()
elif mode == 189:
	GenerosMM()
elif mode == 190:
	ListSerieMM()
	setViewS()
elif mode == 191:
	ListSMM(background)
	setViewS()
elif mode == 192:
	ListEpiMM(background)
	setViewS()
elif mode == 194:
	PlaySMM()
elif mode == 200:
	CheckUpdate(True)
elif mode == 210:
	ListGO("cPageGOf")
	setViewM()
elif mode == 211:
	PlayGO()
elif mode == 219:
	GenerosGO()
elif mode == 220:
	Filmes96()
elif mode == 221:
	MoviesRCR() ###
	setViewM()
elif mode == 229:
	PlayFilmes96()
elif mode == 350:
	AddImdb(url)
elif mode == 401:
	ListSerieSF()
	setViewS()
elif mode == 402:
	ListTempSF()
	setViewS()
elif mode == 403:
	ListEpiSF()
	setViewS()
elif mode == 411:
	ListMovieSF()
	setViewM()
elif mode == 405:
	PlaySSF()
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
#checkintegritymatrix25852
