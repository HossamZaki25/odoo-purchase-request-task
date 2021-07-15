from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = "purchase.request.rejection"
    rejection_reason = fields.Text(string="Rejection Reason", required=True,)
    def confirm_rejection_reason(self):
        req_id = self.env['purchase.request'].browse(self._context.get('active_id'))
        req_id.rejection_reason = self.rejection_reason
        req_id.state = 'reject'
        return {}


