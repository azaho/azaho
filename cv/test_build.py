import sys
import unittest
from pathlib import Path
from types import SimpleNamespace


CV_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CV_DIR))

import build  # noqa: E402


class BuildCvTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = build.load_data(CV_DIR / "cv.json")

    def render(self, *, include_all: bool = False, include=(), exclude=()) -> str:
        args = SimpleNamespace(
            all=include_all,
            include=set(include),
            exclude=set(exclude),
        )
        return build.render_document(self.data, args)

    def test_default_matches_february_2026_selection(self) -> None:
        rendered = self.render()
        self.assertIn("Member of Technical Staff", rendered)
        self.assertIn("Merge Labs", rendered)
        self.assertIn(
            "Master of Engineering in Computer Science and Brain and Cognitive Sciences "
            "[GPA: 5.0/5.0]",
            rendered,
        )
        self.assertIn("CONFERENCE POSTER PRESENTATIONS", rendered)
        self.assertIn("Elected Full Member", rendered)
        self.assertIn("Sigma Xi, The Scientific Research Honor Society", rendered)
        self.assertIn(
            "{\\small\n\\begin{tabularx}{\\textwidth}{@{}Xr@{}}",
            rendered,
        )
        self.assertIn("Chau, G.*", rendered)
        self.assertIn("Gross, E.", rendered)
        self.assertIn("Brady, A.", rendered)
        self.assertIn("(2025, arXiv)", rendered)
        self.assertNotIn("under review at NeurIPS", rendered)
        self.assertNotIn("Stankovits, B.*", rendered)
        self.assertNotIn("RazeMC", rendered)
        self.assertNotIn("PROMYS Europe", rendered)
        self.assertNotIn("\\section{SKILLS}", rendered)

    def test_all_includes_older_optional_material(self) -> None:
        rendered = self.render(include_all=True)
        self.assertIn("RazeMC", rendered)
        self.assertIn("PROMYS Europe", rendered)
        self.assertIn("Taras Shevchenko", rendered)
        self.assertIn("\\section{SKILLS}", rendered)

    def test_single_optional_item_can_be_selected(self) -> None:
        rendered = self.render(include=("promys-europe",))
        self.assertIn("PROMYS Europe", rendered)
        self.assertNotIn("RazeMC", rendered)

    def test_exclusion_overrides_default(self) -> None:
        rendered = self.render(exclude=("tedxmit-speaker-engagement",))
        self.assertNotIn("Speaker Engagement Chair", rendered)

    def test_plain_text_is_latex_escaped(self) -> None:
        self.assertEqual(build.latex_escape("R&D_100%"), r"R\&D\_100\%")

    def test_meng_graduation_details(self) -> None:
        education = next(section for section in self.data["sections"] if section["id"] == "education")
        meng = next(item for item in education["items"] if item["id"] == "mit-meng")
        self.assertEqual(meng["date"], "February 2026")
        self.assertEqual(meng["location"], "Cambridge, MA, USA")
        self.assertIn("[GPA: 5.0/5.0]", meng["subtitle"])

    def test_public_contact_line_omits_phone_and_mailto(self) -> None:
        rendered = self.render()
        self.assertIn("zaho [at] mit [dot] edu", rendered)
        self.assertNotIn("617", rendered)
        self.assertNotIn("mailto:", rendered)


if __name__ == "__main__":
    unittest.main()
