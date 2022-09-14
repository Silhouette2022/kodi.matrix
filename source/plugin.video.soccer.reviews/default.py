#!/usr/bin/python
# -*- coding: utf-8 -*-
# Writer (c) 2022, Silhouette, E-mail: 
# Rev. 0.2.0

import xbmcplugin, xbmcgui, xbmcaddon
import urllib.request, urllib.parse, urllib.error
import os, re, sys, json
from bs4 import BeautifulSoup
import YDStreamExtractor

__addon__ = xbmcaddon.Addon(id='plugin.video.soccer.reviews')
plugin_path = __addon__.getAddonInfo('path')
plugin_icon = __addon__.getAddonInfo('icon')
plugin_fanart = __addon__.getAddonInfo('fanart')

lite_icon = xbmc.translatePath(os.path.join(plugin_path, 'icon2.png'))
art2_icon = xbmc.translatePath(os.path.join(plugin_path, 'fanart2.png'))
icon4_icon = xbmc.translatePath(os.path.join(plugin_path, 'icon4.png'))
art3_icon = xbmc.translatePath(os.path.join(plugin_path, 'fanart3.png'))
icon5_icon = xbmc.translatePath(os.path.join(plugin_path, 'icon5.png'))
icon6_icon = xbmc.translatePath(os.path.join(plugin_path, 'icon6.png'))
icon7_icon = xbmc.translatePath(os.path.join(plugin_path, 'icon7.png'))
art7_icon = xbmc.translatePath(os.path.join(plugin_path, 'fanart7.png'))
dbg = 0

pluginhandle = int(sys.argv[1])

mail_pg = "http://my.mail.ru/mail/jevons/video/"

s24_pg = "http://www.sport-24tv.ru"

gtv_start = "https://gooool365.org"
gtv_gen_pg = gtv_start + "/page/"
gtv_hl_pg = gtv_start + "/obzors/page/"

omm_start = "https://ourmatch.me"


def dbg_log(line):
    if dbg: xbmc.log(line)


def get_url(url, data=None, cookie=None, save_cookie=False, referrer=None):
    dbg_log('-get_url:')
    dbg_log('- url:' + url)
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Opera/9.80 (X11; Linux i686; U; ru) Presto/2.7.62 Version/11.00')
    req.add_header('Accept', 'text/html, application/xml, application/xhtml+xml, */*')
    req.add_header('Accept-Language', 'ru,en;q=0.9')
    if cookie: req.add_header('Cookie', cookie)
    if referrer: req.add_header('Referer', referrer)
    if data:
        response = urllib.request.urlopen(req, data, timeout=30)
    else:
        response = urllib.request.urlopen(req, timeout=30)
    link = response.read()
    if save_cookie:
        setcookie = response.info().get('Set-Cookie', None)
        if setcookie:
            setcookie = re.search('([^=]+=[^=;]+)', setcookie).group(1)
            link = link + '<cookie>' + setcookie + '</cookie>'

    response.close()
    return link



def reportUsage(addonid, action):
    host = 'xbmc-doplnky.googlecode.com'
    tc = 'UA-3971432-4'
    try:
        utmain.main({'id': addonid, 'host': host, 'tc': tc, 'action': action})
    except:
        pass


def resolve(self, url):
    result = xbmcprovider.XBMCMultiResolverContentProvider.resolve(self, url)
    if result:
        # ping befun.cz GA account
        host = 'befun.cz'
        tc = 'UA-35173050-1'
        try:
            utmain.main({'id': __scriptid__, 'host': host, 'tc': tc, 'action': url})
        except:
            print ('Error sending ping to GA')
            traceback.print_exc()
    return result

def add_dir(title, uri, icon=None, art=None, isFolder=True, plot=None):
    item = xbmcgui.ListItem(title)
    if plot == None: plot = title
    if not isFolder: item.setProperty('IsPlayable', 'true')
    item.setInfo(type='video', infoLabels={'title': title, 'plot': plot})
    if icon != None: item.setArt({ 'thumb': icon, 'icon' : icon })
    if art != None: item.setProperty('fanart_image', art)
    xbmcplugin.addDirectoryItem(pluginhandle, uri, item, isFolder)
    dbg_log('- uri:' + uri)
    
def SR_top():
    dbg_log('-SR_top:' + '\n')
    
    srtops =    [
         ("Gooool365.ORG", "gtvtop", icon6_icon, art2_icon),
         ("OURMATCH.me", "ommtop", icon7_icon, art7_icon),
                ]
               
    for ctTitle, ctMode, ctIcon, ctArt  in srtops:
    
        item = xbmcgui.ListItem(ctTitle)
        item.setArt({ 'thumb': ctIcon, 'icon' : ctIcon })
        item.setProperty('fanart_image', ctArt)
        xbmcplugin.addDirectoryItem(pluginhandle,
                                    sys.argv[0] + '?mode=' + ctMode, item, True)     
        item = xbmcgui.ListItem(ctTitle)
        
    xbmcplugin.endOfDirectory(pluginhandle)

