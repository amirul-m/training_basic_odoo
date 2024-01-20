from odoo import fields, models, api
from datetime import datetime as dt
from odoo.exceptions import UserError


class TrainingClassExtension(models.Model):
    _name = 'training.class'
    _inherit = ['training.class', 'mail.thread', 'mail.activity.mixin']

    name = fields.Char(required=True, tracking=True)
    state = fields.Selection(tracking=True)
    description2 = fields.Text(string='Description 2')
    tag_ids = fields.Many2many(tracking=True)
    member_ids = fields.One2many(tracking=True)

    def set_to_confirmed(self):
        # tambahkan sebelum super. tambahkan validasi apakah sudah status confirm. jika sudah raise dan tidak dilanjutkan
        if self.state == 'confirmed':
            raise UserError('Dokumen sudah dikonfirmasi. Silahkan direfresh')
        
        res = super(TrainingClassExtension, self).set_to_confirmed()
        
        # tambahkan setelah super. write desctiption2
        self.description2 = f'Dikonfirmasi pada tanggal {fields.Datetime.now()}'
        return res


class TrainingClassClassical(models.Model):
    _name = 'training.class.classical'
    _inherit = 'training.class'
    
    description3 = fields.Text(string='Description 3')


class TrainingClassDelegation(models.Model):
    _name = "training.class.delegation"
    _inherits = {'training.class': 'training_id'}

    training_id = fields.Many2one('training.class', string='Training', ondelete='restrict', auto_join=True, index=True)
    description4 = fields.Text(string='Description 4')

    # TODO: not work
    @api.model_create_multi
    def create(self, vals):
        for rec in self:
            training_id = self.env['training.class'].create({'name': rec.name})
            vals['training_id'] = training_id.id
        
        res = super(TrainingClassDelegation, self).create(vals)
        return res
