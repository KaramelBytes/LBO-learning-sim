"""Regression checks for classroom scenarios and interactive assumption changes."""
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")


class BridgeTests(unittest.TestCase):
    def app(self, **query):
        app = AppTest.from_file(APP)
        app.query_params.update({
            k: [str(item) for item in v] if isinstance(v, list) else str(v)
            for k, v in query.items()
        })
        app.run()
        self.assertFalse(list(app.exception))
        return app

    def metrics(self, app):
        self.assertFalse(list(app.exception))
        return {metric.label: metric.value for metric in app.metric}

    def test_presets(self):
        app = self.app()
        cases = {
            "Growth Story": ("$500", "$1,200", "2.40x", "19.1%"),
            "Multiple Expansion": ("$400", "$900", "2.25x", "17.6%"),
            "Debt Paydown": ("$300", "$650", "2.17x", "16.7%"),
            "Distressed": ("$400", "$10", "0.03x", "-52.2%"),
            "All Engines": ("$500", "$1,380", "2.76x", "22.5%"),
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                app.button(key=f"preset_{name}").click().run()
                self.assertEqual(tuple(self.metrics(app).values()), expected)
                self.assertTrue(any("Discuss:" in item.value for item in app.info))
                self.assertTrue(any("arithmetic reconciles" in x.value for x in app.success))

    def test_shared_inputs_allow_edits_presets_and_reset(self):
        app = self.app(exit_ebitda=150)
        self.assertEqual(app.number_input(key="exit_ebitda").value, 150)
        app.number_input(key="exit_ebitda").set_value(180).run()
        self.assertEqual(app.number_input(key="exit_ebitda").value, 180)
        app.button(key="preset_Distressed").click().run()
        self.assertEqual(self.metrics(app)["Exit Equity"], "$10")
        next(x for x in app.button if x.label == "Reset to Defaults").click().run()
        self.assertEqual(app.number_input(key="exit_ebitda").value, 130)

    def test_share_link_round_trip(self):
        app = self.app()
        app.number_input(key="exit_ebitda").set_value(145).run()
        next(x for x in app.button if "Copy Shareable Link" in x.label).click().run()
        shared = self.app(**app.query_params)
        self.assertEqual(self.metrics(shared), self.metrics(app))
        shared.number_input(key="exit_ebitda").set_value(155).run()
        self.assertEqual(shared.number_input(key="exit_ebitda").value, 155)

    def test_loss_and_zero_proceeds(self):
        app = self.app(exit_ebitda=35, exit_multiple=10, debt_paydown=150)
        self.assertEqual(self.metrics(app)["IRR"], "-100.0%")
        app.number_input(key="exit_ebitda").set_value(20).run()
        self.assertEqual(self.metrics(app)["MOIC"], "-0.30x")
        self.assertEqual(self.metrics(app)["IRR"], "N/M")
        self.assertTrue(any("sale proceeds" in x.value for x in app.warning))
        app.number_input(key="initial_debt").set_value(1000).run()
        self.assertEqual(self.metrics(app)["MOIC"], "N/M")

    def test_signed_and_undefined_contributions(self):
        app = self.app()
        app.button(key="preset_Distressed").click().run()
        table = app.dataframe[0].value.set_index("Metric")["Value"]
        self.assertEqual(table["EBITDA Growth Contribution"], "-77%")
        self.assertEqual(table["Interaction Contribution"], "+15%")
        app = self.app(exit_ebitda=100, exit_multiple=9, debt_paydown=100)
        table = app.dataframe[0].value
        contributions = table[table["Metric"].str.endswith("Contribution")]
        self.assertEqual(set(contributions["Value"]), {"N/M"})

    def test_worked_tables_preserve_decimal_inputs(self):
        app = self.app(entry_multiple=10.25, holding_period_years=5.25)
        worked = next(x.value for x in app.markdown if "**With your numbers:**" in x.value)
        self.assertIn("10.25x", worked)
        rows = [line for line in worked.splitlines() if line.startswith("|")]
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(line.count("|") == 4 for line in rows))
        self.assertTrue(any("5.25" in x.value for x in app.markdown if "IRR =" in x.value))

    def test_invalid_shared_values_and_negative_multiple(self):
        for value in ("nan", "inf", "bad"):
            with self.subTest(value=value):
                app = self.app(entry_ebitda=value, holding_period_years=0)
                self.assertEqual(app.number_input(key="entry_ebitda").value, 100)
                self.assertEqual(app.number_input(key="holding_period_years").value, 5)
        app = self.app(entry_multiple=-1)
        self.assertTrue(any("Multiples cannot be negative" in x.value for x in app.error))
        self.assertEqual(len(app.metric), 0)


if __name__ == "__main__":
    unittest.main()
