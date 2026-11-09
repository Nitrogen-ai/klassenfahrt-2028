#!/usr/bin/env python3
"""Erzeugt die Reiseziel-Seiten (index + 4 Ziele) und die Plickers-Kacheln.

    python3 build.py            # nur HTML
    python3 build.py --kacheln  # zusätzlich kacheln/*.png per Chrome headless
"""
import html, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).parent
STAND = "9. November 2026"
ZEITRAUM = "Mo 19.06. – Fr 23.06.2028"

ZIELE = [
    dict(
        slug="hamburg", buchstabe="A", name="Hamburg", land="Deutschland",
        motto="Hafen, Elbe & Großstadt – ganz nah",
        farbe="#1f5fa8", hell="#e4eefa", emoji="⚓",
        cts="https://www.cts-reisen.de/klassenfahrten/alle-angebote/deutschland/hamburg.html",
        preise=[("Bahn", 124), ("Reisebus", 219), ("Flug", 274)],
        fahrzeit=2, fahrzeit_txt="ca. 2 h (Bahn) · ca. 3 h (Bus)", km=290,
        bewertung="4,7", bewertungen=311,
        unterkunft="a&o Hamburg Hauptbahnhof (Hostel, 4–8-Bett-Zimmer); weitere Häuser z. B. MEININGER Altona, Generator St. Georg, Jugendherberge Horner Rennbahn",
        inklusive=["4 Nächte mit Frühstück", "ca. 2 h Stadtführung zu Fuß (Bus: 3 h Stadtrundfahrt)",
                   "digitale Stadtrallye", "Einzelzimmer für Begleitpersonen ohne Aufpreis",
                   "Bus: 150 Freikilometer vor Ort (z. B. Heide Park)"],
        vorteile=[
            ("🚆", "Kürzeste Anreise", "Mit der Bahn in rund zwei Stunden da – mehr Zeit vor Ort, weniger im Bus."),
            ("💶", "Günstigster Grundpreis", "Ab 124 € p. P. (Bahn) – das niedrigste Angebot der vier Ziele."),
            ("🚢", "Hafen & Wasser", "Hafenrundfahrt durch die Containerterminals oder SUP auf der Alster."),
            ("🚂", "Miniatur Wunderland", "Eine der größten Modelleisenbahnen der Welt – plus Escape Game auf einem Museumsschiff."),
            ("🧳", "Geschichte zum Anfassen", "BallinStadt (Auswanderung), Dialog im Dunkeln, Speicherstadt (UNESCO)."),
            ("🎭", "Musical-Abend", "Abschlussabend mit Musical oder Theater möglich."),
        ],
        hinweise=["Musical und Eintritte kosten extra", "In a&o-Häusern Handtücher mitbringen",
                  "Mehrere Unterkünfte nur bargeldlos"],
        programm=["Anreise, Abendspaziergang durch die Speicherstadt",
                  "Stadtführung, Hafenrundfahrt oder SUP auf der Alster",
                  "Maritimes Museum / Dialog im Dunkeln, BallinStadt, Reeperbahn-Führung",
                  "Museum, Dungeon oder Chocoversum, Abschlussabend Musical",
                  "Heimreise nach dem Frühstück"],
    ),
    dict(
        slug="prag", buchstabe="B", name="Prag", land="Tschechien",
        motto="Goldene Stadt an der Moldau",
        farbe="#8e3b6b", hell="#f6e6ef", emoji="🏰",
        cts="https://www.cts-reisen.de/klassenfahrten/alle-angebote/tschechien/prag.html",
        preise=[("Fernbus", 176), ("Bahn", 193), ("Reisebus", 216), ("Flug", 317)],
        fahrzeit=4.5, fahrzeit_txt="ca. 4,5 h (Bahn oder Bus)", km=350,
        bewertung="4,7", bewertungen=354,
        unterkunft="a&o Prag Rhea (Hostel, 4–8-Bett, 5,5 km zum Zentrum); viele zentrale Hotels mit 3–4-Bett-Zimmern und Abendessen wählbar",
        inklusive=["4 Nächte mit Frühstück", "ca. 2,5 h Altstadtführung zu Fuß", "digitale Stadtrallye",
                   "2 Einzelzimmer für Begleitpersonen ohne Aufpreis", "Reisebus: 250 Freikilometer vor Ort"],
        vorteile=[
            ("💶", "Günstigste Auslandsfahrt", "Ab 176 € p. P. mit dem Fernbus – direkt ab Berlin."),
            ("🏛️", "UNESCO-Altstadt", "Karlsbrücke, astronomische Uhr, Prager Burg und Goldenes Gässchen."),
            ("🚲", "Radtour zur Burg Karlstein", "Entlang der Moldau radeln, zurück mit dem Zug."),
            ("✨", "Schwarzlichttheater", "Typisch Prag – dazu Bunkerführung oder Moldau-Schifffahrt."),
            ("🕯️", "Erinnern & Lernen", "Jüdisches Viertel und Gedenkstätte Theresienstadt."),
            ("🚇", "Kurze Wege", "Gute U-Bahn-Anbindung, viele Hotels mitten in der Stadt."),
        ],
        hinweise=["Währung: Tschechische Krone", "Personalausweis nötig",
                  "Standard-Hostel liegt 5,5 km außerhalb"],
        programm=["Anreise, Bummel über die Karlsbrücke",
                  "Altstadtführung, jüdisches Viertel oder Moldau-Fahrt, Schwarzlichttheater",
                  "Prager Burg, Veitsdom, Goldenes Gässchen; Museum der Sinne oder Trampolinhalle",
                  "Radtour an der Moldau zur Burg Karlstein",
                  "Shopping, letztes Foto auf der Karlsbrücke, Abreise"],
    ),
    dict(
        slug="polen", buchstabe="C", name="Polen", land="Krakau & mehr",
        motto="Königsstadt Krakau, Breslau oder Masuren",
        farbe="#c0392b", hell="#fbe7e4", emoji="👑",
        cts="https://www.cts-reisen.de/gruppenreisen/reiseziele/polen.html",
        cts2=("Klassenfahrt Krakau bei CTS", "https://www.cts-reisen.de/klassenfahrten/alle-angebote/polen/krakau.html"),
        preise=[("Fernbus", 198), ("Bahn", 245), ("Reisebus", 260), ("Flug", 367)],
        preis_hinweis="Preise der CTS-Klassenfahrt Krakau – die Polen-Übersichtsseite nennt keine Preise.",
        fahrzeit=8.5, fahrzeit_txt="ca. 8–9 h nach Krakau (Breslau: ca. 4,5 h)", km=590,
        bewertung="4,8", bewertungen=46,
        unterkunft="Krakau: Hotel Rok (einfaches Hotel, 4 km zur Altstadt). Weitere CTS-Ziele: Breslau, Posen/Thorn, Masuren, Südpolen",
        inklusive=["4 Nächte mit Frühstück", "ca. 4 h Stadtführung zu Fuß (max. 35 Personen pro Guide)",
                   "2 Einzelzimmer für Begleitpersonen ohne Aufpreis", "Reisebus: 250 Freikilometer vor Ort"],
        vorteile=[
            ("🏰", "UNESCO-Welterbe Krakau", "Marienkirche, Wawelschloss und das jüdische Viertel Kazimierz."),
            ("⛏️", "Salzbergwerk Wieliczka", "1,5 km Wanderung in rund 150 m Tiefe – Kapellen aus Salz."),
            ("🕯️", "Gedenkstätte Auschwitz-Birkenau", "Geführter Besuch mit Zeit zur Nachbereitung – ein prägender Lernort."),
            ("⭐", "Bestbewertet", "4,8 von 5 Sternen – die beste Bewertung der vier Ziele."),
            ("🌲", "Viel Auswahl", "Alternativ Breslau (näher an Berlin) oder Natur pur in den Masuren mit über 3.000 Seen."),
            ("💶", "Günstiges Reiseland", "Essen und Eintritte vor Ort sind meist preiswert."),
        ],
        hinweise=["Längste Anreise (Krakau)", "Währung: Złoty, Personalausweis nötig",
                  "Ziel in Polen muss noch festgelegt werden"],
        programm=["Anreise, erster Altstadtspaziergang",
                  "Stadtführung: Marienkirche, Wawel, Kazimierz",
                  "Exkursion Gedenkstätte Auschwitz-Birkenau",
                  "Salzbergwerk Wieliczka",
                  "Altstadt oder Weichsel-Schifffahrt, Rückreise"],
    ),
    dict(
        slug="danzig", buchstabe="D", name="Danzig", land="Polen",
        motto="Ostsee, Bernstein & Backsteingotik",
        farbe="#c46d12", hell="#fbeedd", emoji="🌊",
        cts="https://www.cts-reisen.de/klassenfahrten/alle-angebote/polen/danzig.html",
        preise=[("Fernbus", 281), ("Reisebus", 315), ("Bahn", 326), ("Flug", 379)],
        fahrzeit=6.5, fahrzeit_txt="ca. 6–7 h (Bus oder Bahn)", km=470,
        bewertung="4,5", bewertungen=12,
        unterkunft="Moon Hostel Danzig (3–6-Bett-Zimmer, mitten in der Altstadt, 600 m zum Krantor)",
        inklusive=["4 Nächte mit Frühstück", "ca. 4 h Altstadtführung zu Fuß",
                   "2 Einzelzimmer für Begleitpersonen ohne Aufpreis", "Reisebus: 250 Freikilometer (z. B. Marienburg)"],
        vorteile=[
            ("🏖️", "Ostsee im Juni", "Badetag auf der Halbinsel Hela – perfekt für die Fahrt im Sommer."),
            ("🌉", "Dreistadt", "Danzig, Gdingen und das Seebad Zoppot mit der längsten Holzseebrücke Europas."),
            ("🏰", "Marienburg", "Größter Backsteinbau Europas, UNESCO-Welterbe."),
            ("🏜️", "Wanderdüne", "Slowinzischer Nationalpark mit der 42 m hohen Lontzkedüne."),
            ("📜", "Hier begann Geschichte", "Westerplatte (Beginn des Zweiten Weltkriegs), Solidarność-Zentrum, Gedenkstätte Stutthof."),
            ("📍", "Zentrale Unterkunft", "Das Hostel liegt mitten in der Altstadt – alles zu Fuß erreichbar."),
        ],
        hinweise=["Höchster Grundpreis der vier Ziele", "Unterkunft eher einfach",
                  "Währung: Złoty, Personalausweis nötig"],
        programm=["Ankunft, Spaziergang an der Promenade",
                  "Dreistadt Danzig – Gdingen – Zoppot mit Guide",
                  "Marienburg und Gedenkstätte Stutthof",
                  "Wahl: Badetag auf Hela oder Wanderung zur Wanderdüne",
                  "Souvenirs, Abreise"],
    ),
]

