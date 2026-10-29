"""Tests for scripts/build.py. Run: python -m unittest discover -s tests

The tests never write into the repository: builds go to temporary folders.
"""
import functools
import importlib.util
import json
import re
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build  # noqa: E402
import check_generated  # noqa: E402

ROOT = build.ROOT


@functools.lru_cache(maxsize=None)
def site():
    """The repository's data, loaded once. Tests that change it work on a copy (json round trip)."""
    return build.load_site()


def copy(value):
    return json.loads(json.dumps(value))


def payload(page, name):
    """The JSON a page carries in `const <name> = ...;`, decoded."""
    return json.loads(page.split(f"const {name} = ")[1].split(";\n")[0].replace("<\\/", "</"))


def row(**kw):
    base = {"id": "SNI-01-900", "simpul": "SNI-01", "tingkat": "1", "soal": "Soal uji?", "jawaban": "Jawaban", "catatan": ""}
    base.update(kw)
    return base


class ValidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.topics, cls.rows = site().topics, site().rows

    def errors(self, *extra):
        return build.validate(self.topics, self.rows + list(extra))

    def test_bank_is_valid(self):
        self.assertEqual(build.validate(self.topics, self.rows), [])

    def test_every_topic_has_questions(self):
        used = {r["simpul"] for r in self.rows}
        for d in self.topics["domains"]:
            for code in d["topics"]:
                self.assertIn(code, used, f"{code} has no questions")

    def test_weights_sum_to_100(self):
        self.assertEqual(sum(d["weight"] for d in self.topics["domains"]), 100)

    def test_rejects_duplicate_id(self):
        self.assertTrue(any("duplicate id" in e for e in self.errors(row(id=self.rows[0]["id"], soal="Lain?"))))

    def test_rejects_unknown_topic(self):
        self.assertTrue(any("unknown simpul" in e for e in self.errors(row(id="XXX-01-001", simpul="XXX-01"))))

    def test_rejects_id_outside_its_topic(self):
        self.assertTrue(any("must start with" in e for e in self.errors(row(id="SNI-02-900"))))

    def test_rejects_bad_level(self):
        self.assertTrue(any("tingkat" in e for e in self.errors(row(tingkat="4"))))

    def test_rejects_empty_answer(self):
        self.assertTrue(any("required" in e for e in self.errors(row(jawaban=""))))

    def test_rejects_repeated_question(self):
        self.assertTrue(any("same question" in e for e in self.errors(row(soal=self.rows[0]["soal"].upper()))))

    def test_whole_site_is_valid(self):
        self.assertEqual(build.validate_site(site()), [])


