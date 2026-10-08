import io
import json
import tempfile
import unittest
from pathlib import Path
from book_research import search_books, save_csv, main

def fake_fetch(req, timeout):
    assert "openlibrary.org/search.json" in req.full_url
    return io.BytesIO(json.dumps({"docs":[{"key":"/works/OL1W","title":"Test Book","author_name":["Researcher"],"first_publish_year":2018},{"key":"/authors/A","title":"Skip"}]}).encode())

class BookResearchTest(unittest.TestCase):
    def test_search(self):
        rows=search_books("democracy",fetcher=fake_fetch)
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["status"],"Unverified")
        self.assertEqual(rows[0]["open_library_url"],"https://openlibrary.org/works/OL1W")
    def test_invalid(self):
        with self.assertRaises(ValueError):
            search_books("democracy",0,fetcher=fake_fetch)
    def test_csv(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/"result.csv"
            save_csv(search_books("democracy",fetcher=fake_fetch),target)
            self.assertIn("Unverified",target.read_text())
    def test_template(self):
        with tempfile.TemporaryDirectory() as folder:
            target=Path(folder)/"claim.csv"
            self.assertEqual(main(["--blank-template",str(target)]),0)
            self.assertIn("supporting_evidence",target.read_text())

if __name__=="__main__":
    unittest.main()
