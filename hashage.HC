extern "c" I32 scanf(U8 *fmt, ...); // lecture de l'entrée standard via scanf côté C

U64 HashStr(U8 *s) // calcule un hash simple sur une chaîne terminée par '\0'
{
    U64 hash = 0;

    while (*s)
    {
        hash = hash * 31 + *s;
        s++;
    }

    return hash;
}

U0 Main() // point d'entrée principal
{
    U8 texte[256];
    U64 h;
    I32 lu;

    "Texte a hash : ";
    lu = scanf(" %255[^\n]", texte); // lit jusqu'à 255 caractères et conserve les espaces

    if (lu != 1)
    {
        "Aucune entree valide lue.\n";
        return;
    }

    h = HashStr(texte);

    "Texte lu : %s\n", texte;
    "Longueur max supportee : 255 caracteres\n";
    "Hash (hex) : %016X\n", h;
}

Main;
