# FantasyTD Reboot — Production Charter (2026-10-25)

## Mission
Rebuild FantasyTD as a polished, original, touch-first, landscape Android fantasy plant tower-defense game. This charter proposes a new direction; existing AGENTS.md remains binding until a dedicated approved scope-change ticket updates it.

## Verified baseline
- GitHub repo: SonGohan231/FantasyTD, main.
- Unity root: UnityProject; editor config 6000.0.26f1; UGUI and Physics2D listed in manifest.
- Local candidate: /home/adambrdon/Repos/FTD/FantasyTD-Unified-20261023/UnityProject; Forest01 and Forest01_TerrainTest scenes found.
- Unity MCP reports no active editor session. No compilation, PlayMode, device test, or APK has been verified.

## Visual north star
Organic hand-painted fantasy with high-clarity silhouettes, dimensional lighting, responsive character animation, cohesive materials, restrained VFX and an accessible touch HUD. Original artwork only. No sci-fi, no reused protected game art. Target 60 FPS on defined reference Android devices.

## Core design contract (subject to playtesting)
Landscape 2D/2.5D, winding path and fixed planting sockets, visible evolving living plant defenders, Essence resource economy, readable enemy telegraphs, boss encounters, strategic upgrades and meaningful map-specific interactions. Keep names Pędostrzał, Kwiat Esencji, Dębowy Strażnik, Mroźny Pąk and existing enemy roster for first vertical slice pending review. MAP-A baseline: 24x14 world units, 12 planting sockets, 4 plants, 4 regular enemy types, Król Cierni boss, 6 waves, 20 HP, radial menu, win/lose/restart.

## Architecture proposal
Separate deterministic simulation (waves, targeting, combat, economy, status effects, victory conditions) from Unity scene presentation (animations, particles, camera, UI, audio). Use ScriptableObject definitions for plants, enemies, wave schedules, upgrades and level topology. Introduce save-schema versioning and migration tests. Prefer object pooling, atlas-friendly sprites, device profiles and Unity Test Framework EditMode tests. Implement only after project inventory and technical review.

## Work packages / quality gates
1. T0100 inventory and baseline: compare all local candidates against main; inspect scene/prefab/script/art inventories, licenses and existing tests. Produce evidence matrix and freeze backup. PASS only with documented sources.
2. T0101 design bible: game loop, player experience, progression, balancing, art bible, UI and audio style, technical budgets. PASS with acceptance criteria and visual references.
3. T0102 Unity foundation: modular systems and automated tests; PASS only with compilation and EditMode results.
4. T0103 MAP-A production: art pipeline, original level, plants, enemies, six waves, effects and HUD. PASS with PlayMode and manual touch tests.
5. T0104 Android release candidate: reproducible signed/unsigned build as appropriate, APK hash, device install, runtime/performance evidence and defect log.
6. Expand campaign only after vertical slice gate passes.

## Tracking rules
One active implementation ticket per branch. Log every ticket's status, changed files, test evidence, risks and next action. Never conflate static source inspection with a working build. Never delete existing assets before provenance review and backup. No automatic merge to main.

## Current status
T0100 IN PROGRESS (partial source inspection). Unity editor session BLOCKED. All implementation, art generation, runtime tests and APK NOT STARTED/NOT VERIFIED.
