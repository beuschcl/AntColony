# Terroir Simulator — Ecological Species Records v0.1

**Status:** Proposed design artifact
**Initial scenario:** Driftless-inspired meadow-to-woods edge
**Initial moment:** Warm, damp day in May after recent rain
**Scope:** Species-record contract plus first records and sprite briefs

## 1. Purpose

This document defines the ecological contract between research, simulation state, and presentation.

Each catalog record answers three different questions:

1. **Ecological facts:** What is known about the organism in the real world?
2. **Simulation representation:** Which facts matter to Terroir Simulator, and how are they modeled?
3. **Visual communication:** How should a sprite reveal modeled state without owning or changing it?

These concerns remain separate. A sprite never decides whether an organism grows, flowers, fruits, or disappears. It only displays state supplied by the simulation.

## 2. Architectural decisions

### 2.1 Catalog records are not organism instances

A species record is immutable reference data shared by every simulated instance of a taxon.

| Concept                | Example                        | Identity                         |
| ---------------------- | ------------------------------ | -------------------------------- |
| Species catalog record | Pennsylvania sedge             | Stable `SpeciesId`               |
| Simulated organism     | One sedge colony at a location | Stable organism/entity ID        |
| Visible structure      | One morel fruiting cluster     | Stable structure or event ID     |
| Observation/history    | “Cluster collapsed on day 19”  | Append-only event/observation ID |

Changing a display name or scientific synonym must not change the stable ID.

### 2.2 Records preserve uncertainty

Real ecology is not a collection of exact game thresholds. Every ecological claim therefore has:

* a source,
* a confidence level,
* a scope or geographic qualification,
* and an optional modeling note.

Unknown facts remain unknown. The simulator must not silently convert “unknown” into “false,” zero, or a guessed optimum.

### 2.3 Facts and model choices are labeled

Record values use one of these classifications:

| Classification      | Meaning                                          |
| ------------------- | ------------------------------------------------ |
| `observed_fact`     | Directly supported by a cited source             |
| `derived_fact`      | Reasonable synthesis of multiple cited facts     |
| `simulation_choice` | Intentional simplification or design decision    |
| `hypothesis`        | Plausible behavior retained for later validation |
| `unknown`           | Not established well enough to model             |

### 2.4 No destructive lifecycle

An organism that is dormant, dead, collapsed, or no longer rendered is not erased from history. Current-world indexes may exclude inactive structures for efficient lookup, but identity, state transitions, and observations remain queryable.

### 2.5 v0.1 uses response categories, not invented equations

The first implementation should use categorical suitability values:

* `unsuitable`
* `tolerated`
* `preferred`
* `unknown`

Numeric response curves and thresholds should be added only when the model has suitable evidence and a testable reason to need them.

## 3. Reusable species-record template

The template applies to plants, fungi, and later other organism groups. Fields marked **required** must exist even when their value is `unknown`.

### 3.1 Identity and provenance

| Field             | Required | Description                                                           |
| ----------------- | -------: | --------------------------------------------------------------------- |
| `species_id`      |      Yes | Stable, non-taxonomic catalog key, such as `flora.pennsylvania_sedge` |
| `record_version`  |      Yes | Version of this catalog record                                        |
| `record_status`   |      Yes | `draft`, `verified`, `deprecated`, or `superseded`                    |
| `kingdom`         |      Yes | Broad organism group                                                  |
| `scientific_name` |      Yes | Accepted name or intentionally broad taxon                            |
| `taxon_rank`      |      Yes | `species`, `genus`, `species_complex`, etc.                           |
| `common_names`    |      Yes | Preferred and alternate display names                                 |
| `regional_scope`  |      Yes | Geography for which the record has been evaluated                     |
| `native_status`   |      Yes | `native`, `introduced`, `uncertain`, or `not_applicable`              |
| `taxonomic_notes` |       No | Synonyms, ambiguity, or reasons for broad identification              |
| `sources`         |      Yes | Source IDs with title, organization, URL, access date, and use        |

### 3.2 Ecological facts