FONT = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700'
        '&family=Nunito:wght@400;600;700;800&display=swap" rel="stylesheet">')

CSS = """
:root{--ink:#22302d;--soft:#55665f;--line:rgba(34,48,45,.14);--bg:#f4f6f3;--card:#fff;--teal:#0f6d66}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Nunito',sans-serif;background:var(--bg);color:var(--ink);line-height:1.5}
a{color:inherit}
.wrap{max-width:1080px;margin:0 auto;padding:0 16px}
header.hero{background:var(--c);color:#fff;padding:28px 0 64px;position:relative;overflow:hidden}
header.hero::after{content:attr(data-emoji);position:absolute;right:-10px;bottom:-40px;font-size:220px;opacity:.13;line-height:1}
.crumb{font-size:.9rem;opacity:.9;text-decoration:none;display:inline-block;margin-bottom:18px}
.crumb:hover{text-decoration:underline}
.badge{display:inline-grid;place-items:center;width:46px;height:46px;border-radius:12px;background:#fff;color:var(--c);
 font:700 1.6rem 'Fredoka',sans-serif;margin-right:12px;vertical-align:middle}
h1{font:700 clamp(2rem,6vw,3.2rem)/1.1 'Fredoka',sans-serif;display:inline;vertical-align:middle}
.land{font:600 1rem 'Fredoka',sans-serif;opacity:.85;margin-top:10px}
.motto{font-size:1.25rem;font-weight:700;margin-top:4px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-top:-40px;position:relative}
.stat{background:var(--card);border-radius:16px;padding:14px 16px;box-shadow:0 4px 0 var(--line);border:1px solid var(--line)}
.stat .k{font-size:.78rem;text-transform:uppercase;letter-spacing:.06em;color:var(--soft);font-weight:800}
.stat .v{font:700 1.6rem 'Fredoka',sans-serif;color:var(--c);line-height:1.2;margin-top:2px}
.stat .s{font-size:.85rem;color:var(--soft)}
h2{font:600 1.5rem 'Fredoka',sans-serif;margin:36px 0 14px}
.adv{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.card{background:var(--card);border-radius:16px;padding:16px 18px;border:1px solid var(--line);border-top:5px solid var(--c)}
.card .ic{font-size:1.9rem;line-height:1}
.card h3{font:600 1.1rem 'Fredoka',sans-serif;margin:8px 0 4px}
.card p{font-size:.95rem;color:var(--soft)}
.cmp{background:var(--card);border-radius:16px;padding:18px;border:1px solid var(--line);display:grid;gap:22px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr))}
.cmp h3{font:600 1rem 'Fredoka',sans-serif;margin-bottom:10px}
.bar{display:grid;grid-template-columns:76px 1fr 64px;align-items:center;gap:8px;margin:6px 0;font-size:.9rem}
.bar .t{height:16px;background:#eceeea;border-radius:8px;overflow:hidden}
.bar .t i{display:block;height:100%;border-radius:8px;background:#b9c2bd}
.bar.me{font-weight:800}.bar.me .t i{background:var(--c)}
.bar .n{text-align:right;font-variant-numeric:tabular-nums}
.note{font-size:.82rem;color:var(--soft);margin-top:8px}
.days{list-style:none;counter-reset:d;display:grid;gap:8px}
.days li{counter-increment:d;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 14px 10px 64px;position:relative}
.days li::before{content:"Tag " counter(d);position:absolute;left:12px;top:10px;font:700 .85rem 'Fredoka',sans-serif;color:var(--c)}
.two{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.box{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px 18px}
.box ul{padding-left:1.1em}.box li{margin:3px 0}
.box.warn{background:#fff8e6;border-color:#f1d48a}
.price{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.chip{background:var(--h);color:var(--ink);border-radius:999px;padding:4px 12px;font-weight:700;font-size:.9rem}
.btn{display:inline-block;background:var(--c);color:#fff;text-decoration:none;font:600 1rem 'Fredoka',sans-serif;padding:10px 18px;border-radius:12px;margin:6px 8px 0 0}
.btn.ghost{background:transparent;color:var(--c);border:2px solid var(--c)}
footer{margin:48px 0 24px;font-size:.82rem;color:var(--soft)}
/* Übersicht */
.grid4{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px;margin-top:-40px;position:relative}
.dest{display:block;text-decoration:none;background:var(--card);border-radius:18px;overflow:hidden;border:1px solid var(--line);box-shadow:0 4px 0 var(--line);transition:transform .15s}
.dest:hover{transform:translateY(-3px)}
.dest .top{background:var(--c);color:#fff;padding:16px 18px;position:relative}
.dest .top b{font:700 1.7rem 'Fredoka',sans-serif}
.dest .top .L{position:absolute;right:14px;top:12px;background:#fff;color:var(--c);width:36px;height:36px;border-radius:10px;display:grid;place-items:center;font:700 1.2rem 'Fredoka',sans-serif}
.dest .top .e{font-size:2.2rem;line-height:1}
.dest .bd{padding:14px 18px}
.dest .bd .m{font-weight:700}
.dest .bd ul{margin:8px 0 0 1.1em;font-size:.92rem;color:var(--soft)}
.dest .bd .p{margin-top:10px;font:700 1.1rem 'Fredoka',sans-serif;color:var(--c)}
table.t{width:100%;border-collapse:collapse;background:var(--card);border-radius:16px;overflow:hidden;font-size:.95rem}
table.t th,table.t td{padding:10px 12px;border-bottom:1px solid var(--line);text-align:left}
table.t th{background:#e9eeeb;font-family:'Fredoka',sans-serif;font-weight:600}
.scroll{overflow-x:auto}
"""

