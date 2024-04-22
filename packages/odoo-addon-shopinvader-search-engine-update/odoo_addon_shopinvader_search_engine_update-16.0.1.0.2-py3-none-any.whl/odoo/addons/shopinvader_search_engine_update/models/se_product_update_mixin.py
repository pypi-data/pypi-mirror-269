# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import api, models


class SEProductUpdateMixin(models.AbstractModel):
    _name = "se.product.update.mixin"
    _description = "Search Engine Product Update Mixin"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.get_products().shopinvader_mark_to_update()
        return res

    def write(self, vals):
        needs_update = self.needs_product_update(vals)
        if needs_update:
            products = self.get_products()
        res = super().write(vals)
        if needs_update:
            (products | self.get_products()).shopinvader_mark_to_update()
        return res

    def unlink(self):
        products = self.get_products()
        res = super().unlink()
        products.shopinvader_mark_to_update()
        return res

    def get_products(self):
        raise NotImplementedError

    def needs_product_update(self, vals):
        return True

    def update_field_translations(self, field_name, translations):
        res = super().update_field_translations(field_name, translations)
        self.get_products().shopinvader_mark_to_update()
        return res