| Field                      | Required | Description                                                          |
| -------------------------- | -------: | -------------------------------------------------------------------- |
| `life_form`                |      Yes | Perennial sedge, rhizomatous forb, ascomycete fungus, etc.           |
| `mature_height`            |      Yes | Sourced range with unit; may be `not_applicable`                     |
| `vertical_layer`           |      Yes | `ground`, `low`, `mid`, `tall`, `canopy`, or `subsurface`            |
| `growth_form`              |      Yes | Tuft, clump, colony, mycelial network, fruiting cluster, etc.        |
| `longevity`                |      Yes | Annual/perennial/persistent network/unknown                          |
| `seasonal_timing`          |      Yes | Emergence, bloom, fruiting, persistence, dormancy                    |
| `light_response`           |      Yes | Sourced descriptive range                                            |
| `moisture_response`        |      Yes | Sourced descriptive range                                            |
| `drainage_response`        |      Yes | Sourced descriptive range                                            |
| `soil_or_substrate`        |      Yes | Soil texture, organic matter, litter, wood/root relationship         |
| `habitat_affinity`         |      Yes | Woodland floor, margin, rocky slope, decay pocket, etc.              |
| `spread_or_reproduction`   |      Yes | Rhizomes, seed, spores, clonal spread, unknown                       |
| `ecological_relationships` |      Yes | Hosts, associates, consumers, decomposer role, pollinators           |
| `disturbance_response`     |       No | Known responses to fire, tree death, trampling, canopy opening, etc. |
| `ecological_uncertainties` |      Yes | Important gaps or contested claims                                   |

### 3.3 Simulation representation

| Field                         | Required | Description                                                            |
| ----------------------------- | -------: | ---------------------------------------------------------------------- |
| `simulation_role`             |      Yes | Ground cover, flowering plant, fungal network, food source, etc.       |
| `modeled_entity`              |      Yes | What receives a stable world identity                                  |
| `modeled_structures`          |      Yes | Optional visible/temporary structures owned by or linked to the entity |
| `required_environment_inputs` |      Yes | Existing world values read by the organism logic                       |
| `optional_environment_inputs` |      Yes | Inputs deferred until supported                                        |
| `suitability_profile`         |      Yes | Categorical response to the required inputs                            |
| `lifecycle_states`            |      Yes | Domain states, not sprite filenames                                    |
| `state_transitions`           |      Yes | Conditions and events that may change state                            |
| `spatial_behavior`            |      Yes | Footprint, colony spread, coordinate lookup behavior                   |
| `resource_behavior`           |      Yes | Produced, stored, exposed, depleted, or no resource                    |
| `history_events`              |      Yes | State changes that must remain queryable                               |
| `v0_1_simplifications`        |      Yes | Explicit departures from ecological completeness                       |
| `deferred_questions`          |      Yes | Decisions intentionally postponed                                      |

### 3.4 Visual contract and sprite brief

| Field                         | Required | Description                                              |
| ----------------------------- | -------: | -------------------------------------------------------- |
| `logical_footprint`           |      Yes | Simulation cells occupied                                |
| `visual_footprint`            |      Yes | Permitted visible extension beyond the logical footprint |
| `view`                        |      Yes | Slightly elevated top-down                               |
| `base_tile`                   |      Yes | 32×32 logical pixels                                     |
| `silhouette_keys`             |      Yes | Features required for recognition                        |
| `palette_notes`               |      Yes | Local colors under the approved meadow lighting          |
| `sprite_states`               |      Yes | Visual variants mapped to domain states                  |
| `readability_priority`        |      Yes | Details that must survive at normal zoom                 |
| `decorative_detail`           |      Yes | Details allowed only when they do not mimic resources    |
| `animation_notes`             |      Yes | Optional motion; `none` is valid                         |
| `occlusion_rules`             |      Yes | What may overlap and what must remain selectable         |
| `prohibited_visual_inference` |      Yes | State that artwork must never invent                     |
| `sprite_open_questions`       |      Yes | Art questions reserved for test sprites                  |

### 3.5 Record acceptance checklist

A record is ready for implementation only when:

* [ ] It has a stable `SpeciesId`.
* [ ] Regional occurrence or native status has been checked.
* [ ] Every ecological input has a cited source or is labeled unknown.
* [ ] Ecological facts and simulation choices are visibly distinct.
* [ ] Uncertainty is preserved.
* [ ] Lifecycle states are domain concepts rather than image names.
* [ ] Historical transitions are identified.
* [ ] Logical and visual footprints are separate.
* [ ] Every sprite state maps to a modeled state.
* [ ] No sprite rule changes simulation behavior.

