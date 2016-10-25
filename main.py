#!/usr/bin/python3
#-*- coding: utf-8 -*-
from werkzeug.contrib.jsrouting import render_template
from flask.templating import render_template_string
import time

fichier="articles.txt"

def litArticle(fichier,nbrArticle):
    """
    lit les x articles du fichier et retourne un tableau des articles
    """
    #print("lit les {} articles du fichier {}".format(nbrArticle,fichier))
    
    tabProvisoire=[]
    tabArticle=[]
    with open(fichier,"r") as f:
        lignes=f.readlines()
    for i in lignes:
        if "[d]" in i: #on est au debut d'un article
            art=True
        if "[f]" in i: #on est a la fin d'un article 
            art=False
        if art: 
            if "[d]" not in i: tabProvisoire.append(i.strip())
        else: 
            tabArticle.append(tabProvisoire)
            tabProvisoire=[]
    if nbrArticle==0: nbrArticle=len(tabArticle)-1
    return tabArticle[0:nbrArticle]
            
    
    
def ecritArticles(fichier,article):
    """
    ecrit l'article dans le fichier, en debut de fichier
    article est un tableau consititue du titre et du contenu
    article=["titre","contenu"]
    """
    print("on ecrit l'article {} dans le fichier {}".format(article,fichier))
    with open(fichier,"r") as f:
        lignes=f.readlines()
    tabProvisoire=["[d]\n",article[0].strip()+"\n",article[1].strip()+"\n","[f]\n"]+lignes
    print(tabProvisoire)
    with open(fichier,"w") as f:
        for i in tabProvisoire:
            f.write(i)
    return True
    
from flask import Flask, render_template, request
import config
app = Flask(__name__)
app.secret_key='kjlkjlkjlkjlkjlkjlkjlkjoijoijoioijoi'

@app.route("/",methods=["GET","POST"])
def hello():
    if 'time' in session:
        if session['time']!=0 and session['time']+config.timeConfig>time.time():
            session['time']=0
            session.pop('name')
            session.pop('pass')
    nbrA=config.nbrArticle
    if request.method=="POST":
        if "toutvoir" in request.form:
            nbrA=0
    return render_template('index.html',table=litArticle(fichier, nbrA),titre=config.titre)


@app.route("/create",methods=["GET","POST"])
def creer():
    if request.method=="POST":
        print("POST")        
        if 'name' in request.form: #session:            
            session['name'] = request.form['name']
            session['pass'] = request.form['password']
            if session['name']!=config.user:
                return hello()
        else: 
            if session['name']==config.user and session['pass']==config.password:
                session['time']=time.time()
                if "titre" in request.form:
                    tab=[]
                    tab.append(request.form['titre'])
                    tab.append(request.form['contenu'])
                    print(tab)
                    ecritArticles(fichier, tab)
                    return hello() #)return render_template('index.html')        
    if 'name' in session:
        if session['name']==config.user and session['pass']==config.password:
            return  render_template('formCreate.html')
        else: session.pop('name')
    return render_template('form.html')




if __name__ == "__main__":
    timeUser=0  
    session={}
    nameUser=''
    app.run(debug=True)