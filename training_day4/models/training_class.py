from odoo import fields, models, api
from odoo.exceptions import UserError


class TrainingClass(models.Model):
    _inherit = 'training.class'

    name_seq = fields.Char(string='Number')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            # create sequence on save
            vals['name_seq'] = self.env['ir.sequence'].next_by_code(
                'training.class')

        return super().create(vals_list)

    def set_to_confirmed(self):
        res = super().set_to_confirmed()
        if not self.name_seq:
            self.name_seq = self.env['ir.sequence'].next_by_code(
                'training.class')
        return res

    def action_view_member_ids(self):
        action = self.env['ir.actions.act_window']._for_xml_id(
            'training_day4.training_member_action')
        action["domain"] = [("class_id", "=", self.id)]
        return action
