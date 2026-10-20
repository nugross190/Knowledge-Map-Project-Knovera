# Plan

Where this project is going, step by step. Each phase starts only when the one before it is working with real students.

**Brand:** practitioner-checked items. Agents draft every item, a script checks every numeric answer, and teachers review and correct the items before they are sold, with credit to the reviewing teachers.

## Phase 1: Now

Uses what already exists (`data/modules/`, `print/`, `specs/tka-templates/`).

1. **Grade X semester modules.** Printable modules that follow the school semester, starting with the subjects taught in class. Vektor dan Gerak (`print/vektor-gerak.pdf`) is the first; next is the next topic on the semester calendar.
2. **TKA modules.** TKA Fisika and TKA Matematika practice, 3–4 modules each, built from agent-written items corrected by teachers. The transcribed TKA 2025 papers (`data/tka/`) stay in the repository as reference and are never sold.
3. **Free diagnostic.** A short test (about 15 questions) that ends by recommending the module a student needs. It grows from the *Cek Prasyarat* → *Kotak Ingat* routing already in the printable modules.
4. **Teacher review loop.** Reviewing teachers agree up front how their corrections are used, and are credited (or paid per reviewed module).
5. **First sales.** Put one small bundle in front of 5–10 students. Track who finishes the diagnostic, who pays, and where they get stuck.

Keep paid modules out of this repository: `docs/` is public on GitHub Pages. Only free samples go there.

## Phase 2: Next

Tools that grow from Phase 1 content.

6. **Teacher administration maker.** Generates Kurikulum Merdeka paperwork (Modul Ajar, ATP, Prota/Promes, KKTP, assessment sheets) from the same content and item bank. Teachers are its first users, which also grows the review network.
7. **Catch-up modules.** For students with large gaps: the basics they skipped, chosen by the diagnostic.
8. **First interactive piece.** One coordinate/vector canvas: students enter points, vectors or equations and see the figure. One component serves both math (shapes, transformations, graphs) and physics (displacement, resultants, trajectories), embedded in the module pages.

## Phase 3: Later

Once modules sell.

9. **Online learning platform** for reading, math and science literacy: accounts, progress, learning paths driven by the diagnostic, payments, and a library of sims built one reusable component at a time.

## Set aside

- **Psychological / interest-and-talent test (tes minat bakat).** Needs a licensed psychologist or official approval. Revisit once there is a credible licensed partner.