---

## 4. Record: Pennsylvania sedge

### 4.1 Identity

| Field             | Value                                                                                                                                   |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `species_id`      | `flora.pennsylvania_sedge`                                                                                                              |
| `record_version`  | `0.1.0`                                                                                                                                 |
| `record_status`   | `draft`                                                                                                                                 |
| `kingdom`         | Plantae                                                                                                                                 |
| `scientific_name` | *Carex pensylvanica* Lam.                                                                                                               |
| `taxon_rank`      | species                                                                                                                                 |
| `common_names`    | Pennsylvania sedge; oak sedge                                                                                                           |
| `regional_scope`  | Wisconsin Driftless-inspired dry-to-mesic woodland opening and margin                                                                   |
| `native_status`   | native                                                                                                                                  |
| `taxonomic_notes` | The simulator should use the scientific name for catalog identity display, but the stable ID must survive future nomenclatural changes. |

### 4.2 Ecological facts

| Attribute                | Value                                                                                               | Classification              |
| ------------------------ | --------------------------------------------------------------------------------------------------- | --------------------------- |
| Life form                | Rhizomatous perennial sedge                                                                         | `observed_fact`             |
| Mature height            | Foliage about 4–6 in; flowering stems up to 12 in                                                   | `observed_fact`             |
| Vertical layer           | Ground layer                                                                                        | `derived_fact`              |
| Growth form              | Soft, low clumps that spread by rhizomes and can form ground cover                                  | `observed_fact`             |
| Seasonal timing          | Greens early; small flowers generally appear in April to early May                                  | `observed_fact`             |
| Light                    | Full shade through open woodland; sun is tolerated when moisture is sufficient                      | `observed_fact`             |
| Moisture                 | Dry to average soil; wet soil is a poor fit                                                         | `observed_fact`             |
| Drainage                 | Well-drained preferred; persistent saturation unsuitable                                            | `derived_fact`              |
| Soil/substrate           | Average woodland soil; can tolerate dry acidic or sandy soil                                        | `observed_fact`             |
| Habitat                  | Open woods, woodland margins, and oak-associated woodland floor                                     | `observed_fact`             |
| Spread                   | Vegetative expansion by rhizomes; seed behavior is deferred                                         | `observed_fact`             |
| Regional occurrence      | Reported throughout Wisconsin by UW Arboretum                                                       | `observed_fact`             |
| Ecological relationships | Often interspersed with early spring woodland flowers; detailed fauna relationships not yet modeled | `observed_fact` / `unknown` |

**Uncertainty:** Horticultural performance is not identical to wild population behavior. The record supports broad habitat suitability, not a claim that every Wisconsin population has the same optimum.

### 4.3 Simulation representation

| Field                | v0.1 decision                                                                   | Classification      |
| -------------------- | ------------------------------------------------------------------------------- | ------------------- |
| `simulation_role`    | Living woodland-floor matrix and low competition layer                          | `simulation_choice` |
| `modeled_entity`     | A persistent sedge colony with stable identity                                  | `simulation_choice` |
| `modeled_structures` | Optional flowering culms linked to the colony                                   | `simulation_choice` |
| Required inputs      | Canopy light, soil moisture, drainage                                           | `simulation_choice` |
| Optional inputs      | Soil texture/acidity, temperature, competition, litter depth                    | `simulation_choice` |
| Preferred            | Partial/intermediate shade; dry-to-medium, well-drained soil                    | `derived_fact`      |
| Tolerated            | Deep shade; brighter sites when moisture is adequate                            | `derived_fact`      |
| Unsuitable           | Persistently wet/saturated soil                                                 | `derived_fact`      |
| Logical footprint    | One occupied cell per colony node; adjacent nodes may share one colony identity | `simulation_choice` |
| Spread               | Slow adjacent-cell rhizome expansion when established and locally suitable      | `simulation_choice` |
| Resource behavior    | No food resource in the initial slice                                           | `simulation_choice` |

#### Lifecycle states

```text
dormant
  → emerging
  → vegetative
  → flowering
  → vegetative_late
  → senescent
  → dormant
```

Flowering is optional within a yearly cycle. Severe stress may move an active colony to `stressed`; local shoots may become `absent_aboveground` without deleting the colony or its history.

#### Required history events

