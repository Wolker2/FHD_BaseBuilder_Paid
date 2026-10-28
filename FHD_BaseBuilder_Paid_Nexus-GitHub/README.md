# FHD_BaseBuilder_Paid — source for Nexus Mods review

**Verified on 28 October 2026: all 13 runtime files rebuild from editable source with exactly the original SHA-256 hashes.** The build uses Python 3.10+ and its standard library. No original binaries, Windows tools, game installation or network downloads are required.

The supplied module declares **version 2.5.2**, author **Prolog_D**, conflict **FHD_BaseBuilder_Free**, and installation at `Mods/FHD_MODS/FHD_BaseBuilder_Paid`. Existing metadata and runtime values remain unchanged.

## Contents

| Path | Purpose |
| --- | --- |
| `source/CFG/Main.json` | Complete UI and event-hook configuration |
| `source/CFG/CacheData.json` | Resource aliases and paths |
| `source/CFG/Rus/Lang.json` | Complete language tree and embedded station-building code |
| `source/DATA/Interface/*.json` | Exact sources for all nine GI images |
| `source/ModuleInfo.txt` | Editable UTF-8 metadata, emitted as original CP1251 |
| `scripts/` | Independent DAT/GI codecs, complete builder and resource audit |
| `tests/` | Hash checking, source edits and isolated source-only rebuild |
| `original-file-sha256.json` | Original hashes for all 13 runtime files |
| `build-verification.json` | Completed verification results and tool versions |
| `.github/workflows/build.yml` | GitHub build/check workflow |

The screenshot `ИНВЕСТИЦИЙ.bmp` and original runtime binaries are excluded from this compact source package. The input archive contained no DLL, EXE or SCR. An RSON project is not needed: the mod's executable statements are fully visible in configuration JSON, primarily under `Script.FHDBaseBuilderPaid` in `Lang.json`.

## Build and test

```sh
python3 scripts/build.py --strict-original
python3 -m unittest discover -s tests -v
```

Verified environment: Python 3.12.14 and zlib 1.3.2. Output: `dist/FHD_BaseBuilder_Paid_FROM_SOURCE.zip` and `dist/build-report.json`.

The build recreates all three DATs, nine GIs and ModuleInfo, checks the complete runtime file list and SHA-256 hashes, audits local CacheData resource paths and validates ZIP integrity. All ten CacheData references resolve to rebuilt files. A separate test rebuilds the entire mod in a temporary directory containing only source, scripts and the reference hash manifest.

For deliberate source changes, omit `--strict-original`; the report lists differing hashes. GitHub hosted execution was not performed during preparation.

## Editable source formats

The DAT JSON includes every string, block, record order, sorting metadata and cipher seed. Parameter `value` strings contain the original runtime code. Editing the included source is sufficient to rebuild it; external decompilation or manual source recovery is not required.

The GI JSON includes all header fields, bounds, reserved values and pixel data. This mod uses one type-2 image with RGB565/alpha RLE packets and eight type-0 images. Type-0 `rgb565` samples are 16-bit packed colors; `argb8888` samples are unsigned `0xAARRGGBB` values written in little-endian BGRA order. No original GI blob or opaque code payload is embedded in the sources.

Tests cover exact image roundtrips and pixel edits in all three representations, an edit to embedded construction code, and the complete source-only build. Original metadata byte encoding and line endings are preserved.

## Provenance and limits

Input: `FHD_BaseBuilder_Paid.rar`, SHA-256 `7fbbadeb6688357722f655b0cf1038a89d22149d6d31fee552de86dc12322a26`. All fourteen files were extracted successfully; thirteen runtime files are reproduced, and the unreferenced screenshot is omitted.

The independent Python DAT codec follows format conventions studied in Sergei Osminin's MIT-licensed [rangers-utils](https://github.com/murgesku/rangers-utils): UTF-16LE BlockPar trees, CRC32, zlib and the game's stream cipher. GI format handling was checked against the previously supplied [SRHD-XenoModKit](https://github.com/Xenomorphchyma/SRHD-XenoModKit) image codec. No third-party binary editor or game executable is bundled. Existing authorship and licensing are not changed by this preparation.

Byte identity establishes preservation of the supplied mod. Game execution, in-game code compilation, construction/economy behavior, antivirus verdicts and Nexus moderation approval were not performed or claimed.
