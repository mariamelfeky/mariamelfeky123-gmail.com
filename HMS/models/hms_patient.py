from odoo import models, fields, api
from odoo.exceptions import UserError
import re
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class Patient(models.Model):
    _name = 'hms.patient'

    first_name = fields.Char(required="True")
    last_name = fields.Char(required="True")
    Birth_date = fields.Date()
    email = fields.Char()
    history = fields.Html()
    PCR = fields.Boolean(default='False')
    CR_ratio = fields.Float()
    blood_type = fields.Selection([
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('O+', 'O+'),
        ('AB', 'AB'),
        ('A-', 'A-'),
        ('B-', 'B-'),
        ('O-', 'O-')
    ])
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute="_compute_age")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default="undetermined")
    department_id = fields.Many2one(comodel_name="hms.department")
    dept_capacity = fields.Integer(related="department_id.capacity")
    doctor_ids = fields.Many2many("hms.doctor")
    created_by = fields.One2many(comodel_name="hms.history", inverse_name="create_uid")
    description = fields.Text(related="created_by.description")
    # related_patient_id = fields.Integer(comodel-name="crm.")

    @api.multi
    @api.depends('Birth_date')
    def _compute_age(self):
        for rec in self:
            age = relativedelta(datetime.now().date(), fields.Datetime.from_string(rec.Birth_date)).years
            rec.age = age

    age
    @api.multi
    def action_approve(self):
        for record in self:
            record.state = "approve"

    @api.constrains('age')
    def onchange_age(self):
        for record in self:
            if record.age < 30:
                record.PCR = True
                return {
                    "warning": {
                                 "title": "PCR Change",
                                 "message": "PCR field id checked"
                             }
                         }


    @api.constrains('email')
    def check_email(self):
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        if not (re.search(regex, self.email)):
            raise UserError('Not valid Email, Enter your email again')

    _sql_constrains = [
        ("Valid Email", "UNIQUE(email)", "The email you entered already exists")
    ]



#
# class patient_customer(models.Model):
#     _name = 'hms.pationt_customer'
#     _inherit = 'crm'






