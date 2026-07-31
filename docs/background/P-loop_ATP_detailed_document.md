# P-loop and ATP Binding — Detailed Reference Document

> This is the extended version. For a quick overview, see *P-loop_ATP_binding_summary.md*, which serves as a TL;DR of this text.

---

## 1. Introduction – what is the P-loop

The P-loop (phosphate-binding loop), also called the **Walker A motif**, is one of the most widespread and evolutionarily oldest structural motifs found in nucleotide-binding proteins (ATP, GTP). It forms a loop between a β-sheet strand and an α-helix (a typical **βαβ fold**), and its main function is to wrap around and stabilize the phosphate group of the bound nucleotide.

### 1.1 Consensus sequence

The Walker A consensus is:

**G-x-x-x-x-G-K-[S/T]**

where x denotes any amino acid. Key elements:
- **Glycines** (two conserved positions) – provide the conformational flexibility needed for the loop to bend sharply around the phosphates
- **Lysine** – the only residue in the motif making direct, specific side-chain contact with the phosphates
- **Serine/threonine** – coordinates the magnesium cation (Mg²⁺)

### 1.2 Occurrence across protein families

The P-loop appears in a huge number of functionally unrelated families, for example:
- ATPases and GTPases (the Ras superfamily, myosin, kinesin)
- ABC transporters
- Kinases (both protein kinases and metabolic kinases)
- Helicases
- Translation elongation factors (EF-Tu, EF-G)

This ubiquity suggests it is one of the evolutionarily oldest and most conserved structural solutions for handling nucleotides – likely appearing very early in the evolution of enzymes.

### 1.3 Sequence consensus vs. structural loop – why the numbers differ

It's common to encounter a discrepancy in the reported length of the motif: **8 amino acids** (the strict sequence-based Walker A consensus) vs. **10–15 amino acids** (a length often quoted elsewhere).

The difference arises because these are two different ways of defining the motif:
- The **sequence consensus** (G-x-x-x-x-G-K-[S/T]) measures only the strictly defined "core" sequence captured by bioinformatic tools (regex-style pattern matching, PROSITE/Pfam profiles) – that's the 8 residues.
- The **structurally defined P-loop** additionally includes part of the preceding β-strand from which the loop emerges, and possibly a couple of residues after the lysine/serine that still contribute to wrapping the phosphates – giving 10–15 residues.

Both numbers are therefore "correct" – they just describe slightly different things: one is a purely sequence-based signature, the other is the entire structural element in 3D.

---

## 2. ATP structure – basic orientation

Before diving into the binding mechanism, it helps to be clear on the structure of ATP itself.

### 2.1 Building blocks

