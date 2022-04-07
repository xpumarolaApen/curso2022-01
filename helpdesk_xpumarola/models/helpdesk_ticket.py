from odoo import fields,models,api

class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    _order = "sequence"

    name = fields.Char()
    description = fields.Text()
    date = fields.Date(help="Date when the ticket was created")
    limit_date = fields.Date(help="Date when the ticket will be closed")
    assigned = fields.Boolean(help="Ticket assigned to someone")
    acctions_todo = fields.Html()
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned to')
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string='Partner')
    
    sequence = fields.Integer()

    state = fields.Selection(
        #[Nuevo,asignado,en_proceso,pendiente,resuelto,cancelado]
        [('nuevo','Nuevo'),
         ('asignado','Asignado'),
         ('en_proceso','En proceso'),
         ('pendiente','Pendiente'),
         ('resuelto','Resuelto'),
         ('cancelado','Cancelado')],
         string='State',
         default='nuevo')

    action_ids = fields.One2many(
        comodel_name='helpdesk.ticket.action',
        inverse_name='ticket_id',
        string='Actions Done')

    tag_ids = fields.Many2many(
        comodel_name='helpdesk.ticket.tag',
        # relation='table_name',
        # column1='col_name',
        # column2='other_col_name',
        string='Tags')         
    
        

    def to_asignado(self):
        self.ensure_one()
        self.state = 'asignado'
    
    def to_en_proceso(self):
        self.write({'state': 'en_proceso'})
    
    def to_pendiente(self):
        for record in self:
            record.state = 'pendiente'
    
    def review_actions(self):
        self.ensure_one()
        self.action_ids.review()

        # actions = self.env['helpdesk.ticket.action'].search([('ticket_id', '=', self.id)])
        # actions.review()
    
    @api.model
    def get_amount_tickets(self):
        # Give amount of ticket for active user
        return self.search_count([('user_id', '=', self.env.user.id)])
