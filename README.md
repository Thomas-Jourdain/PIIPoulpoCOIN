
# PoulpoCOIN

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

Renvoie toute les transactions à enregistrer 


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

Permet à un utilisateur connecté de proposer un bloc . L'utilisateur ne donne que la signature du bloc, car les autres informations sont directement envoyées par le site. Cela est dû au fait que la blockchain ne supporte qu'une branche et que par conséquent il n'y a qu'un seul bloc auquel se rattacher

#### Miner un bloc

```http
  GET /api/mine
```

Permet à un utilisateur connecté de miner un bloc . Dans les faits, le minage est effectué par le serveur.

#### Obtenir tous les blocs

```http
  GET /api/blockchain
```

Renvoie tous les blocs de la blockchain.