* Colony established
* New colony node produced
* Seasonal emergence
* Flowering started and ended
* Stress entered and recovered
* Aboveground shoots became absent
* Colony became locally inactive

#### v0.1 simplifications

* Rhizome spread uses adjacent grid cells rather than continuous underground geometry.
* Flowering is a state indicator, not a full reproductive model.
* Seeds, genetics, pollination, and herbivory are deferred.
* Suitability uses categories rather than numeric response curves.

### 4.4 Sprite brief

| Property             | Direction                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------ |
| Logical footprint    | 1 cell                                                                                                       |
| Visual footprint     | Primarily within 32×32; fine blade tips may extend 3–5 px into neighboring cells                             |
| Scale target         | Low but visually substantial enough to create a lush floor beneath bellwort and the ant                      |
| Silhouette keys      | Several loose tufts; narrow arching blades; irregular natural edge; never a lawn-like square                 |
| Palette              | Fresh yellow-green highlights, mid woodland green, cool teal shadow; flowering culms muted tan-green         |
| Readability priority | The viewer must read “fine sedge tuft/colony,” not generic thick grass                                       |
| Decorative detail    | Sparse dry blade or tiny culm permitted; never add berry-like red dots or flower colors not present in state |
| Animation            | Optional one-pixel asynchronous sway across tuft groups; no synchronized waving                              |
| Occlusion            | May overlap leaf litter and neighboring sedge; must not conceal resource-selection markers                   |

#### Sprite-state set

| Domain state                     | Required visual                                                                       |
| -------------------------------- | ------------------------------------------------------------------------------------- |
| `emerging`                       | Small, bright, sparse blades                                                          |
| `vegetative`                     | Approved lush tuft baseline                                                           |
| `flowering`                      | Vegetative tuft plus subtle upright flowering culms                                   |
| `stressed`                       | Thinner, slightly curled, desaturated blades                                          |
| `senescent`                      | Mixed straw and muted green                                                           |
| `dormant` / `absent_aboveground` | No living tuft sprite; optional persistent dry trace only if domain state provides it |

**Prohibited visual inference:** The renderer may not add flowering culms because the season “looks like spring”; it must receive `flowering` from world state.

**First sprite test:** Create a three-tuft cluster and verify that the ant remains readable over it at normal zoom.

---

## 5. Record: Large-flowered bellwort

### 5.1 Identity

| Field             | Value                                                                                                                                                                           |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `species_id`      | `flora.large_flowered_bellwort`                                                                                                                                                 |
| `record_version`  | `0.1.0`                                                                                                                                                                         |
| `record_status`   | `draft`                                                                                                                                                                         |
| `kingdom`         | Plantae                                                                                                                                                                         |
| `scientific_name` | *Uvularia grandiflora* Sm.                                                                                                                                                      |
| `taxon_rank`      | species                                                                                                                                                                         |
| `common_names`    | Large-flowered bellwort; bellwort; great merrybells                                                                                                                             |
| `regional_scope`  | Wisconsin Driftless-inspired mesic woodland and dappled edge                                                                                                                    |
| `native_status`   | native to eastern North America; accepted for the Wisconsin scenario                                                                                                            |
| `taxonomic_notes` | Modern treatments commonly place *Uvularia* in Colchicaceae. Older horticultural sources may describe it as a lily-family plant. This difference does not affect v0.1 behavior. |

### 5.2 Ecological facts

| Attribute           | Value                                                                                                | Classification                        |
| ------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------------- |
| Life form           | Long-lived rhizomatous perennial woodland forb                                                       | `observed_fact`                       |
| Mature height       | Prairie Moon lists 12 in; UW Extension describes dense clumps about 12–20 in                         | `observed_fact`                       |
| Vertical layer      | Low woodland herb layer above sedge                                                                  | `derived_fact`                        |
| Growth form         | Dense vase-shaped clump; short rhizomes; slow vegetative spread                                      | `observed_fact`                       |
| Emergence/bloom     | Early spring emergence; yellow flowers in April and May                                              | `observed_fact`                       |
| Summer persistence  | Foliage remains through summer; it is not a true spring ephemeral                                    | `observed_fact`                       |
| Flower form         | One to four hanging yellow flowers, approximately 1.5 in, with six overlapping tepals                | `observed_fact`                       |
| Post-flower form    | Three-cornered seed capsule; stems and leaves become more erect after bloom                          | `observed_fact`                       |
| Light               | Partial shade to shade; medium shade is a strong fit                                                 | `observed_fact`                       |
| Moisture            | Medium-dry through medium-wet in Prairie Moon's catalog; UW Arboretum emphasizes consistent moisture | `observed_fact`                       |
| Soil                | Loam, clay, or sand listed horticulturally; rich woodland context preferred for scenario placement   | `observed_fact` / `simulation_choice` |
| Habitat             | Woodland floor, shaded border, and wood margin                                                       | `observed_fact`                       |
| Spread              | Slow spread by rhizomes; clump formation                                                             | `observed_fact`                       |
| Seasonal silhouette | Drooping during expansion and bloom, more erect afterward                                            | `observed_fact`                       |