#    item = xbmcgui.ListItem('SPORT-24TV.ru')
#    item.setArt({ 'thumb': lite_icon, 'icon' : lite_icon })
#    item.setProperty('fanart_image', art2_icon)
#    xbmcplugin.addDirectoryItem(pluginhandle, sys.argv[0] + '?mode=s24top' + '&url=' +
#                                urllib.parse.quote_plus(s24_pg), item, True)
# https://www.sport-24tv.ru

    xbmcplugin.endOfDirectory(pluginhandle)

def GTV_top():
    dbg_log('-GTV_top:' + '\n')
    
    gtvtops =   [
         ("Трансляции", "gtvlist", urllib.parse.quote_plus(gtv_gen_pg), icon6_icon, art2_icon),
         ("Обзоры", "gtvlist", urllib.parse.quote_plus(gtv_hl_pg), icon6_icon, art2_icon),
         ("Разделы", "gtvctlg", urllib.parse.quote_plus(gtv_gen_pg), icon6_icon, art2_icon),
                    ]
               
    for ctTitle, ctMode, ctLink, ctIcon, ctArt  in gtvtops:
        add_dir(ctTitle, sys.argv[0] + '?mode=' + ctMode + '&url=' + ctLink, ctIcon, ctArt, True)

    xbmcplugin.endOfDirectory(pluginhandle)
    

def GTV_ctlg(url):
    dbg_log('-GTV_ctlg:' + '\n')
    dbg_log('- url:'+  url + '\n')

    catalog =  [
    
     ("/news/rus_premier_league/", "Россия"),
     ("/news/ukrainapremer_liga/", "Украина"),
     ("/news/angliya_premier_league/", "Англия"),
     ("/news/ispaniyala_liga_primera/", "Испания"),
     ("/news/italiyalega_calcio/", "Италия"),
     ("/news/germaniyabundesliga/", "Германия"),
     ("/news/francia/", "Франция"),
     ("/news/drugie_nacionalnye_chempionaty_i_kubki/", "Другие Чемпионаты"),
     ("/news/tovarischeskie_matchi/", "Товарищеские матчи"),
     ("/news/futbolnoe_video/", "Передачи"),

     ("/news/evrokubki_2014_2019gg/", "Еврокубки"),
     ("/news/chempionat_evropy/", "Чемпионат Европы"),
     ("/news/chempionat_mira/", "Чемпионат Мира"),
     ("/copa2015/", "Кубок Америки"),
     ("/news/cup-africa/", "Кубок Африканских Наций"),

     ("/news/nhl_nhl/", "НХЛ"),
     ("/news/kontinentalnaya_xokkeynaya_liga_kxl/", "КХЛ"),
     ("/news/mezhdunarodnye_turniry_po_hokkeyu/", "Международные турниры"),

     ("/news/formula_1/", "Формула 1"),
     ("/news/basketbol/", "Баскетбол"),
     ("/news/tennis/", "Теннис"),
     ("/news/edinoborstva/", "Единоборства"),
     ("/news/zimnie_vidy_sporta/", "Биатлон"),
     ("/news/olimpiyskie_igry_2012/", "Олимпийские игры"),
     
]
               
    for ctLink, ctTitle  in catalog:
        add_dir(ctTitle, sys.argv[0] + '?mode=gtvlist&url=' +
            urllib.parse.quote_plus(gtv_start + ctLink + "page/"), 
            icon6_icon, art2_icon, True)
        
    xbmcplugin.endOfDirectory(pluginhandle)

def GTV_list(url, page):
    dbg_log('-GTV_list:')
    dbg_log('- url:' + url)
    dbg_log('- page:' + page)

    http = get_url(url + page + '/')

    i = 0
    nuclears = BeautifulSoup(http, 'html.parser').find_all('div', {'class': 'item nuclear'})
    
    for nuclear in nuclears:
        entries = re.compile('<a href="(.*?)".*?img alt="(.*?)".*?data-src="(.*?)"').findall(str(nuclear))
        for href, title, img in entries:
            dbg_log('-HREF %s' % href)
            dbg_log('-TITLE %s' % title)
            dbg_log('-IMG %s' % img)
            if img[0] == '/':
                img = gtv_start + img
                dbg_log('-IMG %s' % img)

            uri = sys.argv[0] + '?mode=gtvshow' + '&url=' + urllib.parse.quote_plus(href) + '&name=' + urllib.parse.quote_plus(title)
            add_dir(title, uri, img, art2_icon, True)
            i = i + 1

    if i:
        uri = sys.argv[0] + '?mode=gtvlist&page=' + str(int(page) + 1) + '&url=' + url
        add_dir('<NEXT PAGE>', uri, None, plugin_fanart, True)

        uri = sys.argv[0] + '?mode=gtvlist&page=' + str(int(page) + 5) + '&url=' + url
        add_dir('<NEXT PAGE +5>', uri, None, plugin_fanart, isFolder=True)

    xbmcplugin.endOfDirectory(pluginhandle)
    
