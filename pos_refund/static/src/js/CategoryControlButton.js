    odoo.define('pos_refund.CategoryControlButton', function (require) {
   'use strict';
  const { Gui } = require('point_of_sale.Gui');
  const PosComponent = require('point_of_sale.PosComponent');
  const { identifyError } = require('point_of_sale.utils');
  const ProductScreen = require('point_of_sale.ProductScreen');
  const { useListener } = require("@web/core/utils/hooks");
  const Registries = require('point_of_sale.Registries');
  const PaymentScreen = require('point_of_sale.PaymentScreen');
  class CategoryControlButton extends PosComponent {
   setup() {
       super.setup();
       useListener('click', this.onClick);
   }
  async onClick() {
    var self = this;
    await this.rpc({
                   model: 'product.category',
                    method: 'search_read',
                    args: [[], ['name', 'property_cost_method', 'property_valuation']],
            }).then(function (result) {
                 self.showScreen('CategoryScreen', {
                    categories: result,
                });
            });
    }
}
  CategoryControlButton.template = 'CategoryControlButton';
  ProductScreen.addControlButton({
      component: CategoryControlButton,
      condition: function() {
          return true;
      },
  });
  Registries.Component.add(CategoryControlButton);
  return CategoryControlButton;
});