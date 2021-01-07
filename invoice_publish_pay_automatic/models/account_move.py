# Copyright 2020 Raul Carbonell
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _

class AccountMovePublishPayAutomatic(models.Model):
    _inherit = "account.move"

    #Campos para indicar externamente si la factura está publicada y/o pagada
    is_external_published = fields.Boolean(string="Publicada", )

    is_external_paid = fields.Boolean(string="Pagada", )

    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled')
        ], string='Status', required=True, readonly=True, copy=False, tracking=False,
        default='draft')

    invoice_payment_state = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid')],
        string='Payment', store=True, readonly=True, copy=False, tracking=False,
        compute='_compute_amount')


    def _get_creation_message(self):
        # OVERRIDE
        if not self.is_invoice(include_receipts=True):
            return super()._get_creation_message()
        return {
            'out_invoice': _(''),
            'out_refund': _(''),
            'in_invoice': _(''),
            'in_refund': _(''),
            'out_receipt': _(''),
            'in_receipt': _(''),
        }[self.type]



    #Al modificar una factura, si el campo is_external_published se publicará
    #Al modificar una factura, si el campo is_external_paid se pagará
    def write(self, vals):
        res = super(AccountMovePublishPayAutomatic, self).write(vals)
        if vals.get('is_external_published'):
            if (self.is_external_published==True) and (self.state!="posted"):
                self.post()

        if vals.get('is_external_paid'):
            if (self.is_external_paid==True) and (self.invoice_payment_state!="paid"):
                self.invoice_payment_state="paid"
