# Converttentotwenty
## Resume
Bibliotheque permettant la traduction d'un message d'une base 10 a base 20.

Voici le dictionnaire de la base 20 utilise : "0123456789abcdefghij". Par exemple :

- 11 (base10) -> b (base20);
- 20 (base10) -> j (base20);
- 15 (base10) -> f (base20)
## Installation
La bibloteque peut s'installer via pip grace au site PyPI

```
pip install converttentotwenty
```

## Utilisation
La bibloteque comporte une fonction "traduction()" permettant d'effectuer le changement d'une base a l'autre. Pour importer le paquet :
```
from converttentotwenty import traduction
```
Voici le docstring de la fonction :
```
Convertit les elements d'une liste d'une base a l'autre.

La conversion de chaque element se fait d'un entier 
de base 10 vers un entier de base 20, selon le dictionnaire de la
base 20 fournie en documentation

Parameters
----------
message : list
    contient des entiers en base 10.

Returns
-------
res : list
    contient les entiers traduit en base 20 sous forme
    de chaine de caractere.

Examples
--------
>>> traduction([4, 0, 16])
['4', '0', 'g']
>>> traduction([5, 1, 4])
['5', '1', '4']
>>> traduction([11, 16])
['b', 'g']
```
La fonction necessite un argument qui doit etre une liste d'entier en base 10 compris entre 0 et 19 inclus. La liste n'a pas de longueur minimale ou maximale.

La fonction renvoie une liste de chaine de caractere. Chaque valeur de cette liste ne peut etre qu'un seul caractere

## Exemples d'utilisation
Voici un exemple d'utilisation de ma biblioteque
```
from converttentotwenty import traduction
ten = [1, 5, 12, 17]
twenty = traduction(ten)
print(twenty)
['1', '5', 'c', 'h']    
```
## information annexe
Le but de cette bibliotheque est de l'utiliser a des fins pedagogiques pour des TP de NSI.
La base choisie est arbitraire et n'a pas pour but de representer la realite autour d'une base 20 reellement utilise.

