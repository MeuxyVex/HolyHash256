# Hashage simple en HolyC

Petit projet en **HolyC** qui calcule un **hash maison 256 bits inspire de SHA-256**.

Le projet est maintenant organise pour deux usages :

- **CLI** : lancer un binaire et saisir une ligne de texte ;
- **bibliotheque native** : appeler des fonctions reutilisables depuis un autre langage, par exemple **Python avec `ctypes`**.

## API exposee

Le fichier principal `hashage.HC` contient maintenant trois fonctions utiles pour une integration externe :

- `HashTextRaw(U8 *s, U32 digest[8])` : calcule le digest brut sur 8 mots de 32 bits ;
- `DigestToHex(U32 digest[8], U8 *hex_out)` : convertit le digest brut en 64 caracteres hexadecimaux ;
- `HashTextHex(U8 *s, U8 *hex_out)` : calcule directement le hash hexadecimal dans un buffer de **65 octets** (`64` caracteres + `\0`).

L'algorithme reste un **hash maison non standard** : il est **inspire de SHA-256**, mais il **n'est pas compatible SHA-256** et ne doit pas etre presente comme un hash cryptographique officiel.

## Structure de l'algorithme

Le coeur du melange repose sur :

- un etat de **8 mots de 32 bits** ;
- des rotations et XOR ;
- les fonctions `Ch` et `Maj` ;
- un message schedule sur **64 rounds** ;
- un padding de type SHA-like sur blocs de **64 octets**.

## Utilisation en CLI

### Compiler

```bash
hcc hashage.HC
```

### Executer

```bash
./a.out
```

### Exemple

```text
Texte a hash : bonjour tout le monde
Texte lu : bonjour tout le monde
Algorithme : Hash maison 256 bits inspire de SHA-256
API lib : HashTextRaw / HashTextHex / DigestToHex
Longueur max supportee : 255 caracteres
Hash (hex) : 64-caracteres-hexadecimaux
```

## Utilisation comme bibliotheque native

L'objectif de cette version est de rendre l'algo appelable depuis un autre langage sans passer par `scanf` ni parser une sortie console complete.

### Fonction la plus pratique

Pour une integration externe, la fonction la plus simple est :

```c
U0 HashTextHex(U8 *s, U8 *hex_out)
```

Attendu :

- `s` pointe vers une chaine terminee par `\0` ;
- `hex_out` pointe vers un buffer de **65 octets minimum** ;
- la fonction ecrit un hash hexadecimal en majuscules puis un terminateur nul.

### Integration Python via `ctypes`

Un exemple plus robuste est fourni dans `python_ctypes_example.py` : il accepte un chemin de bibliotheque en argument, regarde aussi `HOLYC_HASH_LIB`, ignore les fichiers qui ne ressemblent pas a des `.so`, puis affiche une erreur claire si aucune bibliotheque chargeable n'est trouvee.

Principe :

1. charger une future bibliotheque partagee (ex. `libholyc_hash.so`) ;
2. accepter eventuellement son chemin via argument CLI ou `HOLYC_HASH_LIB` ;
3. ignorer les binaires executables qui ne sont pas des bibliotheques partagees ;
4. declarer la signature de `HashTextHex` ;
5. envoyer un `bytes` UTF-8 ;
6. recuperer le buffer de sortie hexadecimal.

Extrait Python :

```python
import ctypes

# soit : python3 python_ctypes_example.py "bonjour" /chemin/vers/libholyc_hash.so
# soit : HOLYC_HASH_LIB=/chemin/vers/libholyc_hash.so python3 python_ctypes_example.py

lib = load_library()
lib.HashTextHex.argtypes = [ctypes.c_char_p, ctypes.POINTER(ctypes.c_char)]
lib.HashTextHex.restype = None

out = ctypes.create_string_buffer(65)
lib.HashTextHex(b"bonjour tout le monde", out)
print(out.value.decode("ascii"))
```

## Limites actuelles

- le binaire CLI lit toujours une seule ligne avec `scanf(" %255[^\n]", texte)` ;
- l'entree CLI est limitee a **255 caracteres** ;
- la partie **bibliotheque** est prete au niveau API, mais la commande exacte pour produire une `.so` depend encore de ton environnement `hcc` Ubuntu ;
- comme il s'agit d'un hash maison, il faut ajouter des **tests de reference** si tu veux garantir la compatibilite entre HolyC et Python.

## Fichiers

- `hashage.HC` : implementation du hash, API reutilisable et CLI ;
- `python_ctypes_example.py` : exemple Python avec recherche de bibliotheque, filtrage des faux positifs (comme un `a.out` executable) et message d'erreur utile si aucun `.so` valide n'est disponible.

## Pistes suivantes

- ajouter des vecteurs de test fixes ;
- produire un vrai build de bibliotheque partagee si `hcc` le permet ;
- ajouter un petit wrapper Python plus ergonomique ;
- envisager ensuite un package `pip` qui charge la lib native.