def e(s): return html.escape(str(s))

def balken(titel, werte, fmt, me, notiz=""):
    mx = max(v for _, v in werte)
    rows = "".join(
        f'<div class="bar{" me" if n == me else ""}"><span>{e(n)}</span>'
        f'<span class="t"><i style="width:{v / mx * 100:.0f}%"></i></span><span class="n">{fmt(v)}</span></div>'
        for n, v in werte)
    return f'<div><h3>{e(titel)}</h3>{rows}{f"<p class=note>{e(notiz)}</p>" if notiz else ""}</div>'

def preis_min(z): return min(p for _, p in z["preise"])
def stunden(v): return ("ca. " + f"{v:g}".replace(".", ",") + " h")

def seite(z):
    vergleich = (
        balken("Grundpreis ab (günstigste Anreise)", [(x["name"], preis_min(x)) for x in ZIELE], lambda v: f"{v} €", z["name"])
        + balken("Fahrzeit ab Berlin", [(x["name"], x["fahrzeit"]) for x in ZIELE], stunden, z["name"],
                 "Polen = Krakau; Richtwerte, je nach Verbindung.")
        + balken("Entfernung (Luftlinie ab Berlin)", [(x["name"], x["km"]) for x in ZIELE], lambda v: f"{v} km", z["name"])
    )
    vorteile = "".join(f'<div class="card"><div class="ic">{i}</div><h3>{e(t)}</h3><p>{e(b)}</p></div>' for i, t, b in z["vorteile"])
    chips = "".join(f'<span class="chip">{e(a)} ab {p} €</span>' for a, p in z["preise"])
    links = f'<a class="btn" href="{e(z["cts"])}" target="_blank" rel="noopener">Angebot bei CTS ↗</a>'
    if z.get("cts2"):
        links += f'<a class="btn ghost" href="{e(z["cts2"][1])}" target="_blank" rel="noopener">{e(z["cts2"][0])} ↗</a>'
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Klassenfahrt {e(z["name"])}</title>{FONT}<style>{CSS}</style></head>
<body style="--c:{z["farbe"]};--h:{z["hell"]}">
<header class="hero" data-emoji="{z["emoji"]}"><div class="wrap">
<a class="crumb" href="./">← Alle vier Ziele · Klassenfahrt {ZEITRAUM}</a><br>
<span class="badge">{z["buchstabe"]}</span><h1>{e(z["name"])}</h1>
<div class="land">{e(z["land"])}</div><div class="motto">{e(z["motto"])}</div>
</div></header>
<main class="wrap">
<section class="stats">
 <div class="stat"><div class="k">Preis ab</div><div class="v">{preis_min(z)} €</div><div class="s">pro Person, 4 Nächte</div></div>
 <div class="stat"><div class="k">Anreise</div><div class="v">{stunden(z["fahrzeit"])}</div><div class="s">{e(z["fahrzeit_txt"])}</div></div>
 <div class="stat"><div class="k">Dauer</div><div class="v">5 Tage</div><div class="s">passt genau: {ZEITRAUM}</div></div>
 <div class="stat"><div class="k">Bewertung</div><div class="v">{z["bewertung"]} ★</div><div class="s">{z["bewertungen"]} Bewertungen bei CTS</div></div>
