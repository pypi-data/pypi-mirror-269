# Copyright 2020 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo_test_helper import FakeModelLoader

from odoo.tests import SavepointCase


class TestExcludeLocation(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestExcludeLocation, cls).setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()
        from .common import ResPartner

        cls.loader.update_registry((ResPartner,))

        cls.fake = cls.env["res.partner"].create({"name": "name"})
        cls.location_shop = cls.env.ref("stock.stock_location_stock")
        vals = {"location_id": cls.location_shop.id, "name": "Sub Location 1"}
        cls.sub_location_1 = cls.env["stock.location"].create(vals)
        cls.sub_location_1._parent_store_compute()
        cls.product = cls.env.ref("product.product_product_4")

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super(TestExcludeLocation, cls).tearDownClass()

    def _add_stock_to_product(self, product, location, qty):
        """
        Set the stock quantity of the product
        :param product: product.product recordset
        :param qty: float
        """
        self.env["stock.quant"].with_context(inventory_mode=True).create(
            {
                "product_id": product.id,
                "location_id": location.id,
                "inventory_quantity": qty,
            }
        )

    def test_exclude_location(self):
        # Add different levels of stock for product as :
        # Shop 0: 50.0
        # Sub Level (Shop 0 / Sub Location 1): 25.0
        # Query product stock availability normally and with excluded
        # location as Sub Location 1
        self._add_stock_to_product(self.product, self.location_shop, 50.0)
        self._add_stock_to_product(self.product, self.sub_location_1, 25.0)
        self.fake.stock_excluded_location_ids = self.sub_location_1
        qty = self.product.with_context(
            excluded_location_ids=self.fake.stock_excluded_location_ids
        ).qty_available
        self.assertEqual(50.0, qty)
        self.product.invalidate_cache()
        qty = self.product.qty_available
        self.assertEqual(75.0, qty)