def GTV_show(url, name):
    dbg_log('-GTV_show:')
    dbg_log('- url:' + url)
    dbg_log('- name:' + name)

    http = get_url(url)

    scripts = re.compile('ajax\({(.*?)}').findall(str(http))
    dbg_log(str(scripts))
    if len(scripts) > 0:
        script = str(scripts[0]).replace('\\n', ' ').replace('\\t', ' ').replace("\\'", "'")
        dbg_log(str(script))
        newsid = re.compile("newsid: '(.*?)'").findall(str(script))
        if len(newsid) > 0:
            dbg_log(str(newsid))
            pdata = { 'dp' : 'block',
                      'newsid' : str(newsid[0]) }
            dbg_log(str(pdata))
            hpost = get_url(gtv_start + '/player/dp.php', data=urllib.parse.urlencode(pdata).encode(), referrer=url)
            dbg_log(str(hpost))
            links = re.compile('src="(.*?)".*?script:window\.open\((.*?),.*?>(.*?)<').findall(str(hpost))
#            .*?jаvascript:window.open\((.*?),.*?>(.*?)<').findall(str(hpost))
            dbg_log(str(links))
            i = 1
            for img, href, title in links:
                if img[0] == '/':
                    img = gtv_start + img
                href = href.replace("\\'", "'")
                if href[0] == '/':
                    href = gtv_start + href
                    
                title = '[%d] %s'%(i,name)
                uri = sys.argv[0] + '?mode=gtvplay' + '&url=' + urllib.parse.quote_plus(href) + '&name=' + urllib.parse.quote_plus(name)
                add_dir(title, uri, img, art2_icon, True)
                i = i + 1

    xbmcplugin.endOfDirectory(pluginhandle)

def GTV_play(url, title, resolve = False):
    url = url.replace('&amp;', '&')

    dbg_log('-GTV_play:' + '\n')
    dbg_log('- url:' + url + '\n')
    dbg_log('- title:' + title + '\n')
    uri = None
    
    url = url.strip('"').strip("'").strip("'")
    if not url.startswith('http') and not url.startswith('plugin'): url = 'http:' + url
    dbg_log('- url:' + url + '\n')
    
    if url.find('videohatkora') > -1:
        uri = get_hatkora(url)
    else:
        uri = get_YTD(url)

    if uri != None and uri != False:
        if not uri.startswith('http') and not uri.startswith('plugin'): uri = 'http:' + uri
        uri = urllib.parse.unquote_plus(uri)
        dbg_log('- uri: ' + uri + '\n')
        try:
            name = title[(title.find('~') + 1):]
        except:
            name = title
        item = xbmcgui.ListItem(path=uri)
        if resolve:
            xbmcplugin.setResolvedUrl(pluginhandle, True, item)
        else:
            sPlayer = xbmc.Player()
            item.setInfo(type='Video', infoLabels={'title': name})
            item.setProperty('IsPlayable', 'true')
            sPlayer.play(uri, item)    
    
def get_hatkora(url):
    dbg_log('-get_hatkora:' + '\n')
    if not url.startswith('http'): url = 'http:' + url
    dbg_log('- url-in:' + url + '\n')
    result = get_url(url)
#    dbg_log(str(result))
#    sources = re.compile(b"src:{hls:\'(.*?)\'},backupSrc:{hls:\'(.*?)\'}}").findall(result)
    sources = re.compile(b"src:{hls:\'(.*?)\'}").findall(result)
    dbg_log(str(sources))
    if len(sources) > 0 :
        return sources[0].decode()
    else:
        return None

def OMM_top():
    dbg_log('-OMM_top:' + '\n')
    
    ommtops =   [
         ("LATEST", "ommlist", urllib.parse.quote_plus(omm_start), icon7_icon, art7_icon),
         ("POPULAR", "ommctlg", urllib.parse.quote_plus(omm_start), icon7_icon, art7_icon),
         ("ALL COMPETITIONS", "ommctlg&res=1", urllib.parse.quote_plus(omm_start), icon7_icon, art7_icon),
                    ]
               
    for ctTitle, ctMode, ctLink, ctIcon, ctArt  in ommtops:
        add_dir(ctTitle, sys.argv[0] + '?mode=' + ctMode + '&url=' + ctLink, ctIcon, ctArt, True)
        
    xbmcplugin.endOfDirectory(pluginhandle)
    


            
