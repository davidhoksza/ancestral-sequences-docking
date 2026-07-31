# P-loop a vazba ATP — podrobný referenční dokument

> Toto je rozšířená verze. Stručné shrnutí najdete v dokumentu *P-loop_vazba_ATP_shrnuti.md*, který slouží jako TL;DR k tomuto textu.

---

## 1. Úvod – co je P-loop

P-loop (phosphate-binding loop), také nazývaný **Walker A motiv**, je jeden z nejrozšířenějších a evolučně nejstarších strukturních motivů v proteinech vázajících nukleotidy (ATP, GTP). Tvoří smyčku mezi β-skládaným listem a α-helixem (typický **βαβ fold**) a jeho hlavní funkcí je obemknout a stabilizovat fosfátovou skupinu navázaného nukleotidu.

### 1.1 Konsenzuální sekvence

Konsenzus Walker A motivu je:

**G-x-x-x-x-G-K-[S/T]**

kde x označuje libovolnou aminokyselinu. Klíčové prvky:
- **Glyciny** (dvě konzervované pozice) – poskytují konformační flexibilitu potřebnou k tomu, aby se smyčka mohla ostře ohnout kolem fosfátů
- **Lysin** – jediné reziduum motivu s přímým specifickým postranním kontaktem na fosfáty
- **Serin/threonin** – koordinuje hořečnatý kation (Mg²⁺)

### 1.2 Výskyt napříč proteinovými rodinami

P-loop se vyskytuje v obrovském množství funkčně nepříbuzných rodin, například:
- ATPázy a GTPázy (Ras superrodina, myosin, kinesin)
- ABC transportéry
- Kinázy (proteinkinázy i metabolické kinázy)
- Helikázy
- Elongační faktory translace (EF-Tu, EF-G)

Tato všudypřítomnost naznačuje, že jde o jeden z evolučně nejstarších a nejkonzervovanějších strukturních řešení pro práci s nukleotidy – pravděpodobně se objevil velmi brzy v evoluci enzymů.

### 1.3 Sekvenční konsenzus vs. strukturní smyčka – proč se čísla liší

Je běžné narazit na rozpor mezi délkou motivu udávanou různými zdroji: **8 aminokyselin** (přísný sekvenční Walker A konsenzus) vs. **10–15 aminokyselin** (často uváděná délka).

Rozdíl vzniká tím, že jde o dva různé způsoby definice:
- **Sekvenční konsenzus** (G-x-x-x-x-G-K-[S/T]) měří jen tu striktně definovanou "core" sekvenci, kterou zachycují bioinformatické nástroje (regex-style pattern matching, profily PROSITE/Pfam) – to je těch 8 reziduí.
- **Strukturně definovaná P-loop** zahrnuje navíc část předcházejícího β-řetězce, ze kterého smyčka vychází, a případně pár reziduí za lysinem/serinem, které se ještě podílejí na obemknutí fosfátů – to dává 10–15 reziduí.

Obě čísla jsou tedy "správná", jen popisují mírně odlišnou věc: jedno je čistě sekvenční signatura, druhé je celý strukturní element ve 3D.

---

## 2. Struktura ATP – základní orientace

Než se pustíme do mechanismu vazby, je užitečné mít jasno ve struktuře samotného ATP.

### 2.1 Stavební bloky

