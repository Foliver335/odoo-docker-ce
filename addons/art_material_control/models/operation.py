from odoo import models, fields, api, _
from odoo.exceptions import UserError

class MaterialOperation(models.Model):
    _name = "xipp.material.operation"
    _description = "Operação de Entrada/Saída de Material"
    _order = "date desc"

    material_id = fields.Many2one("xipp.material", "Material", required=True, ondelete="cascade")
    date        = fields.Datetime("Data", default=fields.Datetime.now, readonly=True)
    op_type     = fields.Selection([('entry','Entrada'),('exit','Saída')], "Tipo", required=True)
    qty         = fields.Float("Quantidade", required=True)
    user_id     = fields.Many2one("res.users", "Responsável", default=lambda self: self.env.user, readonly=True)

    @api.constrains("qty")
    def _check_qty(self):
        for op in self:
            if op.qty <= 0:
                raise UserError(_("A quantidade deve ser maior que zero."))

    @api.model
    def create(self, vals):
        op = super().create(vals)
        mat = op.material_id
        if op.op_type == 'entry':
            mat.quantity += op.qty
        else:
            if mat.quantity < op.qty:
                raise UserError(_("Estoque insuficiente para operação."))
            mat.quantity -= op.qty
        return op
