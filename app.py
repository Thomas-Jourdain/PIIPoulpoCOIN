import hashlib
from inspect import signature
from flask import Flask, jsonify, make_response, redirect, render_template, request, session, url_for
from flask_mongoengine import MongoEngine
from mongoengine import *
from mongoengine import (DateTimeField, Document, IntField, ListField,
                         ObjectIdField, QuerySet, ReferenceField, StringField,
                         UUIDField)



app = Flask(__name__)
app.config["SECRET_KEY"] = 'thisismyscretkey'
app.config["MONGODB_SETTINGS"] = {'DB': 'myDb'}
db = MongoEngine(app)

# Classes

class User(db.Document):
    pseudo = StringField(unique=True,required=True)
    mdp = StringField(required=True)
    solde = IntField(required=True)


def createUser(pseudo, mdp):  # Creer un utilisateur et l'ajoute à la bd
    newUser = User(pseudo=pseudo,mdp=mdp,solde=0)
    reponse=True
    try:
        newUser.save()
    except:
        reponse=False
    return reponse


class Transaction(db.Document):
    receveur = StringField(required=True)
    payeur = StringField(required=True)
    montant = IntField(0, None, required=True)

    def __str__(self):
        return f"{self.payeur} give {self.montant} to {self.receveur}"

def createTransaction(payeur,montant,receveur)->None:
    newTransaction=Transaction(payeur=payeur,montant=montant,receveur=receveur)
    newTransaction.save()
def getTransactions():
    result=""
    transactions=Transaction.objects()
    for transaction in transactions:
        result +=transaction.__str__() + ", "
    return result

class Block(db.Document):
    data = StringField()
    hash = StringField()
    index = IntField(unique=True)

    def __str__(self):
        str =f"Block {self.index}, " 
        str +=f"data={self.data}, "
        str +=f"hash={self.hash} \n"
        return str



def valideBlock(block):
    if block.hash[:3] == "666":  # Ici le problème consiste à avoir un hash commencant par 666
            return True
    return False

def valideChain():
    blockchain=Block.objects()
    for block in blockchain:
        if not valideBlock(block):
            if block.index>1:
                return False
    return True
    
def createNewBlock(previous_block_hash, previous_block_index, transaction_list, signature) -> None:
    index = previous_block_index+1
    data = f"{' - '.join(transaction_list)} - {previous_block_hash} - {signature}"
    hash = hashlib.sha256(data.encode()).hexdigest()
    newBlock = Block(data=data, hash=hash, index=index)
    return newBlock


def last_block():
        candidat=Block.objects.get(index=1)
        blocks=Block.objects()
        for block in blocks:
            if(block.index>candidat.index):
                candidat=block
        return candidat



def display_chain():
    blocks=Block.objects()
    str=""
    for block in blocks:
        str+=block.__str__()
        print(str)
        return str



## Init db
# J'ai pas trouver de moyen de seeder proprement

# Genesis block
try:
    genesisBlock=createNewBlock("0",0,['Genesis Block'],0)
    genesisBlock.save()
except:
    print("bd déja init")

# Admin
try:
    My = User(pseudo="Admin", mdp="secret", solde=0)
    My.save()
except:
    print("bd déjà init")

## Views

# Site
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/blockchain")
def blockchain():
    blocks=Block.objects()
    return render_template("blockchain.html",blocks=blocks)

@app.route("/login", methods={'POST', 'GET'})
def login():
    if request.method == "POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')
        utilisateur = User.objects.get(pseudo=nom, mdp=mdp)
        if utilisateur is not None:
            session['nom_utilisateur'] = utilisateur.pseudo
            return redirect(url_for("index"))
        else:
            return redirect(request.url)
    else:
        if "nom_utilisateur" in session:
            return redirect(url_for("index"))
        return render_template("login.html")

@app.route("/inscription",methods={'POST', 'GET'})
def inscription():
    if request.method=="POST":
        donnees = request.form
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')
        mdp2=donnees.get('mdp2')
        if mdp!=mdp2: 
            return render_template("erreurMdpDiff.html")
        if createUser(nom,mdp)==False:
            return render_template("erreurDejaExistant.html")
        session['nom_utilisateur'] = nom
        return redirect(url_for("index"))
    return render_template("inscription.html")