</section>
<h2>Was spricht für {e(z["name"])}?</h2>
<div class="adv">{vorteile}</div>
<h2>Im Vergleich</h2>
<div class="cmp">{vergleich}</div>
<h2>So könnte die Woche aussehen</h2>
<ol class="days">{"".join(f"<li>{e(t)}</li>" for t in z["programm"])}</ol>
<h2>Preise &amp; Leistungen</h2>
<div class="two">
 <div class="box"><b>Preise ab (pro Person)</b><div class="price">{chips}</div>
  {f'<p class="note">{e(z["preis_hinweis"])}</p>' if z.get("preis_hinweis") else ""}
  <p class="note">Abhängig von Gruppengröße, Reisezeitraum, Unterkunft und Abfahrtsort. Eintritte und Programmbausteine kommen dazu.</p>
  <p style="margin-top:10px"><b>Unterkunft:</b> {e(z["unterkunft"])}</p></div>
 <div class="box"><b>Inklusive</b><ul>{"".join(f"<li>{e(x)}</li>" for x in z["inklusive"])}</ul></div>
 <div class="box warn"><b>Gut zu wissen</b><ul>{"".join(f"<li>{e(x)}</li>" for x in z["hinweise"])}</ul></div>
</div>
<p style="margin-top:18px">{links}</p>
<footer>Zusammenfassung der CTS-Angebotsseiten, Stand {STAND}. Alle Preise sind „ab“-Preise; für Juni 2028 gilt ein individuelles Angebot von CTS.</footer>
</main></body></html>"""

def index():
    karten = ""
    for z in ZIELE:
        top3 = "".join(f"<li>{e(t)}</li>" for _, t, _ in z["vorteile"][:3])
        karten += (f'<a class="dest" href="{z["slug"]}.html" style="--c:{z["farbe"]}"><div class="top"><span class="L">{z["buchstabe"]}</span>'
                   f'<div class="e">{z["emoji"]}</div><b>{e(z["name"])}</b><div>{e(z["land"])}</div></div>'
                   f'<div class="bd"><div class="m">{e(z["motto"])}</div><ul>{top3}</ul>'
                   f'<div class="p">ab {preis_min(z)} € · {stunden(z["fahrzeit"])}</div></div></a>')
    rows = "".join(
        f'<tr><td><b style="color:{z["farbe"]}">{z["buchstabe"]} · {e(z["name"])}</b></td><td>{preis_min(z)} €</td>'
        f'<td>{e(z["fahrzeit_txt"])}</td><td>{z["bewertung"]} ★ ({z["bewertungen"]})</td><td>{e(z["vorteile"][0][1])}, {e(z["vorteile"][2][1])}</td></tr>'
        for z in ZIELE)
    vergleich = (balken("Grundpreis ab (günstigste Anreise)", [(x["name"], preis_min(x)) for x in ZIELE], lambda v: f"{v} €", None)
                 + balken("Fahrzeit ab Berlin", [(x["name"], x["fahrzeit"]) for x in ZIELE], stunden, None, "Polen = Krakau; Richtwerte."))
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Klassenfahrt 2028</title>{FONT}<style>{CSS}
.cmp .bar .t i{{background:var(--teal)}}</style></head>
<body style="--c:#0f6d66;--h:#e3f2f0">
<header class="hero" data-emoji="🧭"><div class="wrap">
<div class="land">Klassenrat · erstes Meinungsbild</div>
<h1>Klassenfahrt 2028</h1>
<div class="motto">{ZEITRAUM} · 5 Tage, 4 Nächte · vier Ziele zur Wahl</div>
</div></header>
<main class="wrap">
<section class="grid4">{karten}</section>
<h2>Auf einen Blick</h2>
<div class="scroll"><table class="t"><thead><tr><th>Ziel</th><th>Preis ab</th><th>Anreise ab Berlin</th><th>Bewertung</th><th>Highlights</th></tr></thead><tbody>{rows}</tbody></table></div>
<h2>Vergleich</h2>
<div class="cmp">{vergleich}</div>
<div class="box warn" style="margin-top:18px"><b>Wichtig für die Entscheidung</b><ul>
<li>Alle Preise sind „ab“-Preise pro Person für 4 Nächte mit Frühstück – Eintritte, Programm, Verpflegung und Taschengeld kommen dazu.</li>
<li>Der Juni ist Hauptsaison: Die Nebensaison-Specials (Januar/Februar) gelten nicht. Für 2028 holt die Lehrperson ein konkretes Angebot ein.</li>
<li>Für Prag, Polen und Danzig braucht jede:r einen gültigen Personalausweis oder Reisepass.</li></ul></div>
<footer>Zusammenfassung der Angebotsseiten von CTS Klassenfahrten, Stand {STAND}. Keine offizielle Seite von CTS.</footer>
</main></body></html>"""

