from odoo import fields, models, api
from odoo.exceptions import UserError

class TrainingClass(models.Model):
    _name = 'training.class'
    _description = 'Training'

    name = fields.Char(string='Name')
    max_person = fields.Integer(string='Max Person')
    active = fields.Boolean(string='Active', default=True)
    max_duration = fields.Float(string='Max Duration')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Datetime(string='End Date (Datetime)')
    duration_days = fields.Integer(string='Duration in Days', compute='_compute_duration_days')
    mentor_id = fields.Many2one('res.partner', string='Mentor')
    mentor_phone = fields.Char(string='Phone', related='mentor_id.phone')
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], string='Status', default='draft')
    description = fields.Text(string='Description')
    attachment_class = fields.Binary(string='Attachment')
    preview_image = fields.Image(string='Preview')
    tag_ids = fields.Many2many('res.partner.category', string='Tags')
    member_ids = fields.One2many('training.member', 'class_id', string='Peserta')
    class_id = fields.Many2one('master.class', string='Kelas')

    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for rec in self:
            # Hanya eksekusi ketika start date dan end date terisi
            if rec.end_date and rec.start_date:
                value = (rec.end_date.date() - rec.start_date).days
            else:
                value = 0
            rec.duration_days = value
    
    @api.constrains('mentor_id', 'start_date')
    def _check_mentor_start_date(self):
        for rec in self:
            exist_record = self.search([('mentor_id', '=', rec.mentor_id.id), ('start_date', '=', rec.start_date), ('id', '!=', rec.id)])
            if exist_record:
                raise UserError('Tidak boleh menggunakan Mentor yang sama di tanggal start yang sama')
    
    @api.onchange('mentor_id')
    def _onchange_mentor_id(self):
        self.tag_ids = self.mentor_id.category_id
        # new_tags = [(0, 0, {'name': 'Tag New 1'})]
        # new_tags = []
        # new_tags.extend([(1, 0, x.id) for x in self.mentor_id.category_id])
        # new_tags.extend([(1, 0, x.id) for x in self.tag_ids])
        # self.write({'tag_ids': new_tags})

    def set_to_confirmed(self):
        self.state = 'confirmed'
    
    def set_to_draft(self):
        self.state = 'draft'
    
    def unlink(self):
        for rec in self:
            if rec.state == 'confirmed':
                raise UserError('Tidak boleh delete training ketika status sudah confirmed')
        
        # inherit
        res = super(TrainingClass, self).unlink()
        return res

    def action_wizard(self):
        return {
            'name': 'Change Date',
            'res_model': 'wizard.training.class',
            'view_mode': 'form',
            'views': [[False, 'form']],
            'context': {
                'active_model': self._name,
                'active_ids': self.ids,
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }


class TrainingMember(models.Model):
    _name = 'training.member'
    _description = 'Peserta Training'

    peserta_id = fields.Many2one('res.partner', string='Peserta', required=True)
    register_date = fields.Date(string='Tanggal Daftar')
    class_id = fields.Many2one('training.class', string='Class')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends('name', 'phone')
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name} - {rec.phone}"


class MasterClass(models.Model):
    _name = 'master.class'

    name = fields.Char(string='Name')


# TODO: create wizard
