from odoo import models, fields, api

class WizardTrainingClass(models.TransientModel):
    _name = 'wizard.training.class'

    start_date = fields.Date('Start Date')
    end_date = fields.Datetime('End Date')

    def action_change_date(self):
        ctx = self._context
        rec_ids = self.env[ctx.get('active_model')].browse(ctx.get('active_ids'))
        rec_ids.write({'start_date': self.start_date, 'end_date': self.end_date})