ATP (adenosin-5'-trifosfát) se skládá ze tří částí:
- **Adenin** – dusíkatá báze (purin)
- **Ribóza** – pětiuhlíkatý cukr
- **Trifosfátový řetězec** – tři navázané fosfátové skupiny

### 2.2 Alfa, beta, gama fosfáty

Fosfáty tvoří lineární řetězec navázaný na 5'-uhlík ribózy:

```
Ribóza — O — Pα — O — Pβ — O — Pγ — O⁻ (a další O⁻)
```

- **Alfa (α)** fosfát je navázán přímo na ribózu (nejblíže cukru)
- **Beta (β)** fosfát je prostřední
- **Gama (γ)** fosfát je koncový, nejvzdálenější od cukru

Mezi fosfáty jsou tzv. **fosfoanhydridové vazby** – právě tyto vazby jsou ty "vysokoenergetické", jejichž štěpení je spojeno s uvolněním volné energie (viz kapitola 6.4).

Beta a gama fosfát společně tvoří tzv. **fosfátový "ocas"** ATP – tuto část molekuly P-loop obemyká a je to místo, které je při hydrolýze štěpeno.

*Viz přiložené schéma: `atp_schema.svg`*

### 2.3 Kde se štěpí při hydrolýze

Při hydrolýze ATP na ADP + Pi se štěpí vazba **mezi β a γ fosfátem**. Gama fosfát odchází jako volný anorganický fosfát (Pi), zbytek molekuly (adenin–ribóza–α–β) tvoří ADP.

### 2.4 Náboj ATP a proč je -4

Každý fosfát nese kyslíky, které mohou být buď protonované (–OH, neutrální), nebo deprotonované (–O⁻, záporně nabité) – závisí na pH prostředí (fosfátové skupiny jsou slabé kyseliny).

Počet "volných" kyslíků na jednotlivých fosfátech:
- **α-fosfát**: 1 volný kyslík (ostatní jsou vázány na ribózu a β-fosfát)
- **β-fosfát**: 1 volný kyslík
- **γ-fosfát**: 2 volné kyslíky (není vázán na žádný další fosfát)

Při fyziologickém pH (~7.4) je pKa těchto skupin nižší než pH prostředí, takže jsou **prakticky všechny deprotonované**:

- α: −1
- β: −1
- γ: −2

**Celkem: −4** → proto se mluví o ATP⁴⁻ jako o dominantní formě v buňce.

### 2.5 Jak funguje pH a proč je pro tohle relevantní

**pH = −log₁₀[H⁺]**, tedy záporný dekadický logaritmus molární koncentrace vodíkových iontů v roztoku. Je to logaritmická škála – rozdíl o 1 jednotku pH znamená desetinásobnou změnu koncentrace H⁺.

Fosfátová skupina se chová jako slabá kyselina, v roztoku je v rovnováze:

```
R-OH ⇌ R-O⁻ + H⁺
```

Tuto rovnováhu popisuje **Henderson-Hasselbalchova rovnice**:

```
pH = pKa + log([R-O⁻] / [R-OH])
```

- Když **pH > pKa** → převažuje deprotonovaná forma (R-O⁻)
- Když **pH < pKa** → převažuje protonovaná forma (R-OH)
- Když **pH = pKa** → přesně 50:50

Fosfátové OH skupiny ATP mají pKa v rozmezí zhruba 1–2 (první deprotonace) až 6.5–7 (poslední, nejpevněji vázaný proton). Protože fyziologické pH (7.4) je vyšší než všechny tyto hodnoty, rovnováha je silně posunuta k deprotonované formě – pro poslední skupinu (pKa ~7) vychází při pH 7.4 poměr O⁻:OH zhruba 2.5:1.

---

## 3. Molekulární kontakty mezi P-loop a ATP

### 3.1 Kompletní přehled kontaktů

| Část ATP | Interagující skupina/reziduum | Typ kontaktu |
|---|---|---|
| γ,β-fosfát | Backbone NH P-loop | Vodíkové vazby |
| γ,β-fosfát | Konzervovaný Lys (ε-NH₃⁺) | Solný můstek / H-vazby (bidentátně) |
| Mg²⁺ | Ser/Thr (P-loop) | Koordinační vazba |
| Mg²⁺ | Asp (Walker B) + vody | Koordinační vazba |
| γ-fosfát (katalýza) | Glu (Walker B) přes vodu | Aktivace nukleofilu |
| Adenin | Aromatická rezidua jinde v proteinu | π-stacking |
| Ribóza | Asp/Glu, backbone | Vodíkové vazby |

### 3.2 Proč kontakt zajišťuje především páteř, ne postranní řetězce glycinů

Glyciny v P-loop **nemají postranní řetězec** (jen atom vodíku), takže jejich role není přímá chemická interakce s ATP prostřednictvím postranního řetězce – to ani není možné. Jejich role je čistě **konformační**: umožňují smyčce se ohnout do těsného oblouku, který by s objemnějšími postranními řetězci nebyl stericky možný.

To ale neznamená, že by glyciny byly z kontaktu úplně vyloučené. Naopak – kontaktují ATP prostřednictvím **backbone amidových NH skupin**, tedy té části molekuly, kterou má společnou úplně každá aminokyselina (nejen glycin). Klíčová otázka tedy není "kdo kontaktuje", ale "proč musí být zrovna glycin, a ne třeba leucin, když backbone NH má každá aminokyselina":

- **Backbone NH má sice každá aminokyselina** – teoreticky by tedy mohla dělat stejnou vodíkovou vazbu
- **Ale objemný postranní řetězec** (např. u leucinu) by stericky bránil tomu, aby se smyčka ohnula do tak ostrého úhlu, jaký P-loop potřebuje

Glycin je tedy nutný kvůli konformační flexibilitě, ne kvůli nějaké unikátní chemii svého postranního řetězce (protože žádný nemá).

Jediný postranní řetězec v celém motivu, který dělá přímý, specifický chemický kontakt s fosfáty, je **postranní řetězec lysinu** (ε-NH₃⁺ skupina).

### 3.3 Proč gama fosfát dostává nejvíce kontaktů

Intuitivní by mohlo být domnívat se, že gama fosfát má víc kontaktů, protože je "hlouběji zanořený" do P-loop smyčky. Ve skutečnosti P-loop netvoří tunel, do kterého by ATP zajíždělo "ocasem napřed" – je to spíš mělká kolébka, přes kterou leží celý fosfátový řetězec vedle sebe, zhruba v jedné rovině. Z hlediska hloubky zanoření do samotné smyčky jsou tedy β i γ fosfát obklopeny podobně těsně.

Skutečné důvody, proč γ-fosfát dostává víc kontaktů, jsou jiné:

**1. Má prostě víc volných kyslíků k dispozici** – jak jsme spočítali v kapitole 2.4: α-fosfát má 1 volný kyslík, β-fosfát má 1 volný kyslík, ale γ-fosfát má 2 volné kyslíky. Čistě statisticky má tedy víc "úchytných bodů" pro vodíkové vazby.

**2. Je "styčným bodem" pro víc různých strukturních elementů, ne jen pro samotný P-loop.** γ-fosfát je kontaktován i:
- **Switch I a Switch II regiony** (u GTPáz) – tyto struktury "čtou" právě přítomnost γ-fosfátu jako signál pro aktivní konformaci
- **Mg²⁺**, který koordinuje kyslíky obou fosfátů, ale u γ hraje extra roli v katalýze
- **Katalytickým glutamátem/glutaminem** (z Walker B nebo jiné části proteinu), který se orientuje směrem ke γ-fosfátu, protože právě tam probíhá nukleofilní atak při hydrolýze

γ-fosfát je tedy funkčně nejsledovanější a nejdůležitější část molekuly – právě tam se rozhoduje o katalýze a "čte se" stav ATP vs. ADP, proto do jeho okolí konverguje víc strukturních prvků z celého proteinu.

Pro úplnost – **α-fosfát** má naopak nejméně kontaktů s P-loop ze všech tří, protože je nejblíž ribóze a je fixován spíš vazbou na cukr než samotnou smyčkou.

### 3.4 Typické vzdálenosti vazeb

| Typ vazby | Vzdálenost | Poznámka |
|---|---|---|
| Vodíková vazba (backbone NH i Lys s β,γ-fosfátem) | ~2.7–3.0 Å | Flexibilnější co do úhlu i vzdálenosti |
| Koordinační vazba Mg²⁺ (s O, Ser/Thr-OH, vodou) | ~2.0–2.2 Å | Kratší, silnější, geometricky přísnější (musí zapadat do oktaedru) |

### 3.5 Schéma mechanismu vazby

*Viz přiložené schéma: `atp_ploop_mechanism_cz.svg`* – ukazuje β a γ fosfát zanořené v P-loop backbone smyčce, bidentátní kontakt lysinu na γ-fosfát, a koordinační sféru Mg²⁺ (β,γ-kyslíky, Ser/Thr-OH, dvě molekuly vody).

### 3.6 Musí být kontakt vždy přítomen?

Ano, v zásadě jde o definiční vlastnost funkční P-loop vazby – pokud fosfátový ocas ATP nekontaktuje smyčku, nejde o smysluplnou P-loop interakci v tom mechanistickém smyslu, o kterém mluvíme. Nicméně:

- **Apo stav** (bez navázaného ATP) je legitimní stav proteinu – P-loop bývá bez ligandu konformačně flexibilnější/otevřenější
- **Mutace klíčových reziduí** (Lys, glyciny) mohou stále umožnit fyzickou přítomnost ATP v kapse, ale s výrazně nižší afinitou a bez schopnosti efektivní katalýzy/konformačního přepnutí – tedy bez plně "funkčního" kontaktu
- V krystalových strukturách se občas objevují **neproduktivní/alternativní vazebné módy** (např. artefakty krystalizace), které nereprezentují fyziologicky relevantní stav

---

## 4. Role Mg²⁺

Mg²⁺ je nezbytný kofaktor pro funkci P-loop proteinů – v biochemii se proto téměř vždy mluví o komplexu **Mg-ATP**, ne o "holém" ATP.

### 4.1 Koordinační sféra

Mg²⁺ je typicky koordinován **oktaedricky** (6 vazeb):
- 1–2 kyslíky z β a γ fosfátu ATP
- 1 kyslík z OH skupiny Ser/Thr (P-loop)
- 2–3 molekuly vody

### 4.2 Proč je Mg²⁺ nutný – čtyři funkce

**1. Neutralizace náboje.** ATP má při fyziologickém pH náboj přibližně −4 (viz kapitola 2.4) – velmi hustě nahromaděný negativní náboj na malém prostoru. Bez kompenzace by to bylo elektrostaticky nevýhodné (fosfáty by se navzájem odpuzovaly). Mg²⁺ tento náboj částečně stíní a stabilizuje.

**2. Přemostění β a γ fosfátu.** Mg²⁺ typicky koordinuje současně kyslíky z obou fosfátů, funguje jako molekulární svorka, která drží fosfáty ve správné geometrii a zpevňuje afinitu komplexu.

**3. Role v katalýze.** Mg²⁺ polarizuje vazbu mezi β a γ fosfátem (tu, která se štěpí), čímž usnadňuje nukleofilní atak, a pomáhá stabilizovat přechodový stav hydrolýzy. Koordinovaná voda v jeho komplexu je často přímo tou molekulou, která slouží jako nukleofil.

**4. Proč zrovna Ser/Thr.** Krátký postranní řetězec s OH skupinou je dostatečně blízko fosfátům (díky poloze na konci Walker A motivu) pro přímou koordinaci Mg²⁺, aniž by narušil síť H-vazeb s lysinem a backbone.

Bez Mg²⁺: nižší afinita k ATP, výrazně pomalejší nebo žádná hydrolýza.

### 4.3 Co přesně je koordinace – chemický základ

"Koordinace" je termín z anorganické chemie. Normální kovalentní vazba vzniká tak, že oba atomy přispějí jedním elektronem do sdíleného páru. **Koordinační (dativní) vazba** je speciální případ, kdy **oba elektrony páru dodává jen jeden atom** (donor) a druhý (akceptor) poskytne jen prázdný orbital.

- **Mg²⁺** je akceptor (kation, má prázdné valenční orbitaly)
- **Kyslík** (z fosfátu, Ser/Thr, nebo vody) je donor – má volné elektronové páry

Chemicky je to podobné iontové interakci, ale s výrazným kovalentním/směrovým charakterem – proto "koordinační", ne prostě "iontová".

Geometrie je pro Mg²⁺ přísně definovaná – pravidelný **oktaedr** (6 vrcholů kolem centrálního iontu), na rozdíl třeba od Ca²⁺, který je flexibilnější.

### 4.4 Rozdíl oproti H-vazbě

- **H-vazba**: slabší, delší (~2.7–3.0 Å), méně směrově striktní
- **Koordinační vazba s Mg²⁺**: silnější, kratší (~2.0–2.2 Å), přísně geometricky definovaná

Proto je Mg²⁺ tak efektivní "svorka" – drží věci mnohem pevněji a přesněji na místě než pouhé vodíkové můstky.

---

## 5. Walker B motiv

Walker B motiv leží zhruba o 90–120 reziduí dál v sekvenci než P-loop, ale strukturně je mu blízko. Konsenzus: **hhhhD[E]** (h = hydrofobní zbytek).

- **Asp** – koordinuje Mg²⁺ (přímo nebo přes vodu)
- **Glu** – aktivuje (deprotonuje) katalytickou molekulu vody, čímž ji mění na silný nukleofil pro hydrolýzu

Walker B je tedy funkčním doplňkem P-loop – zatímco P-loop drží a orientuje fosfáty, Walker B zajišťuje katalytický aparát pro jejich štěpení.

---

## 6. Mechanismus hydrolýzy ATP

### 6.1 Co je hydrolýza obecně

Hydrolýza (hydro = voda, lysis = štěpení) je reakce, při které se molekula vody použije k rozštěpení kovalentní vazby:

```
R–X + H₂O → R–OH + H–X
```

U ATP se štěpí fosfoanhydridová vazba mezi β a γ fosfátem:

```
ATP + H₂O → ADP + Pi + energie
```

### 6.2 Mechanismus na atomární úrovni – nukleofilní substituce na fosforu

Jde o klasickou nukleofilní substituci (analogickou SN2 mechanismu na uhlíku, ale odehrávající se na fosforu):

1. **Aktivace vody**: Glu z Walker B (přes zprostředkující vodu v koordinační sféře Mg²⁺) odebere vodě proton → vzniká silně nukleofilní **hydroxidový ion (OH⁻)**
2. **Nukleofilní atak**: aktivovaný kyslík zaútočí na atom fosforu γ-fosfátu z opačné strany, než je vazba na β-fosfát (**in-line atak**)
3. **Přechodový stav**: vzniká krátkodobý **pentakoordinovaný** fosfor (trigonální bipyramida) s koncentrovaným negativním nábojem – stabilizovaný Mg²⁺ a P-loop (Lys, backbone NH)
4. **Rozpad vazby**: vazba mezi β a γ fosfátem praskne → vzniká ADP + Pi

Enzym neumožňuje hydrolýzu "z ničeho" – bez katalýzy probíhá extrémně pomalu (poločas rozpadu řádově roky). Enzym ji urychluje o **10⁶–10¹² krát** tím, že stabilizuje nestabilní přechodový stav.

### 6.3 Co jsou nukleofil, elektrofil a polarizace vazby

**Nukleofil** ("milovník jádra") je skupina s přebytkem elektronové hustoty (volný elektronový pár nebo záporný náboj), ochotná ho darovat do vznikající vazby. V podstatě je totéž co **donor elektronového páru** – jen v kontextu chemické reakce (dynamický děj), zatímco "donor" bývá spíše popis role ve stabilní, existující (koordinační) vazbě. Formálněji jde o konkrétní případ **Lewisovy báze**.

**Elektrofil** ("milovník elektronů") je opak – místo/atom s nedostatkem elektronové hustoty, které nukleofil napadá. V našem případě je elektrofilem atom **fosforu** v γ-fosfátu.

**Polarizace vazby**: pokud mají dva vázané atomy rozdílnou elektronegativitu, sdílený elektronový pár není rozložen rovnoměrně – posouvá se blíž k elektronegativnějšímu atomu, čímž vzniká dipól (δ+/δ−).

Vazba P–O je přirozeně polarizovaná (kyslík je elektronegativnější), fosfor je tedy mírně δ+ (elektrofilní) i bez zásahu Mg²⁺. Mg²⁺ ale tuto polarizaci **prohlubuje**: koordinací na kyslík "odčerpává" elektronovou hustotu směrem k sobě, kyslík si to kompenzuje přitažením elektronů z vazby s fosforem, fosfor je tak ještě víc ochuzen o elektrony → stává se ještě lepším cílem pro nukleofilní atak.

Enzym tedy zesiluje elektrostatický "spád" mezi nukleofilem (aktivovaná voda) a elektrofilem (fosfor) z obou stran zároveň – to výrazně urychluje reakci.

### 6.4 Co je Pi a proč je "anorganický"

**Pi** = zkratka pro *inorganic phosphate* (anorganický fosfát). Chemicky jde o volný fosfátový ion, při fyziologickém pH převážně ve formě **HPO₄²⁻** (dominantní) a **H₂PO₄⁻** (menší podíl) – poměr daný stejnou pH/pKa logikou jako v kapitole 2.5.

**Proč "anorganický":**
- **Organická sloučenina** typicky obsahuje vazbu uhlík–vodík (C–H) nebo je součástí uhlíkového skeletu
- **Anorganická sloučenina** takový skelet nemá

Pi je tvořen jen fosforem, kyslíkem a vodíkem – žádný uhlík. Dokud je γ-fosfát součástí ATP (navázaný přes ribózu, tedy přes organickou molekulu), mluví se o **organickém fosfátu** (esterifikovaný fosfát). Jakmile se hydrolýzou oddělí jako samostatná entita, ztrácí spojení s uhlíkovou strukturou a stává se volným **anorganickým** iontem – proto změna názvu.

Biologický význam tohoto rozlišení: volný, difuzibilní Pi se může vzdálit z vazebného místa a nezávisle se účastnit dalších reakcí (např. jako substrát pro syntézu ATP jinde v buňce) – což by nebylo možné, kdyby zůstal navázaný na organickou molekulu.

### 6.5 Odkud pochází uvolněná energie

Toto je místo, kde se často vyskytuje **mylná představa**: že energie je "uložená ve vazbě" a přetržením vazby se uvolní. To je **chemicky nesprávné**. Přetržení vazby vždy vyžaduje dodání energie (je to endotermní krok) – energie se neuvolňuje "z vazby", ale z **celkové bilance reakce**.

Produkty (ADP + Pi) jsou souhrnně energeticky výhodnější (stabilnější) než reaktanty (ATP + H₂O), a to díky součtu několika efektů:

**1. Uvolnění elektrostatické repulze.** Tři fosfáty s hustým záporným nábojem (ATP⁴⁻) se navzájem odpuzují, jako stlačená pružina. Oddělením γ-fosfátu se tento tlak uvolní.

**2. Lepší resonanční stabilizace produktů.** Volný Pi může svůj náboj delokalizovat symetricky mezi všechny 4 kyslíky; dokud je γ-fosfát součástí ATP, tato resonance je omezená.

**3. Lepší solvatace.** Dva menší, oddělené ionty (ADP + Pi) mají dohromady větší povrch vystavený vodě než jeden velký ATP ion – víc stabilizujících interakcí s vodou.

**4. Vyšší entropie.** Z jedné molekuly ATP + jedné molekuly vody vznikají dvě oddělené molekuly (ADP + Pi) – víc částic, vyšší neuspořádanost.

**ΔG°' ≈ −30.5 kJ/mol** (~−7.3 kcal/mol). "Vysokoenergetická fosfoanhydridová vazba" je tedy poněkud zavádějící termín – nejde o vlastnost jedné izolované vazby, ale o vlastnost celé reakce.

Klíčové pro biologii: tuto volnou energii proteiny **spřahují** s konformační změnou (viz kapitola 7), místo aby se jen rozptýlila jako teplo.

---

## 7. Konformační spínač – funkční důsledek vazby a hydrolýzy

Po navázání ATP dochází k několika krokům:

### 7.1 Uzavření smyčky

Navázání ATP vyvolá konformační změnu – P-loop se těsněji sevře kolem β,γ-fosfátů. U mnoha proteinů (např. GTPáz) to zahrnuje pohyb sousedních **Switch I** a **Switch II** regionů v blízkosti γ-fosfátu.

### 7.2 Princip molekulárního spínače

Přítomnost/nepřítomnost γ-fosfátu funguje jako spínač:
- **ATP/GTP navázáno** → "ON" konformace (switch regiony fixované H-vazbami na γ-fosfát)
- **Po hydrolýze (ADP/GDP)** → ztráta těchto vazeb → switch regiony se uvolní → "OFF" konformace

### 7.3 Funkční důsledky podle typu proteinu

**Motorové proteiny (myosin, kinesin).** Konformační změna po vazbě/hydrolýze ATP se translatuje na mechanický pohyb – "power stroke". Cyklus vazba–hydrolýza–uvolnění pohání opakovaný mechanický krok.

**Malé GTPázy (Ras, Rho, Rab).** Fungují jako molekulární "časovače" – v ON stavu (GTP) vážou a aktivují efektorové proteiny v signální dráze. Hydrolýza je vypínač. Rychlost hydrolýzy regulují další proteiny: **GAP** (GTPase-activating proteins) ji urychlují, **GEF** (guanine exchange factors) vyměňují GDP zpět za GTP.

**ABC transportéry.** Vazba ATP na dvě P-loop domény vede k jejich dimerizaci ("sandwich" mechanismus), což mechanicky přepne transmembránové domény a umožní transport substrátu. Hydrolýza dimér rozpojí.

**Kinázy.** Zde není cílem hydrolýza vodou, ale **přenos γ-fosfátu na substrát** (jiný protein, lipid, malou molekulu) – produktem je fosforylovaný substrát + ADP, nikoli Pi. Mechanismus je chemicky analogický (nukleofilní atak na fosfor), ale nukleofilem je OH/amin substrátu, ne voda.

### 7.4 Proč je hydrolýza (nebo přenos fosfátu) nutná pro tyto scénáře

Klíčová myšlenka: hydrolýza/přenos fosfátu je **"reset" krok**, který dělá z jednorázové vazebné události cyklický, opakovatelný proces.

- **Ras/malé GTPázy**: bez hydrolýzy by protein zůstal navždy v ON stavu, signální dráha by se nikdy nezastavila (podobně jako u onkogenních mutací Ras, kde je hydrolýza narušená)
- **Motorové proteiny**: bez hydrolýzy by proběhl jeden "power stroke" a protein by se zasekl – nemohl by se odpojit a pokračovat v dalším kroku
- **ABC transportéry**: bez hydrolýzy by transportér zůstal zaseklý v jedné konformaci, nemohl by provést další transportní cyklus

Bez hydrolýzy/přenosu fosfátu by tedy šlo o jednorázovou, nevratnou konformační změnu.

### 7.5 Uvolnění produktů

Po hydrolýze se typicky nejdřív uvolní **Pi** (ztráta vazeb na γ-fosfát destabilizuje "closed" konformaci), a teprve pak, často pomaleji, **ADP**. Tento krok bývá často rychlost-limitující pro celý cyklus.

---

## 8. Evoluční perspektiva – vztah k ancestrálním aminokyselinám

### 8.1 Konsenzuální raná abeceda 10 aminokyselin

Nezávislé linie důkazů (prebiotická chemie, expanze metabolických drah, biofyzikální optimalizace, ancestrální rekonstrukce sekvencí) se shodují na konsenzuální "rané" (prebioticky dostupné) abecedě 10 aminokyselin:

**Gly, Ala, Ser, Asp, Glu, Val, Leu, Ile, Pro, Thr** (jednopísmenné kódy: G, A, S, D, E, V, L, I, P, T)

Zbylých 10 "pozdních" aminokyselin (produkty pozdějších biosyntetických drah):

**Phe, Tyr, Arg, His, Trp, Asn, Gln, Lys, Cys, Met**

(Existuje i alternativní framework s ~13 aminokyselinami, který rozšiřuje základní desítku o další prebioticky dostupné zbytky pro funkčnější/stabilnější proteiny.)

### 8.2 Rané vs. pozdní rezidua v P-loop a Walker B

Z klíčových, konzervovaných pozic obou motivů patří mezi **rané**:
- oba **glyciny** i **Ser/Thr** z P-loop
- **Asp i Glu** z Walker B (koordinace Mg²⁺, aktivace katalytické vody)

Jediné **pozdní** reziduum mezi definičními pozicemi obou motivů je **Lysin** – jediný postranní řetězec P-loop, který dělá přímý specifický (nikoli jen backbone) kontakt s fosfáty.

Ty čtyři variabilní pozice v konsenzu (x-x-x-x) nejsou definičně vázány na konkrétní aminokyseliny, takže tam teoreticky mohou být i další pozdní AA – nejsou to ale konzervované, definiční znaky motivu.

### 8.3 Možný evoluční scénář

To, že jediné pozdní reziduum v celém aparátu je zrovna lysin – tedy jediný postranní řetězec s přímým specifickým kontaktem na fosfáty – naznačuje pravděpodobný evoluční scénář:

Nejranější prekurzory P-loop pravděpodobně fungovaly **bez lysinu**, s vázáním fosfátů zajištěným jen backbone NH skupinami a Mg²⁺/ranými kyselými zbytky (Asp/Glu z Walker B). Teprve když se lysin zapojil do genetického kódu, mohl motiv "vylepšit" o silnější, specifičtější úchyt γ-fosfátu, což mohlo zvýšit afinitu i katalytickou účinnost.

Je to hezký příklad toho, jak mohla vypadat postupná "modernizace" již existujícího funkčního motivu s postupně se rozšiřující abecedou aminokyselin.

---

## 9. Vazebná energetika

### 9.1 Experimentálně naměřené hodnoty afinity

Vazebná afinita ATP k P-loop proteinům se vyjadřuje jako disociační konstanta **Kd** (nebo Michaelisova konstanta Km u enzymů). Řádové rozmezí napříč rodinami:

- **Kinázy**: Km pro ATP typicky 10–100 µM
- **Adenylátkináza**: Kd v řádu desítek µM
- **Malé GTPázy (Ras a příbuzné)**: Kd v řádu pM–nM (biologicky nutné pro pomalou spontánní výměnu nukleotidu, řízenou GEF proteiny)
- **Motorové proteiny**: typicky mikromolární rozsah, silně závislé na konformačním stavu

### 9.2 Převod na volnou energii

```
ΔG = RT ln(Kd)
```

Pro Kd = 1 µM při 298 K vychází ΔG ≈ −34 kJ/mol. Pro velmi těsné vazby (Ras, pM rozsah) to může být přes −60 kJ/mol.

### 9.3 Proč je odhad z AutoDock Vina pro tento systém problematický

Pokud by někdo chtěl odhadnout vazebnou energii tohoto komplexu pomocí běžného dokovacího nástroje jako AutoDock Vina, je třeba počítat s několika zásadními problémy:

**1. Mg²⁺ koordinace.** Vina nemá explicitní termín pro koordinační vazby s kovy. Mg²⁺ se buď musí pevně fixovat předem (a nedokuje se), nebo se ignoruje – ale právě Mg²⁺ jsme identifikovali jako klíčový prvek stability celého komplexu. Bez něj skóre podhodnotí realitu.

**2. Silně nabitý ligand.** ATP⁴⁻ vyžaduje přesnou elektrostatiku a solvataci. Vina používá zjednodušené empirické náboje (Gasteigerovy náboje, žádná polarizace, žádné explicitní řešení solvatace typu Poisson-Boltzmann) – u takto nabitých systémů to vede k chybám řádově i několik kcal/mol.

**3. Chybějící explicitní voda.** Katalytická voda i strukturní vody v koordinační sféře Mg²⁺ jsou pro geometrii vazebného místa klíčové, Vina je ve výchozím nastavení nezahrnuje.

**4. Vina skóre není absolutní ΔG.** I v jednodušších případech koreluje spíš relativně (užitečné pro srovnání různých ligandů/pozic na stejném proteinu), ne jako absolutní termodynamická veličina – autoři sami doporučují používat skóre spíš pro ranking než pro kvantitativní predikci.

### 9.4 Přesnější alternativy

- **MM-GBSA/MM-PBSA** – post-processing z MD simulace, lepší zachycení elektrostatiky a solvatace (Mg²⁺ pořád zůstává obtížný)
- **FEP (free energy perturbation) / TI (thermodynamic integration)** – nejpřesnější, ale výpočetně náročné
- **QM/MM** – nutné, pokud je potřeba zachytit polarizaci P–O vazby a přenos náboje kolem Mg²⁺ přesně (viz kapitola 6.3)

---

## Přiložená schémata

- `atp_schema.svg` – struktura ATP s vyznačenými α/β/γ fosfáty a místem štěpení
- `atp_ploop_mechanism_cz.svg` – mechanismus vazby ATP do P-loop (backbone kontakty, Lys, Mg²⁺ koordinace)
