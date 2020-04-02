from odoo import models, fields


class History(models.Model):
    _name = 'hms.history'

    # name = fields.Char()
    description = fields.Text()
    patient_id = fields.Many2one(comodel_name="hms.patient")

