
# PoulpoCOIN

A brief description of what this project does and who it's for


## Installation
Création de l'environnement virtuel
 
```bash
  python3 -m venv .venv
  >> .venv\scripts\activate
```

Installer MyApp avec pip

```bash
 pip install -r requirement.txt
```
    
## Deploiment

Deploiment avec flask

```bash
  flask run 
```

## API Reference

#### Se connecter

```http
  POST /api/login
```

| Parametre | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `nom` | `string` | **Required**. Nom de l'utilisateur |
| `mdp` | `string` | **Required**. Mot de passe de l'utilisateur |

Permet à l'utilisateur de se connecter .

#### Obtenir la liste des transactions

```http
  GET /api/transactions
```

Renvoie toute les transactions a enresgistrer 


#### Obtenir un bloc

```http
  GET /api/getBlock/<int:index>
```

| Parametre | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `index` | `int` | **Required**. Numéro du bloc |

Renvoie le bloc n°index

#### Proposer un bloc

```http
  POST /api/valideBlock
```

| Parametre | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `signature` | `int` | **Required**. Signature du block |

Permet à un utilisateur connecter de proposé un block .
L'utilisateur ne donne que la signature du bloc, car les autres
informations sont directement envoyer par le site.
Cela est du au fait que la blockchain ne supporte qu'une branche
et que par conséquand il n'y a qu'un seul bloc auxquel se ratacher.

#### Miner un bloc

```http
  GET /api/mine
```

Permet à un utilisateur connecter de miner un bloc .
Dans les fait, le minage est effectuer par le serveur.

#### Obtenir tous les blocs

```http
  GET /api/blockchain
```

Renvoie tous les bloc de la blockchain.


