from odoo import models, fields, api
# from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
import re




class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'

    active = fields.Boolean(default=True)
    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    history = fields.Text()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-')],
        string='Blood Type'
    )
    pcr = fields.Boolean()
    image = fields.Binary()
    address = fields.Text()
    email = fields.Char(string='Email')
    age = fields.Integer(compute='_compute_age')

    department_id = fields.Many2one('hms.department', string='Department')
    department_capacity = fields.Integer(string='Department Capacity', related='department_id.capacity', readonly=True)
    # doctor_id = fields.Many2one('hms.doctor', string='Doctor')
    doctor_ids=fields.Many2many('hms.doctor','hms_patient_doctor', 'doctor_id','patient_id')
    log_history = fields.One2many('hms.patient.log', 'patient_id')


    @api.onchange('email')
    def _onchange_valid_email(self):
        if self.email:
            match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
            email = self.env['hms.patient'].search([('email', '=', self.email)])
            if not match:
                raise ValidationError('Not a valid E-mail ID')
            if email:
                raise ValidationError('This email used before')

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                record.age = today.year - record.birth_date.year
            else:
                record.age = 0

    @api.onchange('pcr')
    def _onchange_pcr(self):
        print('self', self)  #
        if self.pcr:
            self.cr_ratio = False
        else:
            self.cr_ratio = None

    @api.onchange('age')
    def _onchange_age(self):
        if self.age and self.age < 30:
            self.pcr = True

        if self.age < 50:
            self.history = False




    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], string='State', default='undetermined')

    # def action_undetermined(self):
    #     print("inside action_undetermined")
    #     self.state = 'undetermined'
    #
    # def action_good(self):
    #     print("inside action_good")
    #     self.state = 'good'
    #
    # def action_fair(self):
    #     print("inside action_fair")
    #     self.state = 'fair'
    #
    # def action_serious(self):
    #     print("inside action_serious")
    #     self.state = 'serious'

    def action_undetermined(self):
        # self.state = 'undetermined'
        self.write({'state': 'undetermined'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Undetermined'
        })

    def action_good(self):
        # self.state = 'good'
        self.write({'state': 'good'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Good'
        })

    def action_fair(self):
        # self.state = 'fair'
        self.write({'state': 'fair'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Fair'
        })

    def action_serious(self):
        # self.state = 'serious'
        self.write({'state': 'serious'})
        self.env['hms.patient.log'].create({
            'patient_id': self.id,
            'description': 'State changed to Serious'
        })

    def action_add_history_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hsm.add.history',
            'view_mode': 'form',
            'view_id': self.env.ref('hms.add_history_form_view').id,
            'target': 'new',
            'context': {'default_patient_id': self.id},
        }

    # def unlink(self):
    #     for record in self:
    #         if self.env['hms.patient.log'].search([('patient_id', '=', record.id)]):
    #             raise UserError("You cannot delete a patient with log entries. Please archive instead.")
    #     return super(Patient, self).unlink()

class PatientLog(models.Model):
    _name = 'hms.patient.log'
    _description = 'Patient Log'

    patient_id = fields.Many2one('hms.patient', string='Patient', required=True)
    description = fields.Text(string='Description')
    created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)