**Uncertainty:** Published horticultural height and moisture ranges vary. The simulation should model a broad suitable band and avoid a fabricated single moisture optimum.

### 5.3 Simulation representation

| Field                | v0.1 decision                                                                                      | Classification      |
| -------------------- | -------------------------------------------------------------------------------------------------- | ------------------- |
| `simulation_role`    | Individually inspectable flowering woodland plant and seasonal-state exemplar                      | `simulation_choice` |
| `modeled_entity`     | Persistent bellwort clump with stable identity                                                     | `simulation_choice` |
| `modeled_structures` | Stems, flowers, and seed capsules represented as state-dependent structures                        | `simulation_choice` |
| Required inputs      | Season/accumulated warmth, canopy light, soil moisture                                             | `simulation_choice` |
| Optional inputs      | Drainage, soil organic matter, competition, temperature history                                    | `simulation_choice` |
| Preferred            | Dappled/medium shade with consistent medium moisture                                               | `derived_fact`      |
| Tolerated            | Shade and a broader medium-dry to medium-wet band                                                  | `derived_fact`      |
| Unsuitable           | Prolonged severe drought or sustained saturation; exact thresholds unknown                         | `hypothesis`        |
| Logical footprint    | One cell per clump                                                                                 | `simulation_choice` |
| Spread               | Slow local clump expansion; new clumps deferred                                                    | `simulation_choice` |
| Resource behavior    | No ant food resource in v0.1; flowers and capsules are organism structures, not generic food piles | `simulation_choice` |

#### Lifecycle states

```text
dormant
  → emerging
  → vegetative_drooping
  → flowering
  → fruiting
  → vegetative_erect
  → senescent
  → dormant
```

`stressed` is an orthogonal condition that modifies active states rather than replacing the seasonal lifecycle.

#### Required history events

* Clump established
* Seasonal emergence
* First flower opened
* Flowering ended
* Fruit capsule formed
* Post-flowering posture changed
* Stress entered and recovered
* Senescence began
* Aboveground growth became dormant

#### v0.1 simplifications

* One clump is represented as one plant entity even if it contains several shoots.
* Pollination and viable seed production are not simulated.
* Flower count is a small displayable state value, not a complete reproductive model.
* Rhizome geometry and genetic individuals are deferred.

### 5.4 Sprite brief

| Property             | Direction                                                                                                                |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Logical footprint    | 1 cell                                                                                                                   |
| Visual footprint     | May extend about 8 px above and 5 px laterally beyond the cell to communicate height                                     |
| Scale target         | Clearly taller than sedge; below the approved ant’s apparent length but visually prominent because of the yellow flowers |
| Silhouette keys      | Arcing stems, alternate broad leaves, one to three pendant bell-like yellow flowers, vase-shaped clump                   |
| Palette              | Luminous spring green; warm butter-yellow flowers; cool teal/indigo undersides and cast shadows                          |
| Readability priority | The flowers must visibly hang; avoid an upright daisy or generic star-flower silhouette                                  |
| Decorative detail    | A few leaf turns may reveal cool shadow; do not add scattered yellow pixels that resemble resource markers               |
| Animation            | Very gentle independent nod of flower heads or stem sway; optional after static states pass                              |
| Occlusion            | Foliage may overlap sedge and litter; selection outline must trace the clump rather than the full overhang box           |

#### Sprite-state set

