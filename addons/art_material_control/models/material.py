from odoo import models, fields, api

class Material(models.Model):
    _name = "xipp.material"
    _description = "Material de Depósito"
    _order = "name"

    name        = fields.Char("Nome", required=True)
    code        = fields.Char("Código de Barras", required=True, copy=False, index=True)
    uom_id      = fields.Many2one("uom.uom", "Unidade de Medida", default=lambda self: self.env.ref('uom.product_uom_unit'))
    quantity    = fields.Float("Quantidade em Estoque", default=0.0, readonly=True)
    description = fields.Text("Descrição")
    expiry_date = fields.Date("Validade")

    _sql_constraints = [
        ("code_unique", "unique(code)", "Já existe um material com este código!"),
    ]

    @api.model
    def create(self, vals):
        # inicializa tabela se necessário
        material = super().create(vals)
        return material
