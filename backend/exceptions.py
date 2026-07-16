# erros que a gente criou pra facilitar o tratamento no frontend
# em vez de ficar usando Exception genérico, cada erro tem um nome que já diz o que rolou

class ProdutoNaoEncontradoError(Exception):
    pass

class CategoriaNaoEncontradaError(Exception):
    pass

class EstoqueInsuficienteError(Exception):
    pass

class DadosInvalidosError(Exception):
    pass

class CategoriaDuplicadaError(Exception):
    pass