class PagesTest(unittest.TestCase):
    """Cross-page links: file names in docs/, URLs in the hosted claude.ai copies."""

    @classmethod
    def setUpClass(cls):
        cls.local = build.render_site(site(), {})
        cls.links = build.hosted_links(site())
        cls.hosted = build.render_site(site(), cls.links)

    def test_every_hosted_page_is_built(self):
        self.assertTrue(set(build.ARTIFACT_URLS) <= set(self.local), "every hosted page must also be built locally")
        self.assertEqual(set(self.links), set(build.page_names(site())))
        self.assertTrue(set(self.local) <= set(self.links), "every built page needs a hosted link")

    def test_local_pages_link_by_file_name(self):
        for name, body in self.local.items():
            self.assertNotIn("/*__DATA__*/", body, name)
            self.assertNotIn(build.PAGES_URL, body, f"{name} links to the hosted site instead of a local file")
            for url in build.ARTIFACT_URLS.values():
                self.assertNotIn(url, body, f"{name} links to a hosted copy instead of a local file")

    def test_hosted_pages_link_by_url(self):
        self.assertIn(build.ARTIFACT_URLS["peta.html"], self.hosted["bank.html"])
        self.assertIn(build.ARTIFACT_URLS["bank.html"], self.hosted["peta.html"])
        self.assertIn(f'href="{build.PAGES_URL}"', self.hosted["peta-fisika.html"])
        # A page without a hosted copy is reached on GitHub Pages, in attributes and in the page data alike.
        self.assertEqual(payload(self.hosted["peta-fisika.html"], "MAP")["bank"], build.PAGES_URL + "bank-fisika.html")
        names = "|".join(re.escape(n) for n in self.links)
        for name in build.ARTIFACT_URLS:
            self.assertIsNone(re.search(f'href="({names})', self.hosted[name]), f"{name} keeps a relative link")

    def test_pages_url_and_site_base_agree(self):
        self.assertTrue(build.PAGES_URL.startswith("https://") and build.PAGES_URL.endswith("/"))
        self.assertTrue(build.PAGES_URL.endswith(build.SITE_BASE))
        self.assertTrue(build.SITE_BASE.startswith("/") and build.SITE_BASE.endswith("/"))

    def test_templates_are_assembled(self):
        for name, body in self.local.items():
            self.assertNotIn("/*@include", body, name)
            self.assertNotIn("__TITLE__", body, name)
            self.assertEqual(body.count("Shared light theme"), 1, name)
            self.assertNotIn("prefers-color-scheme: dark", body, name)
            self.assertLess(body.index("Shared light theme"), body.index("</style>"), name)

    def test_script_json_cannot_end_the_script(self):
        text = "a </script> b <!-- c -->"
        out = build.script_json({"t": text})
        self.assertNotIn("</", out)
        self.assertNotIn("<!--", out)
        self.assertEqual(json.loads(out.replace("<\\/", "</")), {"t": text})