def OMM_show(url, name):
    dbg_log('-OMM_show:')
    dbg_log('- url:' + url)
    dbg_log('- name:' + name)
    c  = get_url(url)
    r = re.findall("{embed:.*?<iframe.*?src=\"(.*?)\".*?lang:\\\\'(.*?)\\\\'.*?\\\\'type\\\\':\\\\'(.*?)\\\\'.*?quality:\\\\'(.*?)\\\\'.*?source:\\\\'(.*?)\\\\'", str(c))
#    {embed:\'<iframe width="630" height="390" src="//ok.ru/videoembed/3855664941638?autoplay=1" 
#lang:\'English\', \'type\':\'Extended Higlhights\', quality:\'HD\', source:\'ok.ru\'
    dbg_log(str(r))
    i = 1
    for src, lang, type, quality, source in r:
        try:
            title = '[%d] %s %s %s %s' % (i, type, quality, lang, source)
            uri = sys.argv[0] + '?mode=gtvplay&res=1' + '&url=' + urllib.parse.quote_plus(src) + '&name=' + urllib.parse.quote_plus(title)
            add_dir(title, uri, icon7_icon, art2_icon, isFolder=False)
            i +=1
        except: pass
        
    xbmcplugin.endOfDirectory(pluginhandle)
    
def OMM_list(url, page):
    dbg_log('-OMM_list:')
    dbg_log('- url:' + url)
    dbg_log('- page:' + page)
    

    if page == '' or page == '1': http = get_url(url)
    else:
        query = {
        "0": "{\"error\":\"\",\"m\":\"\",\"p\":0,\"post_parent\":\"\",\"subpost\":\"\",\"subpost_id\":\"\",\"attachment\":\"\",\"attachment_id\":0,\"name\":\"\",\"pagename\":\"\",\"page_id\":0,\"second\":\"\",\"minute\":\"\",\"hour\":\"\",\"day\":0,\"monthnum\":0,\"year\":0,\"w\":0,\"category_name\":\"\",\"tag\":\"\",\"cat\":\"\",\"tag_id\":\"\",\"author\":\"\",\"author_name\":\"\",\"feed\":\"\",\"tb\":\"\",\"paged\":0,\"meta_key\":\"\",\"meta_value\":\"\",\"preview\":\"\",\"s\":\"\",\"sentence\":\"\",\"title\":\"\",\"fields\":\"\",\"menu_order\":\"\",\"embed\":\"\",\"category__in\":[],\"category__not_in\":[],\"category__and\":[],\"post__in\":[],\"post__not_in\":[],\"post_name__in\":[],\"tag__in\":[],\"tag__not_in\":[],\"tag__and\":[],\"tag_slug__in\":[],\"tag_slug__and\":[],\"post_parent__in\":[],\"post_parent__not_in\":[],\"author__in\":[],\"author__not_in\":[],\"ignore_sticky_posts\":false,\"suppress_filters\":false,\"cache_results\":true,\"update_post_term_cache\":true,\"lazy_load_term_meta\":true,\"update_post_meta_cache\":true,\"post_type\":\"\",\"posts_per_page\":36,\"nopaging\":false,\"comments_per_page\":\"50\",\"no_found_rows\":false,\"order\":\"DESC\"}",
        "serie-a" : "{\"category_name\":\"serie-a\",\"error\":\"\",\"m\":\"\",\"p\":0,\"post_parent\":\"\",\"subpost\":\"\",\"subpost_id\":\"\",\"attachment\":\"\",\"attachment_id\":0,\"name\":\"\",\"pagename\":\"\",\"page_id\":0,\"second\":\"\",\"minute\":\"\",\"hour\":\"\",\"day\":0,\"monthnum\":0,\"year\":0,\"w\":0,\"tag\":\"\",\"cat\":177,\"tag_id\":\"\",\"author\":\"\",\"author_name\":\"\",\"feed\":\"\",\"tb\":\"\",\"paged\":0,\"meta_key\":\"\",\"meta_value\":\"\",\"preview\":\"\",\"s\":\"\",\"sentence\":\"\",\"title\":\"\",\"fields\":\"\",\"menu_order\":\"\",\"embed\":\"\",\"category__in\":[],\"category__not_in\":[],\"category__and\":[],\"post__in\":[],\"post__not_in\":[],\"post_name__in\":[],\"tag__in\":[],\"tag__not_in\":[],\"tag__and\":[],\"tag_slug__in\":[],\"tag_slug__and\":[],\"post_parent__in\":[],\"post_parent__not_in\":[],\"author__in\":[],\"author__not_in\":[],\"tax_query\":[{\"taxonomy\":\"seasons\",\"field\":\"id\",\"terms\":[472,473,474]}],\"ignore_sticky_posts\":false,\"suppress_filters\":false,\"cache_results\":true,\"update_post_term_cache\":true,\"lazy_load_term_meta\":true,\"update_post_meta_cache\":true,\"post_type\":\"\",\"posts_per_page\":36,\"nopaging\":false,\"comments_per_page\":\"50\",\"no_found_rows\":false,\"taxonomy\":\"seasons\",\"term_id\":472,\"order\":\"DESC\"}",
        }

        if url != omm_start:
            category = url.rsplit('/', 1)[-1]
        else: category = '0'
        dbg_log(str(category))
        if category not in query: return
        pdata = {
            "action": "loadmore",
            "query": query[category],
#            "{" + category + "\"error\":\"\",\"m\":\"\",\"p\":0,\"post_parent\":\"\",\"subpost\":\"\",\"subpost_id\":\"\",\"attachment\":\"\",\"attachment_id\":0,\"name\":\"\",\"pagename\":\"\",\"page_id\":0,\"second\":\"\",\"minute\":\"\",\"hour\":\"\",\"day\":0,\"monthnum\":0,\"year\":0,\"w\":0,\"category_name\":\"\",\"tag\":\"\",\"cat\":\"\",\"tag_id\":\"\",\"author\":\"\",\"author_name\":\"\",\"feed\":\"\",\"tb\":\"\",\"paged\":0,\"meta_key\":\"\",\"meta_value\":\"\",\"preview\":\"\",\"s\":\"\",\"sentence\":\"\",\"title\":\"\",\"fields\":\"\",\"menu_order\":\"\",\"embed\":\"\",\"category__in\":[],\"category__not_in\":[],\"category__and\":[],\"post__in\":[],\"post__not_in\":[],\"post_name__in\":[],\"tag__in\":[],\"tag__not_in\":[],\"tag__and\":[],\"tag_slug__in\":[],\"tag_slug__and\":[],\"post_parent__in\":[],\"post_parent__not_in\":[],\"author__in\":[],\"author__not_in\":[],\"ignore_sticky_posts\":false,\"suppress_filters\":false,\"cache_results\":true,\"update_post_term_cache\":true,\"lazy_load_term_meta\":true,\"update_post_meta_cache\":true,\"post_type\":\"\",\"posts_per_page\":36,\"nopaging\":false,\"comments_per_page\":\"50\",\"no_found_rows\":false,\"order\":\"DESC\"}",
            "page": page
                }
        dbg_log(str(pdata))
        http = get_url(omm_start + '/wp-admin/admin-ajax.php', data=urllib.parse.urlencode(pdata).encode(), referrer=url + "/")
        dbg_log(str(http))

    i = 0
    matches = BeautifulSoup(http, 'html.parser').find_all('div', {'class': 'col-12 col-md-6 col-lg-4 match-info'})

    for match in matches:
        match = str(match)
        try:
            link = BeautifulSoup(match, 'html.parser').find_all('a', {'class': 'match-info__link'})[0]
            title = re.sub('\t+', ' ', re.sub(' +', ' ', link.get_text().strip("\t\n\r ").replace("\n", " ").replace("\r", " ")))
            link = link.get("href")
        except: link = None

        if link != None:
            uri = sys.argv[0] + '?mode=ommshow' + '&url=' + urllib.parse.quote_plus(link) + '&name=' + urllib.parse.quote_plus(title)
            add_dir(title, uri, icon7_icon, art2_icon, True)
            i = i + 1

    if i and url == omm_start:
        uri = sys.argv[0] + '?mode=ommlist&page=' + str(int(page) + 1) + '&url=' + url
        add_dir('<MORE>', uri, None, art2_icon, True)

    xbmcplugin.endOfDirectory(pluginhandle)

