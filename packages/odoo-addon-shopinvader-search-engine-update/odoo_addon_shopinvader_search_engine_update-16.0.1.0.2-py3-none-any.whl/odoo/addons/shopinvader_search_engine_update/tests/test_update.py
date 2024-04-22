# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from .common import TestProductBindingUpdateBase


class TestUpdate(TestProductBindingUpdateBase):
    def test_simple_update(self):
        self.product.name = "new name"
        self.assertEqual(self.product_binding.state, "to_recompute")

    def test_update_template(self):
        self.product.product_tmpl_id.name = "new name"
        self.assertEqual(self.product_binding.state, "to_recompute")

    def test_update_on_an_archived_product(self):
        self.product.active = False
        self.product_binding.state = "to_delete"
        self.product.name = "new name"
        self.assertEqual(
            self.product_binding.state,
            "to_delete",
            "The product binding should not be updated if an archived product is updated",
        )

    def test_update_product_translation(self):
        self.product.update_field_translations("name", {"en_US": "nouveau nom"})
        self.assertEqual(self.product_binding.state, "to_recompute")

    def test_update_product_template_translation(self):
        self.product.product_tmpl_id.update_field_translations(
            "name", {"en_US": "nouveau nom"}
        )
        self.assertEqual(self.product_binding.state, "to_recompute")
