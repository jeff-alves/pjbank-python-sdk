#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pjbank.recebimentos import Recebimentos

class Boleto(Recebimentos):
    """docstring for Boleto."""
    def __init__(self, credencial=None, chave=None):
        super().__init__(credencial, chave)

    def automatico(f):
        def wrapper(self, *args, **kwargs):
            if 'c' in kwargs.keys():
                self.credencial = kwargs['c']
            if 'ch' in kwargs.keys():
                self.chave = kwargs['ch']
            kwargs.pop('c')
            kwargs.pop('ch')
            return f(self, *args, **kwargs)
        return wrapper

    def credenciar(self, dados):
        dados.pop('cartao', None)
        return super().credenciar(dados)

    @automatico
    def emitir(self, dados):
        headers = self.headers_content
        response = self._post(['transacoes'], headers, dados)
        return response

    @automatico
    def imprimir(self, ids_boletos, carne=None):
        headers = self.headers_content
        headers.update(self.headers_chave)
        dados = {"pedido_numero": ids_boletos}
        if carne:
            dados.update({"formato": carne})
        response = self._post(['transacoes', 'lotes'], headers, dados)
        return response