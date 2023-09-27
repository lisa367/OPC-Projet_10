# Projet 10: SoftDesk - DjangoREST API
***

## <b>Etape 1</b>
Initialisez un répertoire git avec à la commande `git init`


Puis clonez le répertoire distant : \
`git clone https://github.com/lisa367/OPC-Projet_10.git`

---

## <b>Etape 2</b>
Déplacez-vous dans le dossier OPC-Projet_10/ : `cd OPC-Projet_10/`
Créez un environnement virtuel dans le répertoire en utilisant la commande suivante dans le terminal : 
`python3 -m venv .env` 
<br>
<br>
Votre répertoire local devrait désormais avoir la structure suivante : 
<pre>OPC-Projet_10/
        | .env/
        | src/
                | Accounts/
                | Issues/          
                | Projects/
                | SoftDesk/
                | .gitignore
                | README.md
                | requirements.txt
</pre>
<br>
<br>
Démarrer l'environnement virtuel : 
`source .env/bin/activate` 

---

## <b>Etape 3</b>

Assurez-vous que l'interpréteur Python sélectionné par votre éditeur de code est bien celui de l'environnement virtuel, puis installez les dépendences du projet grâce à la commande : \
`pip install -r requirements.txt`

---

## <b>Etape 4</b>
Déplacez-vous dans le dossier src : `cd src`
Créez, puis appliquez les migrations pour la base de données : \
`python manage.py makemigrations`
<br>
`python manage.py migrate`

---

## <b>Etape 5</b>
Enfin, lancez le serveur local : `python manage.py runserver`