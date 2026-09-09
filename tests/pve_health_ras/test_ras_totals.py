"""The persistent hardware-error totals must be parsed per SECTION.

`ras-mc-ctl --summary` prints one block per error class, and a clean machine
still prints every heading — "No Memory errors.", "No PCIe AER errors." and so
on. A parser that greps the whole output for a keyword therefore matches a
HEADING on a healthy node and reports a fault that does not exist, while a
parser that stops at the first section misses a fault that does.

Both directions are asserted here against real output shapes, including a node
that is clean in every class, because a false alarm on the healthy majority is
what gets a hardware alert muted.

The awk programs under test are copied from
roles/pve_health_telemetry/templates/pve-health.sh.j2 and are verified against
that file so the two cannot drift apart silently.
"""

from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "roles/pve_health_telemetry/templates/pve-health.sh.j2"

MEM = (
    '/[Ff]atal on DIMM/ {for (i = 1; i <= NF; i++) if ($i == "errors:") '
    "n += $(i + 1)} END {print n + 0}"
)
MCE = (
    '/^MCE records summary:/ {inblk = 1; next} /^[A-Za-z].*summary:/ '
    "{inblk = 0} inblk && tolower($0) ~ /uncorrected/ {n += $1} END "
    "{print n + 0}"
)
PCIE = (
    '/^PCIe AER events summary:/ {inblk = 1; next} /^[A-Za-z].*summary:/ '
    "{inblk = 0} inblk && tolower($0) ~ /corrected/ {n += $1} END "
    "{print n + 0}"
)

# A node carrying a fatal memory fault and nothing else.
MEMORY_FAULT = """Memory controller events summary:
\tFatal on DIMM Label(s): 'CPU_SrcID#0_MC#1_Chan#0_DIMM#0' location: 1:0:0:-1 errors: 34

No PCIe AER errors.

No ARM processor errors.

No Extlog errors.
"""

# A node carrying uncorrected machine checks and nothing else. Note the MCE
# section is LAST — a parser that stops early never reaches it.
MCE_FAULT = """No Memory errors.

No PCIe AER errors.

No CXL AER uncorrectable errors.

No CXL AER correctable errors.

No Extlog errors.

MCE records summary:
\t3 Uncorrected, software containable error. errors
"""

# Corrected PCIe errors across several descriptions; they must sum.
PCIE_FAULT = """No Memory errors.

PCIe AER events summary:
\t5 Corrected errors: Receiver Error
\t1 Corrected errors: Receiver Error, Bad DLLP
\t1 Corrected errors: Replay Timer Timeout

No ARM processor errors.
"""

# Every heading present, every class clean. The false-positive case.
ALL_CLEAN = """No Memory errors.

No PCIe AER errors.

No ARM processor errors.

No CXL AER uncorrectable errors.

No CXL AER correctable errors.

No Extlog errors.

No Memory failure errors.
"""


def awk(program: str, text: str) -> int:
    out = subprocess.run(
        ["awk", program], input=text, capture_output=True, text=True, check=True
    )
    return int(out.stdout.strip())


class RasTotals(unittest.TestCase):
    def test_memory_fatal_is_summed_from_its_own_line(self) -> None:
        self.assertEqual(awk(MEM, MEMORY_FAULT), 34)

    def test_uncorrected_machine_checks_are_found_in_a_trailing_section(self) -> None:
        self.assertEqual(awk(MCE, MCE_FAULT), 3)

    def test_corrected_pcie_errors_sum_across_descriptions(self) -> None:
        self.assertEqual(awk(PCIE, PCIE_FAULT), 7)

    def test_a_clean_node_reports_zero_in_every_field(self) -> None:
        """The heading 'No PCIe AER errors.' must not read as a fault."""
        for name, program in (("mem", MEM), ("mce", MCE), ("pcie", PCIE)):
            with self.subTest(field=name):
                self.assertEqual(awk(program, ALL_CLEAN), 0)

    def test_one_class_of_fault_does_not_leak_into_another(self) -> None:
        """A memory fault must not inflate the machine-check or PCIe counts."""
        self.assertEqual(awk(MCE, MEMORY_FAULT), 0)
        self.assertEqual(awk(PCIE, MEMORY_FAULT), 0)
        self.assertEqual(awk(MEM, MCE_FAULT), 0)
        self.assertEqual(awk(PCIE, MCE_FAULT), 0)
        self.assertEqual(awk(MEM, PCIE_FAULT), 0)
        self.assertEqual(awk(MCE, PCIE_FAULT), 0)

    def test_the_template_still_contains_these_programs(self) -> None:
        """Guard against the script and this test drifting apart."""
        body = TEMPLATE.read_text(encoding="utf-8")
        squashed = re.sub(r"\s+", " ", body)
        for name, program in (("mem", MEM), ("mce", MCE), ("pcie", PCIE)):
            with self.subTest(field=name):
                self.assertIn(
                    re.sub(r"\s+", " ", program),
                    squashed,
                    f"the {name} parser in the template no longer matches this test",
                )


if __name__ == "__main__":
    unittest.main()
