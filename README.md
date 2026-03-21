# Hashage simple en HolyC

Petit programme en **HolyC** qui lit une ligne de texte, calcule un **hash maison 256 bits inspiré de SHA-256**, puis affiche le résultat en **hexadécimal**.

## Ce que fait le programme

- demande un texte à l'utilisateur ;
- lit jusqu'à **255 caractères** ;
- accepte les **espaces** dans la saisie ;
- applique un hash **plus complexe et moins prédictible** que l'ancien FNV-1a ;
- affiche le texte lu puis le digest hexadécimal sur **64 caractères**.

## Ce qui a changé

Le projet n'utilise plus un hash très simple de type multiplicatif, ni le FNV-1a 64 bits de la version précédente.

À la place, il utilise maintenant un **hash maison 256 bits inspiré de SHA-256** avec :

- un état interne de **8 mots de 32 bits** ;
- un traitement par **blocs de 64 octets** ;
- un **padding** avec bit `1`, zéros, puis longueur du message ;
- des opérations de **rotation**, **XOR**, **choix** (`Ch`) et **majorité** (`Maj`) ;
- un mini **message schedule** recalculé sur 64 tours.

> Ce hash est **inspiré** de SHA-256 dans sa structure générale, mais il **n'est pas compatible SHA-256** et ne doit pas être considéré comme cryptographiquement sûr.

## Structure de l'algorithme

Le cœur du mélange utilise des fonctions proches, dans l'esprit, de SHA-256 :

```c
Ch(x, y, z)
Maj(x, y, z)
BigSigma0(x)
BigSigma1(x)
SmallSigma0(x)
SmallSigma1(x)
```

Chaque bloc de 64 octets est absorbé dans un état initialisé avec 8 constantes de 32 bits, puis mélangé sur **64 rounds**.

## Fichier principal

- `hashage.HC`

## Prérequis

Le programme a ete pense pour **Linux** avec **holyc-lang** (`hcc`) et evite maintenant les casts explicites du style `(U32)x`, qui peuvent poser probleme selon certaines versions du parseur Ubuntu.

Tu dois avoir :

- `hcc` installé ;
- un système Linux compatible.

## Compiler le programme

Dans le dossier du projet :

```bash
hcc hashage.HC
```

Cette commande génère en général un exécutable nommé `a.out`.

## Exécuter le programme

```bash
./a.out
```

## Exemple d'utilisation

Entrée :

```text
bonjour tout le monde
```

Sortie :

```text
Texte a hash : bonjour tout le monde
Texte lu : bonjour tout le monde
Algorithme : Hash maison 256 bits inspire de SHA-256
Longueur max supportee : 255 caracteres
Hash (hex) : 64-caracteres-hexadecimaux
```

## Limites actuelles

Le programme utilise :

```c
scanf(" %255[^\n]", texte);
```

Donc :

- la lecture est limitée à **255 caractères** ;
- la saisie peut contenir des espaces ;
- le programme lit une seule ligne ;
- ce hash est **plus complexe**, mais reste un **hash maison non standard** ;
- il est **plus proche dans l'esprit de SHA-256**, sans être un SHA-256 officiel.

## Fonctionnement du hash

La fonction principale de hashage est :

```c
U0 HashStr(U8 *s, U32 digest[8])
```

Elle :

1. mesure la longueur de la chaîne ;
2. construit un message paddé aligné sur 64 octets ;
3. initialise un état de 8 mots ;
4. traite chaque bloc via `ProcessBlock` ;
5. produit un digest final de **256 bits**.

Pour rester compatible avec un environnement HolyC sur Ubuntu, le code utilise des variables temporaires pour charger les octets sur 32 bits au lieu de s'appuyer sur des casts explicites dans les expressions.

L'affichage concatène ensuite les 8 mots de 32 bits en hexadécimal.

## Pistes d'amélioration

- comparer ce hash maison avec un vrai **SHA-256** ;
- ajouter des tests avec plusieurs entrées et digests attendus ;
- sortir l'algorithme dans un fichier séparé ;
- ajouter un mode comparaison entre plusieurs algorithmes.
