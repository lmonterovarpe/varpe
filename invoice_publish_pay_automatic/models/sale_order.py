# Copyright 2020 Raul Carbonell
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _

class SaleOrderPublishPayAutomatic(models.Model):
    _inherit = "sale.order"

    is_external_invoiced = fields.Boolean(string="Facturada", )

    #Al modificar un pedido, si el campo is_external_invoiced se pondra estado factura a facturado
    def write(self, vals):
        res = super(SaleOrderPublishPayAutomatic, self).write(vals)
        if vals.get('is_external_invoiced'):
            if (self.is_external_invoiced==True) and (self.invoice_status!="invoiced"):
                self.invoice_status="invoiced"
