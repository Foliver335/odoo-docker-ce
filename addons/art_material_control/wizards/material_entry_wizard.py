from odoo import models, fields, api
from odoo.exceptions import UserError

class MaterialEntryWizard(models.TransientModel):
    _name = "xipp.material.entry.wizard"
    _description = "Wizard Entrada de Material"

    code = fields.Char("Código de Barras", required=True)
    qty  = fields.Float("Quantidade", required=True, default=1.0)

    @api.onchange('code')
    def _onchange_code(self):
        mat = self.env['xipp.material'].search([('code','=',self.code)], limit=1)
        if not mat:
            raise UserError("Material não encontrado para o código informado.")

    def action_confirm(self):
        mat = self.env['xipp.material'].search([('code','=',self.code)], limit=1)
        self.env['xipp.material.operation'].create({
            'material_id': mat.id,
            'op_type': 'entry',
            'qty': self.qty,
        })
        return {'type': 'ir.actions.act_window_close'}
