# Of the Waters

Player-facing site for a Mothership campaign set in the Jump Era (3249), served by GitHub Pages.

- `index.html`: home page
- `_episodes/`: one Markdown file per session (copy `_templates/episode.md`); images go in `assets/episodes/`
- `starmap/`: player edition of the starmap, a snapshot of the GM's map. Visitors' changes stay in their own browser; **Send my changes to the GM** packages them as a code or file, which the GM reviews change by change in their own copy of the map (Player changes).
- `chronology/`: read-only setting timeline
- `world-classes/`: the world-classification reference

The starmap, chronology and world-class pages are generated from the GM's working copies; notes marked GM-only are left out.

## Licensing

This repository uses two licenses.

**Code: MIT** (`LICENSE`). The site templates and styles (`_layouts/`, `assets/site.css`), the build tools (`tools/`), and the program code of the starmap, chronology and world-class pages.

**Campaign content: CC BY-NC 4.0** (`LICENSE-CONTENT.md`). Everything written or made for the campaign: the episodes and their images (`_episodes/`, `assets/episodes/`), the text of the home page, and the setting material inside the starmap and chronology (system names, sectors, notes, planetary systems, objects, jump routes and timeline entries). You may share and adapt it for non-commercial purposes, with credit to the author and a link to the license.

**Third-party material** keeps its own terms and is credited on the site's Credits page:

- Mothership is a trademark of Tuesday Knight Games. This is an unofficial fan campaign, not affiliated with or endorsed by them; the site reproduces none of their text or art and does not use their logo.
- Terminology and ideas from the Orion's Arm Universe Project (https://orionsarm.com), used with permission: the NoLWoCS and EWoCS world classifications, and alien biochemistry, ecology and exotic-life concepts in the planetary profiles. One catch-all credit on the Credits page covers all of it. Never copy their text beyond a short phrase or a technical term; write everything in our own words. Orion's Arm content belongs to the project and its contributors.
- Star data from the HYG database (Hipparcos, Yale, Gliese, Gaia); known exoplanets from the Open Exoplanet Catalogue and NASA Exoplanet Archive; three.js (MIT); fonts under the SIL Open Font License.

Never add module or rulebook text, maps or art from Tuesday Knight Games or other publishers here: write episode recaps in your own words.