| Domain state          | Required visual                                    |
| --------------------- | -------------------------------------------------- |
| `emerging`            | Compact folded shoots, no open flowers             |
| `vegetative_drooping` | Curved young stems and leaves, no flowers          |
| `flowering`           | Approved signature form with pendant yellow bells  |
| `fruiting`            | Flowers replaced by subtle three-angled capsules   |
| `vegetative_erect`    | Greener, more upright summer posture               |
| `stressed` modifier   | Reduced turgor/color with domain-provided severity |
| `senescent`           | Yellowing/browning foliage                         |
| `dormant`             | No aboveground sprite                              |

**Prohibited visual inference:** A drooping flowering plant is its normal form and must not automatically be rendered as water-stressed.

**First sprite test:** Compare one-flower and three-flower variants at normal zoom; choose the minimum flower count that remains unmistakably bellwort without dominating the tile.

---

## 6. Record: True morels

### 6.1 Identity

| Field             | Value                                                                                                                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `species_id`      | `fungi.true_morel_eastern_unresolved`                                                                                                                                                       |
| `record_version`  | `0.1.0`                                                                                                                                                                                     |
| `record_status`   | `draft`                                                                                                                                                                                     |
| `kingdom`         | Fungi                                                                                                                                                                                       |
| `scientific_name` | *Morchella* spp.                                                                                                                                                                            |
| `taxon_rank`      | genus-level unresolved regional concept                                                                                                                                                     |
| `common_names`    | True morel; morel                                                                                                                                                                           |
| `regional_scope`  | Eastern North American, non-burn spring woodland morel concept for a Driftless-inspired scenario                                                                                            |
| `native_status`   | not expressed as a plant-style native flag; regional occurrence accepted, exact simulated species unresolved                                                                                |
| `taxonomic_notes` | The record intentionally avoids the outdated catch-all “*Morchella esculenta*” for all yellow morels. Species-level assignment requires evidence the art and simulation do not yet possess. |

### 6.2 Ecological facts

| Attribute               | Value                                                                                                                                                  | Classification      |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------- |
| Life form               | Ascomycete fungus; most of the organism is below ground                                                                                                | `observed_fact`     |
| Visible structure       | Aboveground fruiting body with a ridged, pitted head                                                                                                   | `observed_fact`     |
| Vertical layer          | Subsurface organism with temporary low aboveground fruiting structures                                                                                 | `derived_fact`      |
| Longevity               | Mycelial persistence and individual boundaries are difficult to determine                                                                              | `observed_fact`     |
| Fruiting season         | Spring in eastern North American accounts                                                                                                              | `observed_fact`     |
| Fruiting controls       | Suitable temperature and moisture are important; exact triggers vary and remain incompletely understood                                                | `observed_fact`     |
| Fruiting patterns       | May recur at a location, follow death of an associate, or follow major disturbance, depending on taxon and context                                     | `observed_fact`     |
| Trophic strategy        | Morels may be saprobic or form plant associations; genus-level ecology is plastic                                                                      | `observed_fact`     |
| Tree association        | Eastern yellow morels are frequently associated in local ecological knowledge with elm, apple, and ash; association is not proof of a simple host rule | `observed_fact`     |
| Tree-death relationship | Fruiting can increase following death of an associated tree, but mechanism and predictability are not fully resolved                                   | `observed_fact`     |
| Appearance              | Color and form vary with species, genetics, age, sunlight, and environment                                                                             | `observed_fact`     |
| Edibility               | Outside simulator scope; the game must not function as a foraging-identification guide                                                                 | `simulation_choice` |

**Uncertainty:** Morel taxonomy, nutrition, species boundaries, host relationships, and fruiting triggers are complex. The first record represents a regional ecological guild, not a claim that all morels behave identically.

### 6.3 Simulation representation

| Field                          | v0.1 decision                                                                                                          | Classification                                 |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------- |
| `simulation_role`              | Hidden fungal presence with conditional, temporary fruiting bodies                                                     | `simulation_choice`                            |
| `modeled_entity`               | Persistent subsurface fungal patch with stable identity                                                                | `simulation_choice`                            |
| `modeled_structures`           | Zero or more aboveground fruiting clusters linked to the patch                                                         | `simulation_choice`                            |
| Required inputs                | Season, recent temperature, recent rainfall/soil moisture, associated-tree/root-zone condition                         | `simulation_choice`                            |
| Optional inputs                | Leaf litter, soil temperature, disturbance history, substrate chemistry, fungal competition                            | `simulation_choice`                            |
| Preferred                      | Spring; cool-to-warming recent temperatures; moist but not assumed saturated soil; suitable woodland/root-zone context | `derived_fact`                                 |
| Association for first scenario | Dead or recently declining elm root zone                                                                               | `simulation_choice` based on regional evidence |
| Logical footprint              | Multi-cell hidden fungal patch; each fruiting cluster occupies one logical cell                                        | `simulation_choice`                            |
| Resource behavior              | Fruiting bodies are inspectable biological structures, not generic FOOD in v0.1                                        | `simulation_choice`                            |
| Visibility                     | Hidden patch is visible only through an inspector/debug overlay; fruiting structures use world sprites                 | `simulation_choice`                            |

