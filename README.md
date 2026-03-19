# Hashage simple en HolyC

Programme en **HolyC** qui lit un texte, calcule un hash simple, puis l'affiche en **hexadécimal**.

## Ce que fait le programme

- demande un texte à l'utilisateur
- lit jusqu'à **255 caractères max**
- calcule un hash avec la formule :


hash = hash * 31 + *s;


- affiche le résultat en hexadécimal

## Fichier principal

- hashage.HC

## Prérequis

Le programme a été pensé pour **Linux, distro ubuntu** avec **holyc-lang** (hcc).

Tu dois avoir :

- hcc installé
- un système Linux compatible

## Compiler le programme

Dans le dossier du projet :


hashage.hc

readme


Cette commande compile le programme et génère en général un exécutable nommé :

hcc hashage.HC

## Exécuter le programme

Après compilation, pour le lancer :


./a.out


## Utilisation


Quand on lance le programme actuel on entre du texte normal et on en ressort avec un texte en hexa

## Limitation actuelle

Le programme utilise :


scanf("%255s", texte);


Donc :

- la lecture est limitée à **255 caractères**
- la saisie s'arrête au **premier espace**

Exemple :

- hello → fonctionne
- hello world → seule la partie `hello` sera lue

## Fonctionnement du hash

La fonction principale de hashage est :


U64 HashStr(U8 *s)


Elle :

1. prend une chaîne de caractères en entrée
2. parcourt la chaîne caractère par caractère
3. mélange les valeurs dans une variable `U64`
4. renvoie le hash final

Le hash retourné est stocké sur **64 bits**.

## Remarque

Le projet est **non fini** et a pour but de comparer un hashage sha256 à un hashage en holyc fait maison


