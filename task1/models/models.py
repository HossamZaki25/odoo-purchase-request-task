# -*- coding: utf-8 -*-

from odoo import models, fields, api



class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Char(string="Description", compute = "get_product_name")
    quantity = fields.Float(string="Quantity", default=1)
    cost_price = fields.Float(string="Cost Price", readonly=True, compute = "get_product_price" )
    sub_total = fields.Float(string="Total", readonly=True, compute = "compute_subtotal")
    request_id = fields.Many2one('purchase.request')

    @api.depends('quantity','cost_price')
    def compute_subtotal(self):
        for rec in self:
            rec.sub_total = rec.quantity * rec.cost_price

    @api.depends('product_id')
    def get_product_name(self):
        for rec in self:
            rec.description = rec.product_id.name

    @api.depends('product_id')
    def get_product_price(self):
        for rec in self:
            rec.cost_price = rec.product_id.lst_price

class PurchaseRequest(models.Model):
    _name = 'purchase.request'

    name = fields.Char(string="Request Name", required=True)
    requested_by = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.uid, required=True)
    # requested_by = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.user.id)
    start_date = fields.Date(string="Start Date", default= fields.Date.today)
    end_date = fields.Date(string="End Date")
    rejection_reason = fields.Text(readonly=True, string="Rejection Reason") # will appear in reject state only
    order_line = fields.One2many('purchase.request.line', 'request_id')
    total_price = fields.Float(string="Total Price", default=0, readonly=True, compute="compute_total_price")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('to_be_approved', 'To Be Approved'),
        ('approve','Approve'),
        ('reject','Reject'),
        ('cancel','Cancel')], default='draft')

    @api.depends('order_line.sub_total')
    def compute_total_price(self):
        for rec in self:
            if rec.order_line:
                for line in rec.order_line:
                    rec.total_price += line.sub_total
            else:
                rec.total_price = 0


    def submit_for_approval_action(self):
        self.state = 'to_be_approved'
    # def approve_action(self):
    #     self.state = 'approve'
    # def reject_action(self):
    #     self.state = 'reject'
    def reset_to_draft_action(self):
        self.state = 'draft'
    def cancel_action(self):
        self.state = 'cancel'

    def open_rejection_reason_wizard(self):
        return {
            'name':" Rejection Reason",
            'res_model': 'purchase.request.rejection',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target':'new',
            'domain':[],
            'view_id':False,
        }

    def approve_action(self):
        template_id = self.env.ref('task1.request_approved_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)
        self.state = 'approve'

    def get_emails_of_purchase_manager_group_members(self):
        user_group = self.env.ref("base.purchase_group_manager")
        email_list = [usr.login for usr in user_group.users if usr.login]
        return ",".join(email_list)