#### Lifecycle states

Persistent fungal patch:

```text
present_hidden
  ↔ active_hidden
  → fruiting_eligible
  → present_hidden
```

Fruiting structure:

```text
emerging
  → fresh
  → mature
  → aging
  → collapsed
  → absent
```

The fruiting structure may become absent; the linked fungal patch and every structure event remain in history.

#### Required history events

* Fungal patch established or scenario-seeded
* Patch became metabolically active/inactive
* Fruiting eligibility began and ended
* Fruiting cluster emerged
* Cluster reached maturity
* Cluster began aging
* Cluster collapsed
* Visible structure became absent
* Associated tree/root-zone condition changed

#### v0.1 simplifications

* The hidden network uses a finite set of occupied cells rather than continuous mycelial geometry.
* One unresolved eastern morel concept stands in for multiple possible species.
* The dead-elm relationship is a scenario rule, not a universal rule for *Morchella*.
* Spore dispersal, mating, sclerotia, genetics, harvest, consumption, and toxicity are deferred.
* Fruiting eligibility uses broad conditions and probability; it must not be guaranteed by a dead elm plus rain.

### 6.4 Sprite brief

| Property             | Direction                                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------------------------- |
| Logical footprint    | 1 cell per visible cluster                                                                                    |
| Visual footprint     | Approved large cluster may extend about 6 px above and 4 px laterally beyond its cell                         |
| Scale target         | Preserve the approved enlarged three-morel cluster; large enough for honeycomb texture to read beside the ant |
| Silhouette keys      | Three uneven heights; conical-to-ovoid pitted caps; pale stems; direct ground emergence                       |
| Placement            | Soil/leaf litter near a dead-elm root zone; never visibly sprouting from the log itself                       |
| Palette              | Warm tan, ochre, and muted honey highlights; deep brown pits; pale cream stems; cool shadow at ground contact |
| Readability priority | Pitted morel caps must distinguish the cluster from generic red-capped mushrooms                              |
| Decorative detail    | Small leaf-litter fragments around the base are allowed; no red cap, white spots, or fairy-ring cues          |
| Animation            | None for fresh/mature states; a subtle time-based slump may be considered for aging                           |
| Occlusion            | May sit among sedge or litter, but the full cap silhouette and selection highlight must remain visible        |

#### Sprite-state set

| Domain state | Required visual                                                  |
| ------------ | ---------------------------------------------------------------- |
| `emerging`   | Short pale stems and small compact caps                          |
| `fresh`      | Upright cluster with lighter honey ridges                        |
| `mature`     | Approved three-morel design and strongest readable pit pattern   |
| `aging`      | Darker, drier caps; slight lean                                  |
| `collapsed`  | Low folded/darkened remains, clearly not a harvestable food pile |
| `absent`     | No world sprite; history and hidden patch persist                |

**Prohibited visual inference:** The renderer may not show morels merely because a dead elm is present. It requires an actual fruiting structure in world state.

**First sprite test:** Rebuild the approved cluster at strict production resolution, then test it against leaf litter, sedge, deep shade, and selection overlays.

---

## 7. Cross-species vertical slice

### 7.1 Minimal world support

The three records depend on:

| World property           |                     Sedge |                  Bellwort |             Morel |
| ------------------------ | ------------------------: | ------------------------: | ----------------: |
| Canopy light             |                  Required |                  Required |        Contextual |
| Soil moisture            |                  Required |                  Required |          Required |
| Drainage                 |                  Required |         Deferred/optional | Deferred/optional |
| Season/time              |                  Required |                  Required |          Required |
| Recent temperature       |                  Deferred |                    Useful |          Required |
| Recent rainfall          | Indirect through moisture | Indirect through moisture |          Required |
| Leaf-litter depth        |                  Deferred |                  Deferred |          Optional |
| Root-zone/tree condition |                        No |                        No |          Required |