def OMM_ctlg(url, res):
    dbg_log('-OMM_ctlg:' + '\n')
    dbg_log('- url:'+  url + '\n')

    cat0 =  [
        ("/competitions/england/premier-league", "Premier League"),
        ("/competitions/spain/la-liga", "La Liga"),
        ("/competitions/italy/serie-a", "Serie A"),
        ("/competitions/germany/bundesliga", "Bundesliga"),
        ("/competitions/france/ligue-1", "Ligue 1"),
        ("/competitions/europe/champions-league", "Champions League"),
        ("/competitions/europe/europa-league", "Europa League"),
        ]
        
    cat1 =  [
        ("/competitions/england/premier-league", "England Premier League"),
        ("/competitions/england/championship", "England Championship"),
        ("/competitions/england/fa-cup", "England FA Cup"),
        ("/competitions/england/league-cup", "England League Cup"),
        ("/competitions/england/community-shield", "England Community Shield"),
        ("/competitions/spain/la-liga", "Spain La Liga"),
        ("/competitions/spain/copa-del-rey", "Spain Copa del Rey"),
        ("/competitions/spain/supercopa-de-espana", "Spain Super Cup"),
        ("/competitions/italy/serie-a", "Italy Serie A"),
        ("/competitions/italy/coppa-italia", "Italy Coppa Italia"),
        ("/competitions/italy/supercoppa-italiana", "Italy Super Cup"),
        ("/competitions/germany/bundesliga", "Germany Bundesliga"),
        ("/competitions/germany/2-bundesliga", "Germany 2. Bundesliga"),
        ("/competitions/germany/dfb-pokal", "Germany DFB Pokal"),
        ("/competitions/germany/german-supercup", "Germany Super Cup"),
        ("/competitions/france/ligue-1", "France Ligue 1"),
        ("/competitions/france/coupe-de-la-ligue", "France Coupe de la Ligue"),
        ("/competitions/france/coupe-de-france", "France Coupe de France"),
        ("/competitions/france/trophee-des-champions", "France Super Cup"),
        ("/competitions/europe/euro", "EURO"),
        ("/competitions/europe/champions-league", "Champions League"),
        ("/competitions/europe/europa-league", "Europa League"),
        ("/competitions/europe/uefa-super-cup", "UEFA Super Cup"),
        ("/competitions/europe/nations-league", "Nations League"),
        ("/competitions/international/copa-america", "Copa America"),
        ("/competitions/international/club-friendlies", "Club Friendlies"),
        ("/competitions/international/international-friendlies-highlights", "International Friendlies"), 
        ("/competitions/international/club-world-cup", "Club World Cup"),
        ("/competitions/international/africa-cup-of-nations", "Africa Cup of Nations"),
        ("/competitions/international/copa-libertadores", "Copa Libertadores"),
    ]
    
    if res: catalog = cat1
    else: catalog = cat0                                        
               
    for ctLink, ctTitle  in catalog:
        add_dir(ctTitle, sys.argv[0] + '?mode=ommlist&url=' +
            urllib.parse.quote_plus(omm_start + ctLink), 
            icon6_icon, art2_icon, True)
        
    xbmcplugin.endOfDirectory(pluginhandle)
    

