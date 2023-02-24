#!/usr/bin/env python
# coding: utf-8

# # Journal of Pediatric Neurology

# In[17]:


import pandas as pd
from bs4 import BeautifulSoup as bts
import requests
import re


# In[18]:


url = input("Please insert an URL: ")


# In[19]:


def GetAndResultsURL(url):
    result =requests.get(url,headers={"User-Agent":"Mozilla/5.0"})
    soup=bts(result.text,'html.parser')
    return soup


# In[20]:


def getText(htmlObject):
    res = []
    for tag in htmlObject:
        res.append(tag.text)
    return res


# In[21]:


#url="https://www.thieme-connect.com/products/ejournals/issue/10.1055/s-012-55551"


# In[22]:


#MAKALENİN SAYFA ADRESLERİ
html=GetAndResultsURL(url)
for links in html.findAll("div",{"class":"listItem scientific"}):
    print("https://www.thieme-connect.com/"+links.a["href"]) 


# In[23]:


def remove_html_tags(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


# In[24]:


VOLUME=(html.find('span', {'class': 'issueNumber'}).text).replace("Issue","Number").replace("0","").strip("·")
YEAR=(html.find('span', {'class': 'issueYear'}).text).replace("·",",")
CY=(html.find('div', {'id': 'currentYear'}).text).replace("\n","").strip(" ")
a=(YEAR + VOLUME+", Year "+CY )


# In[25]:


Yazar=[]
Makale=[]
Abstract=[]
PDF=[]
KB=[]
Baslik=[]
SUPP=[]
bControl=""
for links in html.findAll("div",{"class":"articleDetails"}):
    baslık = links.find('span', {'class': 'authors'}).findPrevious('h2', {"class":"Category"})
    Yazar.append(links.find('span', {'class': 'authors'}).text.replace("\n", ""))
    Makale.append(links.a.text.strip())
    Abstract.append(("https://www.thieme-connect.com/"+links.find('li', {'class': 'option'}).findNext()["href"]))
    PDF.append(("https://www.thieme-connect.com/"+links.find('li', {'class': 'option'}).findNext().findNext().a["href"]))
    KB.append(("PDF "+links.find('li', {'class': 'option'}).findNext().findNext().a.text.split()[-2].strip("(")))
    #Sup=links.find('a', {'class': 'gotoLink block'}).findNext().findNext().a["href"]
    
    try:
        Sup = links.find('a', {'class': 'gotoLink block'})
        Sup = Sup['href']
        Sup = "https://www.thieme-connect.com/"+str(Sup)
        SUPP.append(Sup)
    except:
         SUPP.append(' ')
    
    
    baslık = remove_html_tags(str(baslık))
    
    if bControl != baslık:
        bControl = baslık
    else:
        baslık = ' '
    Baslik.append(baslık)


# In[26]:


Yazar_list = [element.replace("                                                                 ", "")  for element in Yazar]


# In[27]:


df=pd.DataFrame(list(zip(a,Baslik,Yazar_list,Makale,Abstract,PDF,KB,SUPP)),columns=["a","BASLIK","YAZAR","MAKALE","ABSTRACT","PDF","KB","SUPP"])


# In[28]:


jpn1="""
<!DOCTYPE html>
<html lang="en">
<head>
<title>Journal of Pediatric Neurology</title>
<meta charset="utf-8">
<link rel="stylesheet" href="css/reset.css" type="text/css" media="all">
<link rel="stylesheet" href="css/layout.css" type="text/css" media="all">
<link rel="stylesheet" href="css/stylejpb.css" type="text/css" media="all">
<script type="text/javascript" src="js/jquery-1.6.js"></script>
<script type="text/javascript" src="js/cufon-yui.js"></script>
<script type="text/javascript" src="js/cufon-replace.js"></script>
<script type="text/javascript" src="js/Vegur_700.font.js"></script>
<script type="text/javascript" src="js/Vegur_400.font.js"></script>
<script type="text/javascript" src="js/Vegur_300.font.js"></script>
<script type="text/javascript" src="js/jquery.easing.1.3.js"></script>
<script type="text/javascript" src="js/tms-0.3.js"></script>
<script type="text/javascript" src="js/tms_presets.js"></script>
<script type="text/javascript" src="js/backgroundPosition.js"></script>
<script type="text/javascript" src="js/atooltip.jquery.js"></script>
<script type="text/javascript" src="js/script.js"></script>
<!--[if lt IE 9]>
<script type="text/javascript" src="js/html5.js"></script>
<style type="text/css">.box1 figure{behavior:url("js/PIE.htc");}</style>
<![endif]-->
</head>
<body id="page1">
<div class="body1">
  <div class="main">
    <!-- header -->
    <header>
      <div class="wrapper">
        <h1><a href="http://worldpediatricsociety/jpn/index.html" id="logo">World of Pediatric Society </a></h1>
        <nav>
          <ul id="menu">
            <li><a href="http://worldpediatricsociety.org/jpn/index.html">Home</a></li>
            <li><a href="about.html">About </a></li>
            <li><a href="associations.html">Associations</a></li>
            <li><a href="editors.html">Editors</a></li>
            <li><a href="editorial.html">Editorial Board</a></li>
            <li><a href="http://www.thieme.com/media/ita/JPN_Author_instructions.pdf"target="_blank">Instructions</a></li>
            <li id="menu_active"><a href="archives.html">Archives</a></li>
            <li><a href="subscription.html">Subscription</a></li>
            <li><a href="http://www.thieme.com/index.php?page=shop.product_details&flypage=flypage.tpl&product_id=1700&category_id=6&keyword=Journal+of+Pediatric+Neurology&option=com_virtuemart&Itemid=53">THIEME PUBLISHERS</a></li>
            <li><a href="contacts.html">Contact</a></li>
          </ul>
        </nav>
      </div>
     </header>
    <!-- / header -->
    <!-- content -->
    <article id="content">
      <div class="wrapper">
        <div class="box1">
         <h2>JOURNAL OF PEDIATRIC NEUROLOGY</h2>
         <h2><span>Official Journal of the World Pediatric Society, Turkiye</span></h2> 
         <br>
         
		 <h2><font color=#12d6ce>30th Annual Meeting of European Academy of Childhood Disability (EACD) will take place in Tbilisi, Georgia, May 28-31, 2018, <a href="https://www.eacd2018.net">https://www.eacd2018.net</a></h2></font><br>
		 
         <h2><a href="https://www.thieme-connect.com/products/ejournals/journal/10.1055/s-00029030">LAST ISSUE</a></h2>
"""


# In[29]:


jpn2="""

 

 <br>
         </div>
      </div>
      <div class="wrapper">
        <h3></h3>
      </div>
    </article>
    <!-- / content -->
    <!-- footer -->
	<footer>
      <div class="wrapper"> <a href="http://worldpediatricsociety.org/jpn/index.html" id="footer_logo"><span>J Pediatr Neurol</span></a>
      <div class="tel"><span>jpn</span>@erbakan.edu.tr</div>
      </div>
      <div class="wrapper"> ISSN: 1304-2580 print, ISSN: 1875-9041 (Electronic).
      <ul id="icons">
          <li><a href="https://facebook.com/worldpediatricsociety" class="normaltip"><img src="../images/icon1.gif" alt=""></a></li>
          <li><a href="https://twitter.com/worldpediatricsociety" class="normaltip"><img src="../images/icon2.gif" alt=""></a></li>
        </ul>
      </div>
      <div id="footer_text">Copyright &copy; <a href="#">World Pediatric Society </a> All Rights Reserved<br>
    </footer>
    <!-- / footer -->
  </div>
</div>
<script type="text/javascript">Cufon.now();</script>
<script type="text/javascript
"""


# In[30]:


with open("jpn.html", "w", encoding="utf-8") as file:
    print(jpn1, file=file, flush=True)
    print('<center><strong>'+a + '</strong><br><br></center>',file=file, flush=True)
    for ind in df.index:
        print("<strong>"+df['BASLIK'][ind]+"</strong><br>", file=file, flush=True)
        print("<em>"+df['YAZAR'][ind]+'</em><br>', file=file, flush=True)
        print(df['MAKALE'][ind]+"<br>", file=file, flush=True)
        print('<ul id="menu2">', file=file, flush=True)
        print('<li id="menu2_active">', file=file, flush=True)
        print('<a href="'+df['ABSTRACT'][ind]+'">Abstract</a></li>', file=file, flush=True)
        print('<li id="menu2_active">', file=file, flush=True)
        print('<a href="'+ df['PDF'][ind]+'">' + df['KB'][ind]+ ' KB</a></li>', file=file, flush=True)

        if df['SUPP'][ind] != ' ':
            print('<li id="menu2_active">', file=file, flush=True)
            print('<a href=' + str(df['SUPP'][ind]) + '>' + 'SUPPLEMENTARY MATERIAL</a></li>', file=file, flush=True)

        print('</ul><br>', file=file, flush=True)
        print('<br>', file=file, flush=True)
    print(jpn2, file=file, flush=True)


# In[184]:


#with open("test.html", "w", encoding="utf-8") as file:
#    print(jpic2, file=file, flush=True)


# In[ ]:





# In[ ]:




