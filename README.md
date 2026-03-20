# Hashage simple en HolyC

Petit programme en **HolyC** qui lit une ligne de texte, calcule un hash simple, puis affiche le résultat en **hexadécimal**.

## Ce que fait le programme

- demande un texte à l'utilisateur ;
- lit jusqu'à **255 caractères** ;
- accepte maintenant les **espaces** dans la saisie ;
- calcule un hash avec la formule suivante :

```c
hash = hash * 31 + *s;
```

- affiche le texte lu puis le hash en hexadécimal sur **16 caractères**.

## Fichier principal

- `hashage.HC`

## Prérequis

Le programme a été pensé pour **Linux** avec **holyc-lang** (`hcc`).

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
Longueur max supportee : 255 caracteres
Hash (hex) : ...
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
- ce hash est **simple et non cryptographique**.

## Fonctionnement du hash

La fonction principale de hashage est :

```c
U64 HashStr(U8 *s)
```

Elle :

1. prend une chaîne de caractères en entrée ;
2. parcourt la chaîne caractère par caractère ;
3. mélange les valeurs dans une variable `U64` ;
4. renvoie le hash final.

Le hash retourné est stocké sur **64 bits**.

## Pistes d'amélioration

- comparer ce hash simple avec une implémentation de **SHA-256** ;
- ajouter des tests avec plusieurs entrées ;
- gérer les entrées vides et les chaînes plus longues ;
- séparer encore davantage l'I/O et la logique de hashage.