def JVS_s24tv(url):
    dbg_log('-JVS_s24tv:' + '\n')
    dbg_log('- url:' + url + '\n')

    http = get_url(urllib.parse.unquote_plus(url))
    
    iframe = re.compile('<iframe.*?src="(.*?)"').findall(http.replace('\r', ' ').replace('\n', ' '))
#     print iframe

    r0 = ["Источник " + str(key) for key in range(1, len(iframe))]
    dbg_log('- r0:'+  str(r0) + '\n')
    i = xbmcgui.Dialog().select('', r0)
    
    http = get_url(iframe[i])
    try:
        uri = re.compile("videoLink = '(.*?)'").findall(http)[0]
    
        dbg_log('- uri: ' + uri + '\n')
        item = xbmcgui.ListItem(path = uri)
        xbmcplugin.setResolvedUrl(pluginhandle, True, item)
    except: pass
    
def JVS_s24play(url):
    dbg_log('-JVS_s24tv:' + '\n')
    dbg_log('- url:' + url + '\n')

    http = get_url(urllib.parse.unquote_plus(url))
    
    iframe = re.compile('<iframe.*?src="(.*?)"').findall(http.replace('\r', ' ').replace('\n', ' '))[0]
#     print iframe
    http = get_url(iframe)
    uri = re.compile("videoLink = '(.*?)'").findall(http)[0]
    
    dbg_log('- uri: ' + uri + '\n')
    item = xbmcgui.ListItem(path = uri)
    xbmcplugin.setResolvedUrl(pluginhandle, True, item)