class BuildTest(unittest.TestCase):
    """The build into a folder: complete, repeatable, and tidy about files it no longer makes."""

    def test_build_writes_the_site(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            build.build(site(), out)
            self.assertTrue((out / ".nojekyll").exists(), "docs/.nojekyll stops Jekyll from processing the site")
            self.assertEqual(sorted(p.name for p in out.iterdir() if p.name != ".nojekyll"),
                             sorted(build.page_names(site()) + ["questions.json"]))
            page = (out / "404.html").read_text(encoding="utf-8")
            self.assertNotIn("__SITE_BASE__", page)
            self.assertIn(f'href="{build.SITE_BASE}"', page)
            for p in out.glob("*.html"):
                self.assertTrue(p.read_text(encoding="utf-8").startswith(build.HEAD), p.name)

    def test_second_build_changes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            first = build.build(site(), out)[out]
            self.assertTrue(first[0])
            self.assertEqual(build.build(site(), out)[out], ([], []))

    def test_files_no_longer_built_are_removed(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d)
            build.build(site(), out)
            (out / "peta-dihapus.html").write_text("old page", encoding="utf-8")
            (out / "CNAME").write_text("example.org", encoding="utf-8")
            changed, removed = build.build(site(), out)[out]
            self.assertEqual((changed, removed), ([], ["peta-dihapus.html"]))
            self.assertTrue((out / "CNAME").exists(), "files the build does not make are left alone")

    def test_artifact_fragments(self):
        with tempfile.TemporaryDirectory() as d:
            docs, frags = Path(d) / "docs", Path(d) / "build"
            build.build(site(), docs, frags)
            self.assertEqual(sorted(p.name for p in frags.iterdir()),
                             sorted(n.replace(".html", ".fragment.html") for n in build.ARTIFACT_URLS))
            body = (frags / "peta-fisika.fragment.html").read_text(encoding="utf-8")
            self.assertFalse(body.startswith("<!doctype"), "a fragment is the page body only")

    def test_committed_docs_are_up_to_date(self):
        """docs/ in the repository is what the build makes now (CI checks the same after rebuilding)."""
        expected = build.site_files(site())
        docs = ROOT / "docs"
        on_disk = {p.name for p in docs.iterdir() if p.is_file()}
        self.assertEqual(on_disk, set(expected), "run python scripts/build.py")
        for name, content in expected.items():
            data = content.encode("utf-8") if isinstance(content, str) else content
            self.assertEqual((docs / name).read_bytes(), data, f"docs/{name} is out of date: run python scripts/build.py")


class SubjectBanksTest(unittest.TestCase):
    """data/questions/<map id>.csv (specs/question-spec.md)."""

    @classmethod
    def setUpClass(cls):
        cls.banks, cls.maps = site().banks, site().maps

    def test_banks_are_valid(self):
        self.assertTrue(self.banks, "data/questions/ has no banks")
        self.assertEqual(build.validate_subject_banks(self.banks, self.maps), [])

    def test_konteks_share(self):
        for name, rows in self.banks.items():
            share = sum(bool(r["konteks"]) for r in rows) / len(rows)
            self.assertGreaterEqual(share, build.MIN_KONTEKS_SHARE, f"{name}: konteks is {share:.0%}")

    def test_level1_share(self):
        for name, rows in self.banks.items():
            share = sum(r["tingkat"] == "1" for r in rows) / len(rows)
            self.assertGreaterEqual(share, build.MIN_LEVEL1_SHARE, f"{name}: level 1 is {share:.0%}")

    def test_every_topic_has_enough_questions(self):
        for name, rows in self.banks.items():
            per_topic = Counter(r["simpul"] for r in rows)
            for d in self.maps[name]["domains"]:
                for t in d["topics"]:
                    self.assertGreaterEqual(per_topic[t["code"]], build.MIN_PER_TOPIC, f"{name}: {t['code']}")

    def test_rejects_bank_without_map(self):
        rows = next(iter(self.banks.values()))[:1]
        self.assertTrue(any("no map" in e for e in build.validate_subject_banks({"tidak-ada": rows}, self.maps)))

    def test_rejects_empty_bank(self):
        """A header-only CSV is an error, not a division by zero in the report."""
        name = next(iter(self.banks))
        self.assertTrue(any("no questions" in e for e in build.validate_subject_banks({name: []}, self.maps)))

    def test_rejects_unknown_topic(self):
        name, rows = next(iter(self.banks.items()))
        bad = dict(rows[0], id="XXX-01-001", simpul="XXX-01")
        self.assertTrue(any("unknown simpul" in e for e in build.validate_subject_banks({name: rows + [bad]}, self.maps)))

    def test_konteks_items_are_marked_and_html_free(self):
        for name, rows in self.banks.items():
            self.assertTrue(any(r["konteks"] for r in rows), f"{name} has no konteks items")
            for r in rows:
                self.assertNotRegex(r["soal"] + r["jawaban"] + r["catatan"], r"<[a-z/]", f"{name} {r['id']}: the bank page shows text, not HTML")

    def test_bank_pages_are_built_and_linked(self):
        pages = build.bank_pages(self.banks, self.maps, {})
        map_pages = build.map_pages(self.maps, {}, self.banks)
        for name in self.banks:
            body = pages[f"bank-{name}.html"]
            self.assertNotIn("/*__DATA__*/", body)
            data = payload(body, "DATA")
            self.assertEqual(data["bank"]["key"], f"bank-soal-{name}-v1")
            self.assertEqual(data["topics"]["map_url"], f"peta-{name}.html")
            self.assertEqual(payload(map_pages[f"peta-{name}.html"], "MAP")["bank"], f"bank-{name}.html")

    def test_bank_pages_have_swipe_mode(self):
        pages = {**build.bank_pages(self.banks, self.maps, {}),
                 "bank.html": build.pages(site().topics, build.question_json(site().rows), {})["bank.html"]}
        for name, page in pages.items():
            for needle in ('id="feedOpen"', '<dialog class="feed" id="feed"', "function makeFeed", 'get("mode") === "geser"',
                           "function storyGrade"):
                self.assertIn(needle, page, name)
        self.assertIn("MAP.bank + '?mode=geser\"", build.map_pages(self.maps, {})["peta-fisika.html"])


class MapsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maps = site().maps

    def test_there_is_at_least_one_map(self):
        self.assertIn("fisika", self.maps)

    def test_maps_are_valid(self):
        for name, m in self.maps.items():
            self.assertEqual(build.validate_map(name, m), [], name)

    def test_validator_catches_problems(self):
        m = copy(self.maps["fisika"])
        first = m["domains"][0]["topics"][0]
        m["domains"][0]["topics"].append(dict(first))            # duplicate code
        m["domains"][1]["topics"][0]["code"] = "XXX-01"          # wrong domain prefix
        m["domains"][1]["topics"][1]["tier"] = 5                 # bad tier
        m["path"].append({"title": "x", "to": "NOPE-01"})        # dangling path step
        errors = " | ".join(build.validate_map("fisika", m))
        for needle in ("duplicate code", "must start with", "tier must be", "unknown code"):
            self.assertIn(needle, errors)

    def test_maps_follow_soft_rules(self):
        for name, m in self.maps.items():
            self.assertEqual(build.lint_map(name, m), [], name)

    def test_lint_catches_problems(self):
        m = copy(self.maps["fisika"])
        t = m["domains"][0]["topics"][0]
        t["sum"] = "kata " * 40
        t["traps"] = []
        t["blocks"][0]["li"] = ["<b>a</b> dan <b>b</b>"]
        for d in m["domains"]:
            for topic in d["topics"]:
                topic["tier"] = 1
        warnings = " | ".join(build.lint_map("fisika", m))
        for needle in ("summary has", "no traps", "more than one bold", "tier mix"):
            self.assertIn(needle, warnings)

    def test_lanjut_tag(self):
        m = copy(self.maps["fisika"])
        m["domains"][0]["topics"][0]["lanjut"] = "ya"
        self.assertIn("'lanjut' must be true or false", " | ".join(build.validate_map("fisika", m)))
        m["domains"][0]["topics"][0]["lanjut"] = True
        self.assertEqual(build.validate_map("fisika", m), [])
        self.assertIn("no 'lanjut_note'", " | ".join(build.lint_map("fisika", m)))
        tagged = {name for name, mp in self.maps.items() if any(t.get("lanjut") for d in mp["domains"] for t in d["topics"])}
        self.assertTrue({"matematika", "bahasa-indonesia", "bahasa-inggris", "sejarah"} <= tagged, tagged)
        page = build.map_pages(self.maps, {})["peta-matematika.html"]
        self.assertIn('id="onlyLanjut"', page)
        self.assertIn('"lanjut": true', page)

    def test_grades_come_from_src(self):
        m = copy(self.maps["fisika"])
        m["domains"][0]["topics"][0]["src"] = "Kelas 10"
        self.assertIn("src 'Kelas 10' must be one of", " | ".join(build.validate_map("fisika", m)))
        self.assertEqual(build.GRADE_LABELS["Kelas XI–XII"], ["XI", "XII"])
        self.assertEqual(build.GRADE_LABELS["Semua kelas"], ["X", "XI", "XII"])
        page = build.map_pages(self.maps, {})["peta-fisika.html"]
        data = payload(page, "MAP")
        for t in (t for d in data["domains"] for t in d["topics"]):
            self.assertEqual(t["grades"], build.GRADE_LABELS[t["src"]], t["code"])
        self.assertTrue(data["icon"])
        self.assertIn('id="grades"', page)

    def test_map_pages_have_story_mode(self):
        for name, page in build.map_pages(self.maps, {}).items():
            for needle in ('id="feedOpen"', '<dialog class="feed" id="feed"', "function makeFeed", 'params.get("mode") === "geser"'):
                self.assertIn(needle, page, name)

    def test_every_map_has_an_icon(self):
        icons = build.load_icons()
        for name in self.maps:
            self.assertIn(name, icons)

    def test_map_pages_render(self):
        pages = build.map_pages(self.maps, {})
        for m in self.maps.values():
            body = pages[f"peta-{m['id']}.html"]
            self.assertNotIn("/*__MAP__*/", body)
            self.assertNotIn("__TITLE__", body)
            self.assertIn(f"<title>{m['title']}</title>", body)


class SubjectsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.subjects, cls.maps, cls.tka, cls.groups = site().subjects, site().maps, site().tka, site().groups

    def test_roster_is_valid_and_complete(self):
        self.assertEqual(build.validate_subjects(self.subjects, self.maps, self.tka, self.groups), [])

    def test_validator_catches_problems(self):
        subjects = copy(self.subjects)
        subjects.append(dict(subjects[0]))                                   # duplicate id
        subjects[1] = dict(subjects[1], tka=["tka-tidak-ada"])               # unknown TKA bank
        subjects = [s for s in subjects if s.get("map") != "fisika"]         # fisika map left out
        errors = " | ".join(build.validate_subjects(subjects, self.maps, self.tka, self.groups))
        for needle in ("duplicate id", "unknown TKA bank", "map fisika is not listed", "tka-fisika-pilihan-2025 is not listed"):
            self.assertIn(needle, errors)

    def test_validator_checks_groups(self):
        subjects = copy(self.subjects)
        subjects[0]["group"] = "olahraga"
        subjects[1]["also"] = ["ips", "seni"]
        subjects[2].pop("short")
        lanjut = next(s for s in subjects if s.get("lanjut_of"))
        lanjut["group"] = "umum"
        errors = " | ".join(build.validate_subjects(subjects, self.maps, self.tka, self.groups))
        for needle in ("group must be one of", "bad extra group seni", "needs 'short'", "belongs in group 'lanjut'"):
            self.assertIn(needle, errors)

    def test_status_reports_every_subject(self):
        lines = build.subject_status(self.subjects, self.maps, site().banks, self.tka)
        self.assertEqual(len(lines), len(self.subjects) + 1)
        text = "\n".join(lines)
        self.assertIn("tag di peta matematika", text)
        self.assertIn("bank", text)


class TkaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.banks = site().tka

    def test_banks_are_valid(self):
        self.assertTrue(self.banks, "data/tka/ has no banks")
        for name, b in self.banks.items():
            self.assertEqual(build.validate_tka(name, b), [], name)

    def test_validator_catches_problems(self):
        name, b = next(iter(self.banks.items()))
        b = copy(b)
        items = {it["format"]: it for it in b["soal"]}
        b["id"] = "lain"                                          # id differs from file name
        b["soal"].append(dict(b["soal"][0]))                      # duplicate id
        items["pilihan-ganda"]["kunci"] = 9                       # key outside the options
        items["pilihan-ganda"]["passage"] = "NOPE"                # unknown passage
        items["pilihan-ganda"]["soal"] += " [Gambar]"
        items["pilihan-ganda"].pop("gambar", None)                # marker without a description
        items["benar-salah"]["kunci"] = [True]                    # wrong length
        items["benar-salah"].pop("kolom")
        items["pilihan-ganda-kompleks"]["kunci"] = [3, 1]         # not sorted
        items["pilihan-ganda-kompleks"]["keyakinan_kunci"] = "pasti"
        errors = " | ".join(build.validate_tka(name, b))
        for needle in ("must match the file name", "duplicate id", "index of one option", "unknown teks",
                       "no 'gambar'", "one true/false", "needs 'kolom'", "sorted list", "keyakinan_kunci"):
            self.assertIn(needle, errors)

    def test_missing_key_needs_tidak_ada(self):
        name, b = next(iter(self.banks.items()))
        b = copy(b)
        b["soal"][0]["kunci"] = None
        b["soal"][0]["keyakinan_kunci"] = "tinggi"
        self.assertTrue(any("tidak ada" in e for e in build.validate_tka(name, b)))
        b["soal"][0]["keyakinan_kunci"] = "tidak ada"
        self.assertEqual(build.validate_tka(name, b), [])

    def test_tka_page_renders(self):
        built = build.pages(site().topics, [], {}, site().maps, self.banks)
        page = built["tka.html"]
        self.assertNotIn("/*__TKA__*/", page)
        self.assertIn('class="home-link" href="index.html"', page)
        self.assertEqual([b["id"] for b in payload(page, "BANKS")], list(self.banks))
        self.assertIn('href="tka.html"', built["index.html"])

    def test_tka_page_has_swipe_mode(self):
        built = build.pages(site().topics, [], {})
        for needle in ('id="feedOpen"', '<dialog class="feed" id="feed"', "function makeFeed", 'get("mode") === "geser"',
                       "function swipeCheck", 'optsHTML(it, "sw-"'):
            self.assertIn(needle, built["tka.html"])
        self.assertIn('href="tka.html?mode=geser"', built["index.html"])


class TkaTypesTest(unittest.TestCase):
    """data/tka-types.json covers its banks exactly (specs/tka-item-types.md)."""

    def test_every_item_has_exactly_one_type(self):
        types = json.loads((ROOT / "data/tka-types.json").read_text(encoding="utf-8"))
        codes = [t["kode"] for s in types.values() for t in s["types"]]
        self.assertEqual(len(codes), len(set(codes)))
        for subject, s in types.items():
            items = {}
            for b in s["banks"]:
                for it in json.loads((ROOT / f"data/tka/{b}.json").read_text(encoding="utf-8"))["soal"]:
                    items[it["id"]] = it
            mapped = [i for t in s["types"] for i in t["contoh"]]
            self.assertEqual(sorted(mapped), sorted(items), subject)
            for t in s["types"]:
                self.assertIn(t["level"], (1, 2, 3))
                for i in t["contoh"]:
                    self.assertIn(items[i]["format"], t["format"], f"{t['kode']} {i}")

    def test_every_bank_has_a_template(self):
        types = json.loads((ROOT / "data/tka-types.json").read_text(encoding="utf-8"))
        listed = {b for s in types.values() for b in s["banks"]}
        self.assertEqual(listed, {p.stem for p in (ROOT / "data/tka").glob("*.json")})
        for subject in types:
            self.assertTrue((ROOT / f"specs/tka-templates/{subject}.md").exists(), subject)


class ModulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules, cls.maps, cls.types = site().modules, site().maps, site().tka_types

    def test_modules_are_valid(self):
        self.assertIn("vektor-gerak", self.modules)
        for name, mod in self.modules.items():
            self.assertEqual(build.validate_module(name, mod, self.maps, self.types), [], name)
            self.assertEqual(build.lint_module(name, mod), [], name)

    def test_validator_catches_problems(self):
        mod = copy(self.modules["vektor-gerak"])
        items = mod["tahap"][0]["soal"]
        by_format = {it["format"]: it for st in mod["tahap"] for it in st["soal"]}
        items.append(dict(items[0]))                                   # duplicate id
        mod["tahap"][1]["tahap"] = 7                                   # stages out of order
        mod["materi"][0]["simpul"] = ["NOPE-01"]                       # unknown map topic
        by_format["isian"]["kunci"] = "lima"                           # non-numeric key
        by_format["pilihan-ganda"]["kunci"] = 9                        # key outside the options
        by_format["benar-salah"]["kunci"] = [True]                     # wrong length
        tka_item = next(it for st in mod["tahap"] for it in st["soal"] if "tka" in it and it["format"] == "pilihan-ganda")
        tka_item["tka"] = {"tipe": "FIS-HITUNG", "acuan": ["FIS25-002"]}  # example of another type
        errors = " | ".join(build.validate_module("vektor-gerak", mod, self.maps, self.types))
        for needle in ("duplicate id", "numbered 1, 2, 3", "unknown topic", "numeric 'kunci'",
                       "index of one option", "one true/false", "acuan must list"):
            self.assertIn(needle, errors)

    def test_tka_format_must_match_type(self):
        mod = copy(self.modules["vektor-gerak"])
        it = next(i for st in mod["tahap"] for i in st["soal"] if i.get("tka", {}).get("tipe") == "FIS-ANALISIS")
        it["format"], it["kunci"] = "pilihan-ganda-kompleks", [0]
        errors = build.validate_module("vektor-gerak", mod, self.maps, self.types)
        self.assertTrue(any("not allowed for FIS-ANALISIS" in e for e in errors))

    def test_module_pages_render_and_link(self):
        pages = build.module_pages(self.modules, self.maps, {}, self.types)
        home = build.pages(site().topics, [], {}, self.maps, None, self.modules)["index.html"]
        for mod in self.modules.values():
            body = pages[f"modul-{mod['id']}.html"]
            self.assertNotIn("/*__MODULE__*/", body)
            self.assertIn(f"<title>{mod['title']}</title>", body)
            self.assertIn('class="home-link" href="index.html"', body)
            self.assertNotIn("</script><", body.split("const MOD")[1].split(";\n")[0])
            self.assertIn(f'href="modul-{mod["id"]}.html"', home)

    def test_tka_levels_come_from_the_types(self):
        """The "Setara TKA" badge levels are read from data/tka-types.json, not kept in the page."""
        page = build.module_pages(self.modules, self.maps, {}, self.types)["modul-vektor-gerak.html"]
        levels = payload(page, "MOD")["tka_levels"]
        used = {it["tka"]["tipe"] for st in self.modules["vektor-gerak"]["tahap"] for it in st["soal"] if "tka" in it}
        self.assertEqual(levels, {code: self.types[code]["level"] for code in used})
        self.assertNotIn("TKA_LEVEL", page)

    def test_printable_answers_recompute(self):
        """Every numeric answer in the printable module is re-derived by its content.check()."""
        for src in (ROOT / "print").glob("*/content.py"):
            spec = importlib.util.spec_from_file_location(f"print_{src.parent.name}", src)
            content = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(content)
            self.assertTrue(content.check(), src)

    def test_printable_pdf_is_published_and_linked(self):
        self.assertIsNotNone(build.module_pdf("vektor-gerak"), "print/vektor-gerak.pdf is missing")
        local = build.module_pages(self.modules, self.maps, {}, self.types)["modul-vektor-gerak.html"]
        hosted = build.module_pages(self.modules, self.maps, build.hosted_links(site()), self.types)["modul-vektor-gerak.html"]
        self.assertEqual(payload(local, "MOD")["pdf"], "modul-vektor-gerak.pdf")
        self.assertEqual(payload(hosted, "MOD")["pdf"], f"{build.PAGES_URL}modul-vektor-gerak.pdf")
        self.assertEqual(build.site_files(site())["modul-vektor-gerak.pdf"], build.module_pdf("vektor-gerak").read_bytes())


class HomeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = build.render_site(site(), {})["index.html"]

    def test_home_page_lists_every_subject(self):
        self.assertNotIn("__SUBJECT_CARDS__", self.home)
        self.assertIn('href="peta.html"', self.home)
        for m in site().maps.values():
            self.assertIn(f'href="peta-{m["id"]}.html"', self.home, m["id"])

    def test_home_page_groups_subjects(self):
        self.assertNotIn("<!--__", self.home)
        self.assertNotIn("__N_", self.home)
        self.assertNotIn("/*__HOME__*/", self.home)
        groups = site().groups
        self.assertEqual([g["id"] for g in groups], ["umum", "ipa", "ips", "bahasa", "lanjut"])
        names = {g["id"]: g["name"] for g in groups}
        panels = {g["id"]: self.home.split(f'id="panel-{g["id"]}"')[1].split('class="gpanel"')[0] for g in groups}
        for s in site().subjects:
            card = f'data-sid="{s["id"]}"'
            self.assertIn(card, panels[s["group"]], s["id"])
            self.assertNotIn('<span class="flag">', panels[s["group"]].split(card)[1].split("</a>")[0], s["id"])
            for g in s.get("also", []):
                self.assertIn(card, panels[g], s["id"])
                self.assertIn(f'<span class="flag">{names[s["group"]]}</span>', panels[g].split(card)[1].split("</a>")[0])
        self.assertIn('href="peta-matematika.html?lanjut=1"', panels["lanjut"])
        data = payload(self.home, "HOME")
        self.assertEqual(list(data["subjects"]["matematika-tingkat-lanjut"]["grades"]), ["XI", "XII"])
        self.assertEqual(list(data["subjects"]["fisika"]["grades"]), ["X", "XI", "XII"])

    def test_lanjut_subject_without_tags_is_left_out(self):
        """A Tingkat Lanjut card needs tagged topics in its parent map; without them it would open an empty map."""
        maps = copy(site().maps)
        for d in maps["sejarah"]["domains"]:
            for t in d["topics"]:
                t.pop("lanjut", None)
        _, data = build.home_sections(maps, site().topics, 0, site().tka, site().modules, site().banks,
                                      site().subjects, site().groups)
        self.assertNotIn("sejarah-tingkat-lanjut", data["subjects"])
        self.assertIn("matematika-tingkat-lanjut", data["subjects"])

    def test_subject_pages_link_home(self):
        built = build.render_site(site(), {})
        for name in ["peta.html", "bank.html", "simulasi.html", "tka.html"] + [f"peta-{i}.html" for i in site().maps]:
            self.assertIn('class="home-link" href="index.html"', built[name], name)

    def test_root_index_forwards_to_docs(self):
        page = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('url=docs/', page)


class GeneratedCheckTest(unittest.TestCase):
    """scripts/check_generated.py accepts a good batch and rejects a bad one."""

    def item(self, **kw):
        it = {"id": "FISG-G001", "passage": None, "nomor": "1", "format": "pilihan-ganda",
              "kompetensi": "-", "subkompetensi": None, "indikator": "-",
              "soal": "Sebuah benda bermassa 2 kg didorong gaya 10 N. Berapa percepatannya?",
              "opsi": ["2 m.s⁻²", "5 m.s⁻²", "10 m.s⁻²", "20 m.s⁻²", "0,2 m.s⁻²"], "kunci": 1,
              "status_kunci": "usulan", "keyakinan_kunci": "tinggi", "alasan": "a = F/m = 10/2 = 5 m.s⁻²",
              "halaman": [], "catatan_transkripsi": [], "asal": "generated", "tipe": "FIS-HITUNG",
              "acuan": ["FIS25-012"]}
        it.update(kw)
        return it

    def run_check(self, items):
        bank = {"id": "fisika-test", "kode": "FISG", "mapel": "Fisika", "ujian": "uji",
                "sumber": {"berkas": None, "halaman": 0, "bentuk": "dibuat agen"}, "catatan": [], "teks": [],
                "soal": items}
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "fisika-test.json"
            p.write_text(json.dumps(bank, ensure_ascii=False), encoding="utf-8")
            return check_generated.check(p, check_generated.load_types())

    def test_good_batch_passes(self):
        self.assertEqual(self.run_check([self.item()]), [])

    def test_bad_batch_fails(self):
        problems = self.run_check([self.item(tipe="FIS-NOPE"), self.item(id="FISG-G002", acuan=["BINW25-001"]),
                                   self.item(id="FISG-G003", status_kunci="resmi")])
        text = "\n".join(problems)
        self.assertIn("unknown tipe", text)
        self.assertIn("acuan", text)
        self.assertIn("status_kunci", text)


if __name__ == "__main__":
    unittest.main()
