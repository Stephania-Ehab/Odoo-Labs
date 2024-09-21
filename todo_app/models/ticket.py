from odoo import models, fields



class Ticket(models.Model):
    _name = 'td.ticket'
    _description = 'Ticket'

    name = fields.Char()
    number = fields.Integer()
    tag = fields.Char()
    file = fields.Binary()
    assign_to = fields.Many2one('res.users', string='Assign To')
    description = fields.Char()
    state = fields.Selection([
        ('new', 'New'),
        ('doing', 'Doing'),
        ('done', 'Done')
    ], string="State", default='new')

    def action_new(self):
        print("inside action_new")
        self.state = 'new'

    def action_doing(self):
        print("inside action_doing")
        self.state = 'doing'

    def action_done(self):
        print("inside action_done")
        self.state = 'done'