def get_rutube(url, videoId=None):
    dbg_log('-get_rutube:' + '\n')
    dbg_log('- url-in:' + url + '\n')
    c = 0
    if not videoId:
        if 'rutube.ru' in url:
            try:
                videoId = re.findall('rutube.ru/play/embed/(.*?)"', url)[0]
            except:
                try:
                    videoId = re.findall('rutube.ru/video/(.*?)/', url)[0]
                except:
                    pass

    if videoId:
        url = 'http://rutube.ru/api/play/options/' + videoId + '?format=json'
        dbg_log('- url-req:' + url + '\n')
        request = urllib.request.Request(url)
        request.add_header('User-agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
        try:
            response = urllib.request.urlopen(request)
            resp = response.read()
        except:
            pass

        jsonDict = json.loads(resp)
        link = urllib.parse.quote_plus(jsonDict['video_balancer']['m3u8'])

        return link
    else:
        return None


def get_rutube1(url):
    dbg_log('-get_rutube:' + '\n')
    dbg_log('- url-in:' + url + '\n')
    if not videoID:
        if 'rutube.ru/play/embed/' in url:
            try:
                videoId = re.findall('rutube.ru/play/embed/(.*?)"', url)[0]
            except:
                pass
    if videoID:
        url = 'http://rutube.ru/api/play/options/' + videoId + '?format=json'
        request = urllib.request.Request(url)
        request.add_header('User-agent',
                           'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36')
        response = urllib.request.urlopen(request)
        resp = response.read()
        jsonDict = json.loads(resp)
        link = urllib.parse.quote_plus(jsonDict['video_balancer']['m3u8'])
        return link
    else:
        return None


def get_rutube2(url):
    dbg_log('-get_rutube:' + '\n')
    if not url.startswith('http'): url = 'http:' + url
    dbg_log('- url-in:' + url + '\n')
    result = get_url(url)
    jdata = urllib.parse.unquote_plus(result).replace('&quot;', '"').replace('&amp;', '&')
    try:
        #         url = re.compile('"m3u8": "(.*?)"').findall(jdata)[0]
        url = re.compile('href="(.*?)"').findall(jdata)[0].replace('rutube.ru/', 'rutube.ru/api/')
        result = get_url(url)
        #         print result
        #         url = re.compile('rel="video_src" href="(.*?)"').findall(result)[0]
        #         result = get_url(url)

        #         <meta property="og:video" content="https://video.rutube.ru/8810316" />
        #         <meta property="og:video:secure_url" content="https://video.rutube.ru/8810316" />
        try:
            url = re.compile('"og:video" content="(.*?)"').findall(result)[0]
        except:
            try:
                url = re.compile('"og:video:secure_url" content="(.*?)"').findall(result)[0]
            except:
                url = ''

        dbg_log('- url-out:' + url + '\n')
    except:
        url = None
    return url


def get_VK(url, n = 0):
    dbg_log('-get_VK:' + '\n')
    dbg_log('- url:' + url + '\n')

    newVK = VKIE()
    nurl = newVK._real_extract(url)

    if nurl != None and 'rutube' in nurl:
        nurl = get_rutube(nurl.replace('?','"'))

    return nurl


def get_YTD(url):

    vid = YDStreamExtractor.getVideoInfo(url, resolve_redirects=True)

    dbg_log('- YTD: \n')
    if vid:
        dbg_log('- YTD: Try\n')
        stream_url = vid.streamURL()
        #         stream_url = vid.streamURL().split('|')[0]
        dbg_log('- surl:' + stream_url + '\n')
        return stream_url
    else:
        dbg_log('- YTD: None\n')
        return None


def touch(url):
    req = urllib.request.Request(url)
    try:
        res = urllib.request.urlopen(req)
        res.close()
        return True
    except:
        return False


def get_mailru(url):
    #    try:
    url = url.replace('/my.mail.ru/video/', '/api.video.mail.ru/videos/embed/')
    url = url.replace('/my.mail.ru/mail/', '/api.video.mail.ru/videos/embed/mail/')
    url = url.replace('/videoapi.my.mail.ru/', '/api.video.mail.ru/')
    result = get_url(url)
    #        print result
    url = re.compile('"metadataUrl" *: *"(.+?)"').findall(result)[0]
    #        print url
    if not url.startswith('http'): url = 'http:' + url
    mycookie = get_url(url, save_cookie=True)
    cookie = re.search('<cookie>(.+?)</cookie>', mycookie).group(1)
    h = "|Cookie=%s" % urllib.quote(cookie)

    result = get_url(url)
    #        print result
    result = json.loads(result)
    result = result['videos']
    #        print result
    url = []
    url += [{'quality': '1080p', 'url': i['url'] + h} for i in result if i['key'] == '1080p']
    url += [{'quality': 'HD', 'url': i['url'] + h} for i in result if i['key'] == '720p']
    url += [{'quality': 'SD', 'url': i['url'] + h} for i in result if not (i['key'] == '1080p' or i['key'] == '720p')]

    if url == []: return None
    return url
    #    except:
    return None

 
class Streamable():
    def __init__(self):
        name = "Streamable"
        domains = ['streamable.com']
        pattern = '(?://|\.)(streamable\.com)/(?:s/)?([a-zA-Z0-9]+(?:/[a-zA-Z0-9]+)?)'
 
    def get_media_url(self, web_url):
        html = get_url(web_url)
        match = re.search('videoObject\s*=\s*(.*?});', html)
        if match:
            try: js_data = json.loads(match.group(1))
            except: js_data = {}
            streams = js_data.get('files', {})
            sources = [(stream.get('height', 'Unknown'), stream['url']) for _key, stream in streams.iteritems()]
            sources = [(label, 'https:' + stream_url) if stream_url.startswith('//') else (label, stream_url) for label, stream_url in sources]
            sources.sort(key=lambda x: x[0], reverse=True)
            return sources[0][1].replace('&amp;','&')
        else:
            dbg_log('JSON Not Found')
            return None


def JVS_play(url, title):
    url = url.replace('&amp;', '&')

    dbg_log('-JVS_play:' + '\n')
    dbg_log('- url:' + url + '\n')
    dbg_log('- title:' + title + '\n')
    uri = None

    if url.find('videoapi.my.mail.ru') > -1:
        quals = get_mailru(url)
        for d in quals:
            try:
                if d['quality'] == 'HD':
                    uri = d['url']
                    break
                if d['quality'] == '1080p':
                    uri = d['url']
                    break
                if d['quality'] == 'SD':
                    uri = d['url']
                    break
            except:
                pass

    elif url.find('vkontakte.ru') > -1:
        uri = get_VK(url)
    elif url.find('vk.com') > -1:
        #         uri = get_YTD(url)
        uri = get_VK(url)
    elif url.find('rutube') > -1:
        uri = get_rutube(url)

    if uri != None and uri != False:
        if not uri.startswith('http') and not uri.startswith('plugin'): uri = 'http:' + uri
        uri = urllib.parse.unquote_plus(uri)
        dbg_log('- uri: ' + uri + '\n')
        try:
            name = title[(title.find('~') + 1):]
        except:
            name = title
        item = xbmcgui.ListItem(path=uri)
        if 0:
            xbmcplugin.setResolvedUrl(pluginhandle, True, item)
        else:
            sPlayer = xbmc.Player()
            item.setInfo(type='Video', infoLabels={'title': name})
            item.setProperty('IsPlayable', 'true')
            sPlayer.play(uri, item)


def JVS_playpbtv(url, title):
    url = urllib.parse.unquote_plus(url.replace('&amp;', '&'))
    if pbtv_start not in url:
        url = pbtv_start + url
    dbg_log('-JVS_playpbtv:' + '\n')
    dbg_log('- url:' + url + '\n')

    http = get_url(url)
    uri = pbtv_start + re.compile('file: "(.*?)"').findall(http)[0]

    dbg_log('- uri: ' + uri + '\n')
    name = title
    item = xbmcgui.ListItem(label=name, path=uri)
    #    xbmcplugin.setResolvedUrl(pluginhandle, True, item)

    sPlayList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    sPlayer = xbmc.Player()
    sPlayList.clear()
    item.setProperty('mimetype', 'video/x-msvideo')
    item.setProperty('IsPlayable', 'true')
    item.setInfo(type='video', infoLabels={'title': name})
    sPlayList.add(uri, item, 0)
    sPlayer.play(sPlayList)


def uni2enc(ustr):
    raw = ''
    uni = unicode(ustr, 'utf8')
    uni_sz = len(uni)
    for i in xrange(len(ustr)):
        raw += ('%%%02X') % ord(ustr[i])
    return raw


def get_params():
    param = []
    # print sys.argv[2]
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


params = get_params()
mode = params['mode'] if 'mode' in params else ''
page = params['page'] if 'page' in params else '1'
name = urllib.parse.unquote_plus(params['name']) if 'name' in params else ''
url = urllib.parse.unquote_plus(params['url']) if 'url' in params else ''
if 'res' in params and params['res'] != '0' : res = True
else: res = False

if mode == '':
    SR_top()
elif mode == 'gtvtop':
    GTV_top()
elif mode == 'gtvlist':
    GTV_list(url, page)
elif mode == 'gtvshow':
    GTV_show(url, name)
elif mode == 'gtvplay':
    GTV_play(url, name, res)
elif mode == 'gtvctlg':
    GTV_ctlg(url)
elif mode == 'ommtop':
    OMM_top()
elif mode == 'ommlist':
    OMM_list(url, page)
elif mode == 'ommshow':
    OMM_show(url, name)
elif mode == 'ommctlg':
    OMM_ctlg(url, res)
elif mode == 's24top':
    JVS_s24top(s24_pg)
elif mode == 's24tv':
    JVS_s24tv(url)

