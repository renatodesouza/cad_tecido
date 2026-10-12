from django.db import models

<<<<<<< HEAD
class Representante(models.Model):
    nome = models.CharField(max_length=30, verbose_name='Nome')
    email = models.EmailField('E-mail')
    telefone = models.CharField(max_length=40)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = 'Representante'
        verbose_name_plural = 'Representantes'


class Fornecedor(models.Model):
    nome_empresa = models.CharField(max_length=150, verbose_name='Empresa')
    representante = models.ForeignKey(Representante, on_delete=models.PROTECT, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, verbose_name='Telefone/WhatsApp')
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')
    cnpj = models.CharField(max_length=20, blank=True, null=True, verbose_name='CNPJ')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome_empresa']

    def __str__(self):
        return self.nome_emrpesa

class PedidoCompra(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.PROTECT, verbose_name='Fornecedor')
    numero_pedido = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nº do Pedido / NF')
    data_compra = models.DateField(verbose_name='Data da Compra')
    data_previsao_entrega = models.DateField(blank=True, null=True, verbose_name='Previsão de Entrega')
    observacoes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Pedido de Compra'
        verbose_name_plural = 'Pedidos de Compra'

    def __str__(self):
        return (f'Pedido {self.numero_pedido or self.id} - {self.fornecedor.nome_emrpesa}')


class Tecido(models.Model):
    UNIDADE_MEDIDA_CHOICES = [
        ('MT', 'Metro (mt)'),
        ('KG', 'Quilograma (kg)')
    ]

    pedido = models.ForeignKey(PedidoCompra, on_delete=models.CASCADE, related_name='itens', verbose_name='Pedido de Origem')
    nome = models.CharField(max_length=150, verbose_name='Nome/Artigo do Tecido')
    cor = models.CharField(max_length=100, verbose_name='Cor Específica')
    unidade_medida = models.CharField(max_length=2, choices=UNIDADE_MEDIDA_CHOICES, default='MT', verbose_name='Unidade de Medida')
    quantidade_comprada = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Quantidade Comprada')
    rendimento = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Rendimento (mt/kg)')
    preco_total_item = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Total do Item')
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações do Lote')

    class Meta:
        verbose_name = 'Item do Pedido (tecido/Cor)'
        verbose_name_plural = 'Itens do Pedido (Tecidos/Cores)'

    def save(self, *args, **kwargs):
        if (self.preco_total_item and self.quantidade_comprada and self.quantidade_comprada > 0):
            self.preco_unitario = self.preco_total_item / self.quantidade_comprada 
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome} - Cor: {self.cor} ({self.quantidade_comprada} {self.unidade_medida})'

