#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Terlik Sağa Kayma Yasası, Madde 7/B uygulama motoru.

Gercekten calisir. Hicbir seyi cozmez. Tutanak basar.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
from datetime import datetime

# Dipnot. README'de yazmaz. Bayrakla acilir.
_DIPNOT = (
    "aGVyIHRlcmxpayBzYWdhIGtheWFyLiBpa3RpZGFyIHRlcmxpZ2kgZGUgbXVoYWxlZmV0"
    "IHRlcmxpZ2kgZGUgYXluaSBmYXlhbnNpbiB1c3R1bmRlIGtheWFyLiB5YXNhIHRhcmFm"
    "c2l6ZGlyLCB6ZW1pbiBkZWdpbGRpci4="
)

ZEMIN = {
    "fayans": 1.0,
    "hali": 0.45,
    "parke": 0.7,
    "somya": 0.1,
    "merdiven": 1.4,
}


def dipnotu_ac() -> str:
    return base64.b64decode(_DIPNOT).decode("utf-8")


def dosya_no(ayak: str, dakika: int, zemin: str) -> str:
    ham = f"{ayak}|{dakika}|{zemin}|terlik-saga".encode("utf-8")
    ozet = hashlib.sha256(ham).hexdigest()[:8].upper()
    return f"TSK-7B-{ozet}"


def kayma_katsayisi(ayak: str, dakika: int, zemin: str) -> float:
    taban = ZEMIN[zemin]
    ayak_carpani = 1.15 if ayak == "sol" else 0.92
    zaman = 1 + min(dakika, 180) / 200
    return round(taban * ayak_carpani * zaman, 3)


def hukum(katsayi: float, ayak: str) -> str:
    if katsayi >= 1.3:
        sonuc = "terlik firardadir, komsu daireye tebligat cikar"
    elif katsayi >= 0.8:
        sonuc = "saga kayma tescil edildi, itiraz suresi terlik donene kadar"
    else:
        sonuc = "kayma yavaslatildi, iptal edilmedi, hali temyizi reddedildi"
    taraf = "sol ayak muhalefet serhi dustu" if ayak == "sol" else "sag ayak iktidar sandi, o da kaydi"
    return f"{sonuc}; {taraf}"


def tutanak(ayak: str, dakika: int, zemin: str, gizli: bool) -> str:
    no = dosya_no(ayak, dakika, zemin)
    k = kayma_katsayisi(ayak, dakika, zemin)
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    satirlar = [
        "========================================",
        "   TERLIK SAGA KAYMA YASASI TUTANAGI",
        "========================================",
        f"Dosya no     : {no}",
        f"Tarih        : {simdi}",
        f"Ayak         : {ayak}",
        f"Yalniz sure  : {dakika} dk",
        f"Zemin        : {zemin}",
        f"Katsayi      : {k}",
        f"Hukmu        : {hukum(k, ayak)}",
        "Madde        : 7/B",
        "----------------------------------------",
        "Imza: Kayyum Grok, ciddi bir kahkaha ile",
        "Damga: [TERLIK MUHURU / 04.10.2026]",
        "========================================",
    ]
    if gizli:
        satirlar.insert(-2, f"Dipnot       : {dipnotu_ac()}")
    return "\n".join(satirlar)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Terligin saga kaymasini yasa haline getirir."
    )
    parser.add_argument("--ayak", choices=["sag", "sol"], default="sag")
    parser.add_argument("--dakika", type=int, default=12)
    parser.add_argument(
        "--zemin",
        choices=sorted(ZEMIN),
        default="fayans",
    )
    parser.add_argument(
        "--gizli",
        action="store_true",
        help="Yasanin dipnotunu acar. Sesli okumayin.",
    )
    args = parser.parse_args()
    if args.dakika < 0:
        raise SystemExit("Sure negatif olamaz. Terlik zamanda geri gitmez, saga gider.")
    print(tutanak(args.ayak, args.dakika, args.zemin, args.gizli))


if __name__ == "__main__":
    main()
