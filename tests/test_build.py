"""Tests for scripts/build.py. Run: python -m unittest discover -s tests"""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import build  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def row(**kw):
    base = {"id": "SNI-01-900", "simpul": "SNI-01", "tingkat": "1", "soal": "Soal uji?", "jawaban": "Jawaban", "catatan": ""}
    base.update(kw)
    return base


class ValidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.topics, cls.rows = build.load()

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


class PagesTest(unittest.TestCase):
    def test_links_resolve_per_target(self):
        topics, rows = build.load()
        qs = [{"id": r["id"], "t": r["simpul"], "lv": int(r["tingkat"]), "q": r["soal"], "a": r["jawaban"], "x": r["catatan"]} for r in rows]
        maps = build.load_maps()
        local = {**build.pages(topics, qs, {}), **build.map_pages(maps, {})}
        hosted = {**build.pages(topics, qs, build.HOSTED_LINKS), **build.map_pages(maps, build.HOSTED_LINKS)}
        self.assertTrue(set(build.ARTIFACT_URLS) <= set(local), "every hosted page must also be built locally")
        for name, body in local.items():
            self.assertNotIn("/*__DATA__*/", body, name)
            for url in build.HOSTED_LINKS.values():
                self.assertNotIn(url, body, f"{name} links to a hosted copy instead of a local file")
        self.assertIn(build.ARTIFACT_URLS["peta.html"], hosted["bank.html"])
        self.assertIn(build.ARTIFACT_URLS["bank.html"], hosted["peta.html"])
        self.assertIn(build.PAGES_URL, hosted["peta-fisika.html"])


class MapsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.maps = build.load_maps()

    def test_there_is_at_least_one_map(self):
        self.assertIn("fisika", self.maps)

    def test_maps_are_valid(self):
        for name, m in self.maps.items():
            self.assertEqual(build.validate_map(name, m), [], name)

    def test_validator_catches_problems(self):
        m = json.loads(json.dumps(self.maps["fisika"]))
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
        m = json.loads(json.dumps(self.maps["fisika"]))
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

    def test_map_pages_render(self):
        pages = build.map_pages(self.maps, {})
        for m in self.maps.values():
            body = pages[f"peta-{m['id']}.html"]
            self.assertNotIn("/*__MAP__*/", body)
            self.assertNotIn("__TITLE__", body)
            self.assertIn(f"<title>{m['title']}</title>", body)


class TkaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.banks = build.load_tka()

    def test_banks_are_valid(self):
        self.assertTrue(self.banks, "data/tka/ has no banks")
        for name, b in self.banks.items():
            self.assertEqual(build.validate_tka(name, b), [], name)

    def test_validator_catches_problems(self):
        name, b = next(iter(self.banks.items()))
        b = json.loads(json.dumps(b))
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
        b = json.loads(json.dumps(b))
        b["soal"][0]["kunci"] = None
        b["soal"][0]["keyakinan_kunci"] = "tinggi"
        self.assertTrue(any("tidak ada" in e for e in build.validate_tka(name, b)))
        b["soal"][0]["keyakinan_kunci"] = "tidak ada"
        self.assertEqual(build.validate_tka(name, b), [])

    def test_tka_page_renders(self):
        topics, rows = build.load()
        built = build.pages(topics, [], {}, build.load_maps(), self.banks)
        page = built["tka.html"]
        self.assertNotIn("/*__TKA__*/", page)
        self.assertIn('class="home-link" href="index.html"', page)
        for b in self.banks.values():
            self.assertIn(b["id"], page)
        self.assertNotIn("</script><", page.split("const BANKS")[1].split(";\n")[0])
        self.assertIn('href="tka.html"', built["index.html"])


class ModulesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = build.load_modules()
        cls.maps = build.load_maps()
        cls.types = build.load_tka_types()

    def test_modules_are_valid(self):
        self.assertIn("vektor-gerak", self.modules)
        for name, mod in self.modules.items():
            self.assertEqual(build.validate_module(name, mod, self.maps, self.types), [], name)
            self.assertEqual(build.lint_module(name, mod), [], name)

    def test_validator_catches_problems(self):
        mod = json.loads(json.dumps(self.modules["vektor-gerak"]))
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
        mod = json.loads(json.dumps(self.modules["vektor-gerak"]))
        it = next(i for st in mod["tahap"] for i in st["soal"] if i.get("tka", {}).get("tipe") == "FIS-ANALISIS")
        it["format"], it["kunci"] = "pilihan-ganda-kompleks", [0]
        errors = build.validate_module("vektor-gerak", mod, self.maps, self.types)
        self.assertTrue(any("not allowed for FIS-ANALISIS" in e for e in errors))

    def test_module_pages_render_and_link(self):
        pages = build.module_pages(self.modules, self.maps, {})
        topics, rows = build.load()
        home = build.pages(topics, [], {}, self.maps, None, self.modules)["index.html"]
        for mod in self.modules.values():
            body = pages[f"modul-{mod['id']}.html"]
            self.assertNotIn("/*__MODULE__*/", body)
            self.assertIn(f"<title>{mod['title']}</title>", body)
            self.assertIn('class="home-link" href="index.html"', body)
            self.assertNotIn("</script><", body.split("const MOD")[1].split(";\n")[0])
            self.assertIn(f'href="modul-{mod["id"]}.html"', home)

    def test_printable_answers_recompute(self):
        """Every numeric answer in the printable module is re-derived by its content.check()."""
        import importlib.util
        for src in (ROOT / "print").glob("*/content.py"):
            spec = importlib.util.spec_from_file_location(f"print_{src.parent.name}", src)
            content = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(content)
            self.assertTrue(content.check(), src)

    def test_printable_pdf_is_published_and_linked(self):
        self.assertIsNotNone(build.module_pdf("vektor-gerak"), "print/vektor-gerak.pdf is missing")
        local = build.module_pages(self.modules, self.maps, {})["modul-vektor-gerak.html"]
        hosted = build.module_pages(self.modules, self.maps, build.HOSTED_LINKS)["modul-vektor-gerak.html"]
        self.assertIn('"pdf": "modul-vektor-gerak.pdf"', local)
        self.assertIn(f'"pdf": "{build.PAGES_URL}modul-vektor-gerak.pdf"', hosted)
        topics, rows = build.load()
        build.build(topics, rows, self.maps, artifact=False)
        self.assertEqual((build.ROOT / "docs/modul-vektor-gerak.pdf").read_bytes(), build.module_pdf("vektor-gerak").read_bytes())


class SiteTest(unittest.TestCase):
    def test_build_writes_site_files(self):
        topics, rows = build.load()
        build.build(topics, rows, build.load_maps(), artifact=False)
        docs = build.ROOT / "docs"
        self.assertTrue((docs / ".nojekyll").exists(), "docs/.nojekyll stops Jekyll from processing the site")
        page = (docs / "404.html").read_text(encoding="utf-8")
        self.assertNotIn("__SITE_BASE__", page)
        self.assertIn(f'href="{build.SITE_BASE}"', page)
        self.assertTrue(build.SITE_BASE.startswith("/") and build.SITE_BASE.endswith("/"))

    def test_home_page_lists_every_subject(self):
        topics, rows = build.load()
        maps = build.load_maps()
        home = build.pages(topics, [], {}, maps)["index.html"]
        self.assertNotIn("__SUBJECT_CARDS__", home)
        self.assertIn('href="peta.html"', home)
        for m in maps.values():
            self.assertIn(f'href="peta-{m["id"]}.html"', home, m["id"])

    def test_subject_pages_link_home(self):
        topics, rows = build.load()
        maps = build.load_maps()
        built = {**build.pages(topics, [], {}, maps), **build.map_pages(maps, {})}
        for name in ["peta.html", "bank.html", "simulasi.html"] + [f"peta-{i}.html" for i in maps]:
            self.assertIn('class="home-link" href="index.html"', built[name], name)

    def test_root_index_forwards_to_docs(self):
        page = (build.ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('url=docs/', page)


if __name__ == "__main__":
    unittest.main()


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
        import tempfile
        sys.path.insert(0, str(ROOT / "scripts"))
        import check_generated
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