### 7.2 Initial May snapshot

* Pennsylvania sedge: `vegetative`, with a small subset `flowering`
* Large-flowered bellwort: `flowering`
* Hidden morel patch: `active_hidden`
* One visible morel cluster: `fresh` or `mature`
* Soil: recently moistened, not saturated
* Light: dappled transition from brighter opening to cool woodland shade
* Dead elm: mostly outside or at the edge of the playable cells, with its root zone represented in the world

### 7.3 Minimum inspector output

Selecting an organism should show:

* stable entity ID,
* species/common name,
* current lifecycle state,
* age or establishment time when known,
* current habitat inputs,
* categorical suitability,
* active stressors,
* linked structures,
* and chronological state history.

For morels, the normal inspector must distinguish the hidden fungal entity from a selected fruiting cluster.

## 8. Production order

1. Confirm this record contract.
2. Define the shared lifecycle/state vocabulary as code-facing enums or value objects.
3. Confirm how multi-cell colonies and hidden patches relate to the existing stable-ID registry.
4. Create strict-resolution silhouette tests:

   * bellwort first, because it has the clearest individual silhouette;
   * morel second, because its concept design is already approved;
   * sedge third, because it must be evaluated as a repeated terrain layer.
5. Test all three over the same 32×32 terrain grid at normal game zoom.
6. Add final sprites only after the states are legible under shade and selection overlays.

## 9. Deferred decisions

* Exact numeric growth and fruiting thresholds
* How simulation time maps to real hours, days, and seasons
* Competition and carrying-capacity model
* Seed, spore, and genetic inheritance systems
* Ant consumption or harvesting of any organism structure
* Morel species-level resolution
* Slime mold and decaying-log microhabitat
* Final file formats, atlas layout, and animation frame counts

## 10. Sources

Accessed 2026-07-26.

### Pennsylvania sedge

1. UW–Madison Arboretum, “*Carex pensylvanica* — Pennsylvania Sedge.” Height, flowering period, rhizomatous spread, moisture limits, woodland-margin habitat, and Wisconsin range.
   https://arboretum.wisc.edu/content/uploads/2015/03/PI_Pennsylvania-Sedge.pdf
2. UW–Madison Arboretum, “Gardening with Native Plants: Woodland Plants for Shaded Gardens.” Intermediate-shade ground-cover use.
   https://arboretum.wisc.edu/news/arboretum-news/gardening-with-native-plants-woodland-plants/
3. USDA PLANTS, “*Carex pensylvanica* Lam.” Broad native-status reference.
   https://plants.sc.egov.usda.gov/plant-profile/CAPE6

### Large-flowered bellwort

4. Prairie Moon Nursery, “*Uvularia grandiflora* Bellwort.” Light, moisture, soil, height, bloom period, rhizome, and horticultural range.
   https://www.prairiemoon.com/uvularia-grandiflora-bellwort
5. University of Wisconsin–Madison Extension, “Bellwort, *Uvularia grandiflora*.” Morphology, clump form, flower and fruit structure, emergence, and summer persistence.
   https://hort.extension.wisc.edu/articles/bellwort-uvularia-grandiflora/
6. UW–Madison Arboretum, “Gardening with Native Plants: May Favorites.” Medium-shade and consistent-moisture guidance.
   https://arboretum.wisc.edu/news/arboretum-news/gardening-with-native-plants-may-favorites/

### Morels

7. Emery, M. R. and Barron, E. S., USDA Forest Service, “Using Local Ecological Knowledge to Assess Morel (*Morchella*) Ecology and Population Dynamics.” Hidden fungal body, fruiting patterns, trophic variability, temperature/moisture dependence, and eastern tree associations.
   https://research.fs.usda.gov/download/treesearch/36229.pdf
8. Pilz, D. et al., USDA Forest Service, “Ecology and Management of Morels Harvested From the Forests of Western North America.” Taxonomic and ecological uncertainty, variable form, forest fruiting, and tree-death/disturbance relationships. Used for genus-level principles, not to assert Wisconsin-specific thresholds.
   https://www.fs.usda.gov/pnw/pubs/pnw_gtr710.pdf
