"""CODEC-3's freeze inherits CODEC-2's rules unchanged: checked, not asserted."""
import hashlib
import json
import unittest
from pathlib import Path

FORECASTS = Path(__file__).resolve().parent.parent / "docs/represent/forecasts"
CODEC2 = FORECASTS / "continuation-codec-2.json"
CODEC3 = FORECASTS / "continuation-codec-3.json"
BANK3 = FORECASTS / "continuation-codec-3-token-bank.json"


class InheritanceTests(unittest.TestCase):
    def setUp(self):
        self.raw2 = CODEC2.read_bytes()
        self.c2 = json.loads(self.raw2)
        self.c3 = json.loads(CODEC3.read_text(encoding="utf-8"))

    def test_the_pinned_codec_2_file_is_the_one_on_disk(self):
        pinned = self.c3["acceptance"]["inherited_from"]["sha256"]
        self.assertEqual(hashlib.sha256(self.raw2).hexdigest(), pinned)

    def test_the_rule_metric_and_positions_are_codec_2s_byte_for_byte(self):
        for key in ("rule", "metric", "scored_positions"):
            self.assertEqual(self.c3["acceptance"][key], self.c2["acceptance"][key], key)
        for key in ("rule", "null", "A_yardstick_usable"):
            self.assertEqual(
                self.c3["acceptance"]["guards"][key], self.c2["acceptance"]["guards"][key], key
            )

    def test_the_bank_named_is_the_bank_committed(self):
        bank = json.loads(BANK3.read_text(encoding="utf-8"))
        self.assertEqual(self.c3["bank"]["ids_sha256_u32le"], bank["ids_sha256_u32le"])
        self.assertEqual(len(bank["ids"]), bank["count"])


if __name__ == "__main__":
    unittest.main()
