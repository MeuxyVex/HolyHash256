extern "c" I32 scanf(U8 *fmt, ...); // lecture de l'entree standard via scanf cote C

U32 RotR32(U32 x, I32 n)
{
    return (x >> n) | (x << (32 - n));
}

U32 Ch(U32 x, U32 y, U32 z)
{
    return (x & y) ^ (~x & z);
}

U32 Maj(U32 x, U32 y, U32 z)
{
    return (x & y) ^ (x & z) ^ (y & z);
}

U32 BigSigma0(U32 x)
{
    return RotR32(x, 2) ^ RotR32(x, 13) ^ RotR32(x, 22);
}

U32 BigSigma1(U32 x)
{
    return RotR32(x, 6) ^ RotR32(x, 11) ^ RotR32(x, 25);
}

U32 SmallSigma0(U32 x)
{
    return RotR32(x, 7) ^ RotR32(x, 18) ^ (x >> 3);
}

U32 SmallSigma1(U32 x)
{
    return RotR32(x, 17) ^ RotR32(x, 19) ^ (x >> 10);
}

U32 StrLen(U8 *s)
{
    U32 len = 0;

    while (s[len])
        len++;

    return len;
}

U32 LoadBE32(U8 *p)
{
    U32 b0, b1, b2, b3;

    b0 = p[0];
    b1 = p[1];
    b2 = p[2];
    b3 = p[3];

    return (b0 << 24) | (b1 << 16) | (b2 << 8) | b3;
}

U0 InitState(U32 state[8])
{
    state[0] = 0x6A09E667;
    state[1] = 0xBB67AE85;
    state[2] = 0x3C6EF372;
    state[3] = 0xA54FF53A;
    state[4] = 0x510E527F;
    state[5] = 0x9B05688C;
    state[6] = 0x1F83D9AB;
    state[7] = 0x5BE0CD19;
}

U0 ProcessBlock(U32 state[8], U8 *block)
{
    U32 k[16];
    U32 w[16];
    U32 a, b, c, d, e, f, g, h;
    U32 t1, t2;
    U32 round_salt;
    I32 i;

    k[0] = 0x428A2F98;  k[1] = 0x71374491;  k[2] = 0xB5C0FBCF;  k[3] = 0xE9B5DBA5;
    k[4] = 0x3956C25B;  k[5] = 0x59F111F1;  k[6] = 0x923F82A4;  k[7] = 0xAB1C5ED5;
    k[8] = 0xD807AA98;  k[9] = 0x12835B01;  k[10] = 0x243185BE; k[11] = 0x550C7DC3;
    k[12] = 0x72BE5D74; k[13] = 0x80DEB1FE; k[14] = 0x9BDC06A7; k[15] = 0xC19BF174;

    for (i = 0; i < 16; i++)
        w[i] = LoadBE32(block + i * 4);

    a = state[0];
    b = state[1];
    c = state[2];
    d = state[3];
    e = state[4];
    f = state[5];
    g = state[6];
    h = state[7];

    for (i = 0; i < 64; i++)
    {
        if (i >= 16)
            w[i & 15] = SmallSigma1(w[(i - 2) & 15]) + w[(i - 7) & 15] + SmallSigma0(w[(i - 15) & 15]) + w[(i - 16) & 15];

        round_salt = i * 0x9E3779B1;
        t1 = h + BigSigma1(e) + Ch(e, f, g) + k[i & 15] + w[i & 15] + round_salt;
        t2 = BigSigma0(a) + Maj(a, b, c);

        h = g;
        g = f;
        f = e;
        e = d + t1;
        d = c;
        c = b;
        b = a;
        a = t1 + t2;
    }

    state[0] += a;
    state[1] += b;
    state[2] += c;
    state[3] += d;
    state[4] += e;
    state[5] += f;
    state[6] += g;
    state[7] += h;
}

U0 HashStr(U8 *s, U32 digest[8]) // hash maison 256 bits inspire de SHA-256, mais non compatible SHA-256
{
    U8 buffer[320];
    U32 len;
    U32 total_len;
    U32 i;
    U32 block_count;
    U64 bit_len;

    len = StrLen(s);
    bit_len = len;
    bit_len *= 8;
    total_len = (len + 9 + 63) & ~63;

    for (i = 0; i < len; i++)
        buffer[i] = s[i];

    buffer[len] = 0x80;

    for (i = len + 1; i < total_len; i++)
        buffer[i] = 0;

    for (i = 0; i < 8; i++)
        buffer[total_len - 1 - i] = (bit_len >> (i * 8)) & 0xFF;

    InitState(digest);

    block_count = total_len / 64;

    for (i = 0; i < block_count; i++)
        ProcessBlock(digest, buffer + i * 64);
}

U0 PrintDigest(U32 digest[8])
{
    "Hash (hex) : %08X%08X%08X%08X%08X%08X%08X%08X\n",
        digest[0], digest[1], digest[2], digest[3],
        digest[4], digest[5], digest[6], digest[7];
}

U0 Main() // point d'entree principal
{
    U8 texte[256];
    U32 digest[8];
    I32 lu;

    "Texte a hash : ";
    lu = scanf(" %255[^\n]", texte); // lit jusqu'a 255 caracteres et conserve les espaces

    if (lu != 1)
    {
        "Aucune entree valide lue.\n";
        return;
    }

    HashStr(texte, digest);

    "Texte lu : %s\n", texte;
    "Algorithme : Hash maison 256 bits inspire de SHA-256\n";
    "Longueur max supportee : 255 caracteres\n";
    PrintDigest(digest);
}

Main;
