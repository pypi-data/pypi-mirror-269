# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def write(self, vals):
        res = super().write(vals)
        self.shopinvader_mark_to_update()
        return res

    def update_field_translations(self, field_name, translations):
        res = super().update_field_translations(field_name, translations)
        self.shopinvader_mark_to_update()
        return res