ATP (adenosine-5'-triphosphate) consists of three parts:
- **Adenine** – a nitrogenous base (purine)
- **Ribose** – a five-carbon sugar
- **Triphosphate chain** – three linked phosphate groups

### 2.2 Alpha, beta, gamma phosphates

The phosphates form a linear chain attached to the 5' carbon of the ribose:

```
Ribose — O — Pα — O — Pβ — O — Pγ — O⁻ (and additional O⁻)
```

- The **alpha (α)** phosphate is bonded directly to the ribose (closest to the sugar)
- The **beta (β)** phosphate is in the middle
- The **gamma (γ)** phosphate is terminal, farthest from the sugar

Between the phosphates are so-called **phosphoanhydride bonds** – these are the "high-energy" bonds whose cleavage is associated with the release of free energy (see section 6.4).

The beta and gamma phosphates together form the so-called **"tail"** of ATP – this is the part the P-loop wraps around, and it's the site cleaved during hydrolysis.

*See the attached diagram: `atp_schema_en.svg`*

### 2.3 Where cleavage occurs during hydrolysis

During hydrolysis of ATP to ADP + Pi, the bond **between the β and γ phosphate** is cleaved. The gamma phosphate leaves as free inorganic phosphate (Pi), while the rest of the molecule (adenine–ribose–α–β) forms ADP.

### 2.4 ATP's charge, and why it is −4

Each phosphate carries oxygens that can be either protonated (–OH, neutral) or deprotonated (–O⁻, negatively charged) – depending on the pH of the environment (phosphate groups are weak acids).

Number of "free" oxygens on each phosphate:
- **α-phosphate**: 1 free oxygen (the others are bonded to the ribose and the β-phosphate)
- **β-phosphate**: 1 free oxygen
- **γ-phosphate**: 2 free oxygens (not bonded to any further phosphate)

At physiological pH (~7.4), the pKa of these groups is lower than the ambient pH, so they are **almost entirely deprotonated**:

- α: −1
- β: −1
- γ: −2

**Total: −4** → hence ATP⁴⁻ is referred to as the dominant form inside the cell.

### 2.5 How pH works, and why it matters here

**pH = −log₁₀[H⁺]**, i.e., the negative base-10 logarithm of the molar concentration of hydrogen ions in solution. It is a logarithmic scale – a difference of 1 pH unit means a tenfold change in H⁺ concentration.

A phosphate group behaves as a weak acid, existing in solution in equilibrium:

```
R-OH ⇌ R-O⁻ + H⁺
```

This equilibrium is described by the **Henderson-Hasselbalch equation**:

```
pH = pKa + log([R-O⁻] / [R-OH])
```

- When **pH > pKa** → the deprotonated form (R-O⁻) dominates
- When **pH < pKa** → the protonated form (R-OH) dominates
- When **pH = pKa** → exactly 50:50

ATP's phosphate OH groups have pKa values ranging roughly from 1–2 (first deprotonation) to 6.5–7 (the last, most tightly held proton). Because physiological pH (7.4) is higher than all of these values, the equilibrium is strongly shifted toward the deprotonated form – for the last group (pKa ~7), at pH 7.4 the O⁻:OH ratio works out to roughly 2.5:1.

---

## 3. Molecular contacts between the P-loop and ATP

### 3.1 Complete contact overview

| Part of ATP | Interacting group/residue | Type of contact |
|---|---|---|
| γ,β-phosphate | P-loop backbone NH | Hydrogen bonds |
| γ,β-phosphate | Conserved Lys (ε-NH₃⁺) | Salt bridge / H-bonds (bidentate) |
| Mg²⁺ | Ser/Thr (P-loop) | Coordination bond |
| Mg²⁺ | Asp (Walker B) + waters | Coordination bond |
| γ-phosphate (catalysis) | Glu (Walker B) via water | Nucleophile activation |
| Adenine | Aromatic residues elsewhere in the protein | π-stacking |
| Ribose | Asp/Glu, backbone | Hydrogen bonds |

### 3.2 Why contact is provided mainly by the backbone, not glycine side chains

Glycines in the P-loop **have no side chain** (just a hydrogen atom), so their role cannot be direct chemical interaction with ATP via a side chain – that isn't even possible. Their role is purely **conformational**: they allow the loop to bend into the tight arc that would not be sterically possible with bulkier side chains.

This does not mean glycines are excluded from contact altogether. On the contrary – they contact ATP via their **backbone amide NH groups**, the part of the molecule shared by every amino acid (not just glycine). The key question, then, is not "who makes contact" but "why must it specifically be glycine, rather than, say, leucine, when every amino acid has a backbone NH":

- **Every amino acid has a backbone NH** – in principle, any of them could form the same hydrogen bond
- **But a bulky side chain** (e.g., leucine's) would sterically prevent the loop from bending into the sharp angle the P-loop requires

Glycine is therefore necessary for conformational flexibility, not because of any unique chemistry of its side chain (since it has none).

The only side chain in the entire motif making direct, specific chemical contact with the phosphates is the **lysine side chain** (the ε-NH₃⁺ group).

### 3.3 Why the gamma phosphate gets the most contacts

It might seem intuitive that the gamma phosphate has more contacts because it is "buried deeper" in the P-loop. In reality, the P-loop does not form a tunnel that ATP enters "tail-first" – it's more of a shallow cradle over which the entire phosphate chain lies side by side, roughly in one plane. In terms of depth of burial within the loop itself, the β and γ phosphates are surrounded about equally tightly.

The actual reasons the γ-phosphate gets more contacts are different:

**1. It simply has more free oxygens available.** As calculated in section 2.4: the α-phosphate has 1 free oxygen, the β-phosphate has 1 free oxygen, but the γ-phosphate has 2 free oxygens. Purely statistically, it has more "anchor points" for hydrogen bonds.

**2. It is a "hub" for several structural elements, not just the P-loop.** The γ-phosphate is also contacted by:
- **Switch I and Switch II regions** (in GTPases) – these structures "read" the presence of the γ-phosphate as a signal for the active conformation
- **Mg²⁺**, which coordinates oxygens from both phosphates, but plays an extra role in catalysis at the γ position
- The **catalytic glutamate/glutamine** (from Walker B or elsewhere in the protein), which orients toward the γ-phosphate, since that's exactly where the nucleophilic attack occurs during hydrolysis

The γ-phosphate is thus the functionally most "watched" and important part of the molecule – it is precisely where catalysis is decided and where the ATP vs. ADP state is "read", so more structural elements from across the protein converge on it.

For completeness – the **α-phosphate** has the fewest contacts with the P-loop of the three, since it is closest to the ribose and is fixed more by its bond to the sugar than by the loop itself.

### 3.4 Typical bond distances

| Bond type | Distance | Note |
|---|---|---|
| Hydrogen bond (backbone NH and Lys to the β,γ-phosphate) | ~2.7–3.0 Å | More flexible in both angle and distance |
| Mg²⁺ coordination bond (to O, Ser/Thr-OH, water) | ~2.0–2.2 Å | Shorter, stronger, geometrically stricter (must fit an octahedron) |

### 3.5 Binding mechanism diagram

*See the attached diagram: `atp_ploop_mechanism_en.svg`* – shows the β and γ phosphates buried in the P-loop backbone, the bidentate lysine contact on the γ-phosphate, and the Mg²⁺ coordination sphere (β,γ-oxygens, Ser/Thr-OH, two water molecules).

### 3.6 Must the contact always be present?

Yes, in principle this is a defining property of a functional P-loop interaction – if the phosphate tail of ATP doesn't contact the loop, it isn't a meaningful P-loop interaction in the mechanistic sense discussed here. However:

- The **apo state** (without bound ATP) is a legitimate state of the protein – the P-loop tends to be conformationally more flexible/open without a ligand
- **Mutations of key residues** (Lys, glycines) may still allow the physical presence of ATP in the pocket, but with substantially reduced affinity and without the capacity for efficient catalysis/conformational switching – i.e., without a fully "functional" contact
- Crystal structures occasionally show **non-productive/alternative binding modes** (e.g., crystallization artifacts) that do not represent a physiologically relevant state

---

## 4. The role of Mg²⁺

Mg²⁺ is an essential cofactor for P-loop protein function – which is why biochemistry almost always refers to the **Mg-ATP** complex rather than "bare" ATP.

### 4.1 Coordination sphere

Mg²⁺ is typically coordinated **octahedrally** (6 bonds):
- 1–2 oxygens from the β and γ phosphate of ATP
- 1 oxygen from the OH group of the P-loop Ser/Thr
- 2–3 water molecules

### 4.2 Why Mg²⁺ is necessary – four functions

**1. Charge neutralization.** At physiological pH, ATP carries a charge of roughly −4 (see section 2.4) – a very dense negative charge concentrated in a small space. Without compensation, this would be electrostatically unfavorable (the phosphates would repel one another). Mg²⁺ partially shields and stabilizes this charge.

**2. Bridging the β and γ phosphate.** Mg²⁺ typically coordinates oxygens from both phosphates simultaneously, acting as a molecular clamp that holds the phosphates in the correct geometry and strengthens the affinity of the complex.

**3. Role in catalysis.** Mg²⁺ polarizes the bond between the β and γ phosphate (the one that gets cleaved), facilitating nucleophilic attack, and helps stabilize the transition state of hydrolysis. The water coordinated in its complex is often directly the molecule that serves as the nucleophile.

**4. Why specifically Ser/Thr.** The short side chain with an OH group is close enough to the phosphates (due to its position at the end of the Walker A motif) for direct Mg²⁺ coordination, without disrupting the network of H-bonds with the lysine and backbone.

Without Mg²⁺: lower affinity for ATP, markedly slower or no hydrolysis.

### 4.3 What exactly coordination is – the chemical basis

"Coordination" is a term from inorganic chemistry. A normal covalent bond forms when both atoms each contribute one electron to a shared pair. A **coordination (dative) bond** is a special case where **both electrons of the pair are supplied by a single atom** (the donor), while the other atom (the acceptor) contributes only an empty orbital.

- **Mg²⁺** is the acceptor (a cation, with empty valence orbitals)
- **Oxygen** (from the phosphate, Ser/Thr, or water) is the donor – it has lone electron pairs

Chemically this resembles an ionic interaction, but with a pronounced covalent/directional character – hence "coordination" rather than simply "ionic."

The geometry is strictly defined for Mg²⁺ – a regular **octahedron** (6 vertices around the central ion), unlike, for instance, Ca²⁺, which is more flexible.

### 4.4 Difference from a hydrogen bond

- **Hydrogen bond**: weaker, longer (~2.7–3.0 Å), less directionally strict
- **Mg²⁺ coordination bond**: stronger, shorter (~2.0–2.2 Å), strictly geometrically defined

This is why Mg²⁺ is such an effective "clamp" – it holds things much more firmly and precisely in place than mere hydrogen bonds.

---

## 5. Walker B motif

The Walker B motif sits roughly 90–120 residues further along the sequence than the P-loop, but is structurally close to it. Consensus: **hhhhD[E]** (h = hydrophobic residue).

- **Asp** – coordinates Mg²⁺ (directly or via water)
- **Glu** – activates (deprotonates) the catalytic water molecule, turning it into a strong nucleophile for hydrolysis

Walker B is thus the functional complement to the P-loop – while the P-loop holds and orients the phosphates, Walker B provides the catalytic machinery for cleaving them.

---

## 6. Mechanism of ATP hydrolysis

### 6.1 What hydrolysis is in general

Hydrolysis (hydro = water, lysis = cleavage) is a reaction in which a water molecule is used to break a covalent bond:

```
R–X + H₂O → R–OH + H–X
```

In ATP, the phosphoanhydride bond between the β and γ phosphate is cleaved:

```
ATP + H₂O → ADP + Pi + energy
```

### 6.2 The atomic-level mechanism – nucleophilic substitution at phosphorus

This is a classic nucleophilic substitution (analogous to the SN2 mechanism at carbon, but occurring at phosphorus):

1. **Water activation**: Glu from Walker B (via an intervening water in the Mg²⁺ coordination sphere) removes a proton from water → generating a strongly nucleophilic **hydroxide ion (OH⁻)**
2. **Nucleophilic attack**: the activated oxygen attacks the phosphorus atom of the γ-phosphate from the side opposite the bond to the β-phosphate (**in-line attack**)
3. **Transition state**: a short-lived **pentacoordinate** phosphorus forms (a trigonal bipyramid) carrying concentrated negative charge – stabilized by Mg²⁺ and the P-loop (Lys, backbone NH)
4. **Bond cleavage**: the bond between the β and γ phosphate breaks → yielding ADP + Pi

The enzyme does not enable hydrolysis "out of nothing" – without catalysis it proceeds extremely slowly (half-life on the order of years). The enzyme accelerates it by **10⁶–10¹²-fold** by stabilizing the unstable transition state.

### 6.3 Nucleophile, electrophile, and bond polarization

A **nucleophile** ("nucleus lover") is a group with excess electron density (a lone electron pair or a negative charge) that is willing to donate it into a forming bond. It is essentially the same as a **donor of an electron pair** – just used in the context of a chemical reaction (a dynamic event), whereas "donor" tends to describe a role within a stable, existing (coordination) bond. More formally, it is a specific instance of a **Lewis base**.

An **electrophile** ("electron lover") is the opposite – a site/atom with a deficit of electron density that a nucleophile attacks. In our case, the electrophile is the **phosphorus** atom of the γ-phosphate.

**Bond polarization**: when two bonded atoms differ in electronegativity, the shared electron pair is not distributed evenly – it shifts toward the more electronegative atom, creating a dipole (δ+/δ−).

The P–O bond is inherently polarized (oxygen is more electronegative), so phosphorus is already mildly δ+ (electrophilic) even without Mg²⁺. Mg²⁺, however, **deepens** this polarization: by coordinating the oxygen, it "pulls" electron density toward itself; the oxygen compensates by drawing electrons from its bond with phosphorus, which becomes even more electron-poor → an even better target for nucleophilic attack.

The enzyme thus strengthens the electrostatic "gradient" between the nucleophile (activated water) and the electrophile (phosphorus) from both sides at once – substantially accelerating the reaction.

### 6.4 What Pi is, and why it is "inorganic"

**Pi** = abbreviation for *inorganic phosphate*. Chemically, it is a free phosphate ion, at physiological pH existing mainly as **HPO₄²⁻** (dominant) and **H₂PO₄⁻** (minor fraction) – the ratio governed by the same pH/pKa logic as in section 2.5.

**Why "inorganic":**
- An **organic compound** typically contains a carbon–hydrogen (C–H) bond or is part of a carbon skeleton
- An **inorganic compound** has no such skeleton

Pi consists only of phosphorus, oxygen, and hydrogen – no carbon. As long as the γ-phosphate is part of ATP (bonded via the ribose, i.e., via an organic molecule), it is referred to as an **organic phosphate** (an esterified phosphate). Once hydrolysis separates it as a standalone entity, it loses its connection to any carbon structure and becomes a free **inorganic** ion – hence the change in name.

The biological significance of this distinction: a free, diffusible Pi can move away from the binding site and independently participate in other reactions (e.g., as a substrate for ATP synthesis elsewhere in the cell) – which would not be possible if it remained bound to an organic molecule.

### 6.5 Where the released energy comes from

This is a point where a **common misconception** arises: that energy is "stored in the bond" and released when the bond breaks. This is **chemically incorrect**. Breaking a bond always requires an input of energy (it is an endothermic step) – energy is not released "from the bond," but from the **overall balance of the reaction**.

The products (ADP + Pi) are collectively more energetically favorable (more stable) than the reactants (ATP + H₂O), due to the sum of several effects:

**1. Release of electrostatic repulsion.** The three densely negatively charged phosphates (ATP⁴⁻) repel one another, like a compressed spring. Separating the γ-phosphate releases this tension.

**2. Better resonance stabilization of the products.** Free Pi can delocalize its charge symmetrically across all 4 oxygens; while the γ-phosphate is still part of ATP, this resonance is limited.

**3. Better solvation.** Two smaller, separate ions (ADP + Pi) together present a larger surface area to water than one large ATP ion – more stabilizing interactions with water.

**4. Higher entropy.** From one ATP molecule + one water molecule, two separate molecules (ADP + Pi) are produced – more particles, higher disorder.

**ΔG°' ≈ −30.5 kJ/mol** (~−7.3 kcal/mol). "High-energy phosphoanhydride bond" is therefore a somewhat misleading term – it is not a property of a single isolated bond, but a property of the entire reaction.

Crucially for biology: proteins **couple** this free energy to a conformational change (see section 7), rather than simply dissipating it as heat.

---

## 7. Conformational switch – functional consequence of binding and hydrolysis

Several steps follow ATP binding:

### 7.1 Closing of the loop

ATP binding triggers a conformational change – the P-loop tightens around the β,γ-phosphates. In many proteins (e.g., GTPases), this involves movement of the neighboring **Switch I** and **Switch II** regions near the γ-phosphate.

### 7.2 Principle of the molecular switch

The presence/absence of the γ-phosphate acts as a switch:
- **ATP/GTP bound** → "ON" conformation (switch regions fixed by H-bonds to the γ-phosphate)
- **After hydrolysis (ADP/GDP)** → loss of these bonds → switch regions relax → "OFF" conformation

### 7.3 Functional consequences by protein type

**Motor proteins (myosin, kinesin).** The conformational change following ATP binding/hydrolysis translates into mechanical movement – the "power stroke." The bind–hydrolyze–release cycle drives a repeated mechanical step.

**Small GTPases (Ras, Rho, Rab).** These act as molecular "timers" – in the ON state (GTP), they bind and activate effector proteins downstream in a signaling pathway. Hydrolysis is the switch-off. The rate of hydrolysis is regulated by other proteins: **GAPs** (GTPase-activating proteins) accelerate it, **GEFs** (guanine exchange factors) exchange GDP back for GTP.

**ABC transporters.** ATP binding to two P-loop domains drives their dimerization (a "sandwich" mechanism), which mechanically flips the transmembrane domains and enables substrate transport. Hydrolysis dissociates the dimer.

**Kinases.** Here the goal is not hydrolysis by water, but **transfer of the γ-phosphate to a substrate** (another protein, a lipid, a small molecule) – the product is a phosphorylated substrate + ADP, not Pi. The mechanism is chemically analogous (nucleophilic attack on phosphorus), but the nucleophile is the substrate's OH/amine group, not water.

### 7.4 Why hydrolysis (or phosphate transfer) is necessary for these scenarios

The key idea: hydrolysis/phosphate transfer is a **"reset" step** that turns a one-off binding event into a cyclical, repeatable process.

- **Ras/small GTPases**: without hydrolysis, the protein would stay permanently ON, and the signaling pathway would never switch off (similar to oncogenic Ras mutations, where hydrolysis is impaired)
- **Motor proteins**: without hydrolysis, a single "power stroke" would occur and the protein would get stuck – unable to detach and proceed to the next step
- **ABC transporters**: without hydrolysis, the transporter would remain stuck in one conformation, unable to perform another transport cycle

Without hydrolysis/phosphate transfer, the process would amount to a one-off, irreversible conformational change.

### 7.5 Product release

After hydrolysis, **Pi** is typically released first (loss of contacts to the γ-phosphate destabilizes the "closed" conformation), and then, often more slowly, **ADP**. This step is frequently rate-limiting for the entire cycle.

---

## 8. Evolutionary perspective – relationship to ancestral amino acids

### 8.1 Consensus early alphabet of 10 amino acids

Independent lines of evidence (prebiotic chemistry, expansion of metabolic pathways, biophysical optimization, ancestral sequence reconstruction) converge on a consensus "early" (prebiotically available) alphabet of 10 amino acids:

**Gly, Ala, Ser, Asp, Glu, Val, Leu, Ile, Pro, Thr** (one-letter codes: G, A, S, D, E, V, L, I, P, T)

The remaining 10 "late" amino acids (products of later biosynthetic pathways):

**Phe, Tyr, Arg, His, Trp, Asn, Gln, Lys, Cys, Met**

(An alternative framework with ~13 amino acids also exists, extending the base ten with further prebiotically available residues for more functional/stable proteins.)

### 8.2 Early vs. late residues in the P-loop and Walker B

Among the key, conserved positions of both motifs, the following belong to the **early** set:
- both **glycines** and **Ser/Thr** from the P-loop
- both **Asp and Glu** from Walker B (Mg²⁺ coordination, activation of the catalytic water)

The only **late** residue among the defining positions of both motifs is **lysine** – the sole P-loop side chain that makes direct, specific (rather than merely backbone-mediated) contact with the phosphates.

The four variable positions in the consensus (x-x-x-x) are not tied by definition to any particular amino acid, so late amino acids could theoretically appear there too – but they are not conserved, defining features of the motif.

### 8.3 A possible evolutionary scenario

The fact that the only late residue in the entire apparatus happens to be lysine – the sole side chain making direct, specific contact with the phosphates – suggests a plausible evolutionary scenario:

The earliest P-loop precursors likely functioned **without lysine**, with phosphate binding provided solely by backbone NH groups and Mg²⁺/early acidic residues (Asp/Glu from Walker B). Only once lysine became available in the genetic code could the motif be "upgraded" with a stronger, more specific grip on the γ-phosphate, potentially increasing both affinity and catalytic efficiency.

This is a nice example of what the gradual "modernization" of an already-functional motif might have looked like, as the amino acid alphabet progressively expanded.

---

## 9. Binding energetics

### 9.1 Experimentally measured affinity values

The binding affinity of ATP to P-loop proteins is expressed as a dissociation constant **Kd** (or the Michaelis constant Km, for enzymes). The order-of-magnitude range across families:

- **Kinases**: Km for ATP typically 10–100 µM
- **Adenylate kinase**: Kd on the order of tens of µM
- **Small GTPases (Ras and relatives)**: Kd on the order of pM–nM (biologically necessary for slow spontaneous nucleotide exchange, controlled by GEF proteins)
- **Motor proteins**: typically micromolar range, strongly dependent on conformational state

### 9.2 Conversion to free energy

```
ΔG = RT ln(Kd)
```

For a Kd of 1 µM at 298 K, ΔG ≈ −34 kJ/mol. For very tight binders (Ras, pM range), it can exceed −60 kJ/mol.

### 9.3 Why an AutoDock Vina estimate is problematic for this system

If someone wanted to estimate the binding energy of this complex using a standard docking tool like AutoDock Vina, several fundamental problems would need to be considered:

**1. Mg²⁺ coordination.** Vina has no explicit term for coordination bonds with metals. Mg²⁺ must either be rigidly fixed in advance (and not docked) or ignored – but Mg²⁺ has been identified as a key element of the complex's stability. Without it, the score will underestimate reality.

**2. A highly charged ligand.** ATP⁴⁻ requires accurate electrostatics and solvation. Vina uses simplified empirical charges (Gasteiger charges, no polarization, no explicit Poisson-Boltzmann-type solvation) – for such charged systems, this leads to errors on the order of several kcal/mol or more.

**3. Missing explicit water.** Both the catalytic water and structural waters in the Mg²⁺ coordination sphere are critical to the binding-site geometry, and Vina does not include these by default.

**4. Vina score is not an absolute ΔG.** Even in simpler cases it correlates more with relative comparison (useful for ranking different ligands/poses on the same protein) than with an absolute thermodynamic quantity – the authors themselves recommend using the score more for ranking than for quantitative prediction.

### 9.4 More accurate alternatives

- **MM-GBSA/MM-PBSA** – post-processing of an MD simulation, better captures electrostatics and solvation (Mg²⁺ remains challenging)
- **FEP (free energy perturbation) / TI (thermodynamic integration)** – most accurate, but computationally demanding
- **QM/MM** – necessary if precise capture of P–O bond polarization and charge transfer around Mg²⁺ is required (see section 6.3)

---

## Attached diagrams

- `atp_schema_en.svg` – ATP structure with α/β/γ phosphates labeled and the cleavage site marked
- `atp_ploop_mechanism_en.svg` – mechanism of ATP binding into the P-loop (backbone contacts, Lys, Mg²⁺ coordination)