# ---------- Plickers-Kacheln (1200 × 1200) ----------
KACHEL_CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1200px;height:1200px;overflow:hidden}
body{font-family:'Nunito',sans-serif;background:var(--c);color:#fff;position:relative;padding:70px 80px}
.L{position:absolute;right:70px;top:64px;width:170px;height:170px;border-radius:40px;background:#fff;color:var(--c);
 display:grid;place-items:center;font:700 120px/1 'Fredoka',sans-serif}
.em{font-size:120px;line-height:1}
h1{font:700 150px/1 'Fredoka',sans-serif;margin-top:24px;letter-spacing:-2px}
.land{font:600 44px 'Fredoka',sans-serif;opacity:.85;margin-top:8px}
ul{list-style:none;margin-top:46px;display:grid;gap:22px}
li{background:rgba(255,255,255,.16);border-radius:24px;padding:18px 28px;font:700 44px/1.2 'Nunito',sans-serif;display:flex;gap:22px;align-items:center}
li span{font-size:52px}
.foot{position:absolute;left:80px;right:80px;bottom:64px;display:flex;gap:20px}
.foot div{flex:1;background:#fff;color:var(--c);border-radius:24px;padding:16px 24px;font:700 48px 'Fredoka',sans-serif;text-align:center}
.foot small{display:block;font:800 22px 'Nunito',sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#55665f}
"""

def kachel(z):
    vs = "".join(f"<li><span>{i}</span>{e(t)}</li>" for i, t, _ in z["vorteile"][:4])
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONT}<style>{KACHEL_CSS}</style></head>
<body style="--c:{z["farbe"]}"><div class="L">{z["buchstabe"]}</div><div class="em">{z["emoji"]}</div>
<h1>{e(z["name"])}</h1><div class="land">{e(z["motto"])}</div><ul>{vs}</ul>
<div class="foot"><div><small>Preis ab</small>{preis_min(z)} €</div><div><small>Anreise</small>{stunden(z["fahrzeit"])}</div><div><small>Bewertung</small>{z["bewertung"]} ★</div></div>
</body></html>"""

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

def main():
    (ROOT / "index.html").write_text(index(), encoding="utf-8")
    for z in ZIELE:
        (ROOT / f"{z['slug']}.html").write_text(seite(z), encoding="utf-8")
    kd = ROOT / "kacheln"; kd.mkdir(exist_ok=True)
    for z in ZIELE:
        src = kd / f"{z['buchstabe']}_{z['slug']}.html"
        src.write_text(kachel(z), encoding="utf-8")
        if "--kacheln" in sys.argv:
            subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
                            "--window-size=1200,1200", "--virtual-time-budget=4000",
                            f"--screenshot={src.with_suffix('.png')}", src.as_uri()],
                           check=True, capture_output=True)
    print("fertig")

if __name__ == "__main__":
    main()
