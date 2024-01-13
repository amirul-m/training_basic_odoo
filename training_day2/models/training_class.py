from odoo import fields, models, api

class TrainingClass(models.Model):
    _name = 'training.class'

    name = fields.Char(string='Name')
    max_person = fields.Integer(string='Max Person')
    active = fields.Boolean(string='Active', default=True)
    max_duration = fields.Float(string='Max Duration')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Datetime(string='End Date (Datetime)', required=True)
    duration_days = fields.Integer(string='Duration in Days', compute='_compute_duration_days')
    mentor_id = fields.Many2one('res.partner', string='Mentor')
    mentor_phone = fields.Char(string='Phone', related='mentor_id.phone')
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], string='Status', default='draft')
    description = fields.Text(string='Description')
    attachment_class = fields.Binary(string='Attachment')
    preview_image = fields.Image(string='Preview')
    tag_ids = fields.Many2many('res.partner.category', string='Tags')
    member_ids = fields.One2many('training.member', 'class_id', string='Peserta')

    @api.depends('start_date', 'end_date')
    def _compute_duration_days(self):
        for rec in self:
            # Hanya eksekusi ketika start date dan end date terisi
            if rec.end_date and rec.start_date:
                value = (rec.end_date.date() - rec.start_date).days
            else:
                value = 0
            rec.duration_days = value


class TrainingMember(models.Model):
    _name = 'training.member'

    peserta_id = fields.Many2one('res.partner', string='Peserta', required=True)
    register_date = fields.Date(string='Tanggal Daftar')
    class_id = fields.Many2one('training.class', string='Class')