@app.route('/profil')
def profil():
    if 'nom_utilisateur' in session:
        utilisateur = User.objects.get(pseudo=session['nom_utilisateur'])
        return render_template("profil.html",utilisateur=utilisateur)
    redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('nom_utilisateur', None)
    return redirect(url_for('login'))

@app.route('/transaction',methods={'POST', 'GET'})
def transaction():
    if 'nom_utilisateur' in session:
        utilisateur = User.objects.get(pseudo=session['nom_utilisateur'])
        if request.method == "POST":
            donnees = request.form
            nom = donnees.get('receveur')
            montant = donnees.get('montant')
            try:
                receveur = User.objects.get(pseudo=nom)
            except:
                return render_template("transaction.html",utilisateur=utilisateur)
            nouveau_solde=int(utilisateur.solde)-int(montant)
            if nouveau_solde<0:
                return render_template("erreurSoldeInsuf.html",utilisateur=utilisateur)
            utilisateur.solde = nouveau_solde
            receveur.solde +=int(montant)
            utilisateur.save()
            receveur.save()
            createTransaction(utilisateur.pseudo,montant,receveur.pseudo)
            return redirect(request.url)   
        return render_template("transaction.html",utilisateur=utilisateur)
    return render_template(url_for("index"))
# API


@app.route('/api/login',methods=["POST","GET"])
def login_user():
    if "nom_utilisateur" not in session:
        donnees = request.get_json()
        nom = donnees.get('nom')
        mdp = donnees.get('mdp')
        utilisateur = User.objects.get(pseudo=nom, mdp=mdp)
        if utilisateur is not None:
            session['nom_utilisateur'] = utilisateur.pseudo
            return make_response("sucess",200)
        else:
            return make_response("could not verify",401)
    return make_response("already loged",200)

@app.route('/api/last_block')
def get_last_block():
    return jsonify(last_block())
@app.route('/api/transactions')
def get_transaction():
    transactions=Transaction.objects()
    return jsonify(transactions)
    
@app.route('/api/getBlock/<int:index>')
def getBlock(index):
    block=Block.objects.get(index=index)
    return jsonify(block)

@app.route('/api/valideBlock',methods=["POST"])
def addBlock():
    if "nom_utilisateur" in session:
        current_user=User.objects.get(pseudo=session["nom_utilisateur"])
        donnees = request.get_json()
        signature=donnees.get("signature")
        previous_block=last_block()
        block=createNewBlock(previous_block.hash,previous_block.index,getTransactions(),signature)
        if valideBlock(block):
            block.save()
            if not valideChain():
                block.delete()
                return make_response("BlockChain Compromise",400)
            Transaction.drop_collection()
            nouveauSolde=int(current_user.solde)+1
            current_user.solde=nouveauSolde
            current_user.save()
            createTransaction("Admin",1,current_user.pseudo)
            return make_response("Block Valide",200)
        return make_response("Block Invalide")
    return make_response("Please log in",400)

@app.route('/api/mine')
def mine():
    if "nom_utilisateur" in session:
        current_user=User.objects.get(pseudo=session["nom_utilisateur"])
        previous_block=last_block()
        signature=0
        block=createNewBlock(previous_block.hash,previous_block.index,getTransactions(),signature)
        while not valideBlock(block):
            signature+=1
            block=createNewBlock(previous_block.hash,previous_block.index,getTransactions(),signature)
        block.save()
        if not valideChain():
                block.delete()
                return make_response("BlockChain Compromise",400)
        Transaction.drop_collection()
        nouveauSolde=int(current_user.solde)+1
        current_user.solde=nouveauSolde
        current_user.save()
        createTransaction("Admin",1,current_user.pseudo)
        return jsonify(block)
    return make_response("Please log in",400)
    

            

        

@app.route('/api/blockchain')
def getBlockchain():
    blockchain=Block.objects()
    return jsonify(blockchain)
if __name__ == '__main__':
    app.run(debug=True)
