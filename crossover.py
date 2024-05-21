import random
import sys

from utils import CrossoverHelper


class Item:
    def __init__(self, nome: str, peso: int, valor: float, qnt: int):
        self.nome = nome
        self.peso = peso
        self.valor = valor
        self.qnt = qnt

    def __str__(self) -> str:
        return f"Nome: {self.nome} | Peso: {self.peso} | Valor: {self.valor} | Quantidade: {self.qnt}"


class Individuo:
    def __init__(
        self,
        nome: str,
        item1: int,
        item2: int,
        item3: int,
    ):
        self.nome = nome
        self.item1 = item1
        self.item2 = item2
        self.item3 = item3

    def get_weight(self) -> int:
        weight = 0
        weight += ITEM_1.peso * self.item1
        weight += ITEM_2.peso * self.item2
        weight += ITEM_3.peso * self.item3

        return weight

    def get_value(self) -> int:
        sum_value = 0
        sum_value += ITEM_1.valor * self.item1
        sum_value += ITEM_2.valor * self.item2
        sum_value += ITEM_3.valor * self.item3

        return sum_value

    def __str__(self) -> str:
        return f"Nome: {self.nome} | Item 1: {self.item1} | Item 2: {self.item2} | Item 3: {self.item3} | Valor: {self.get_value()} | Peso: {self.get_weight()}"


# Itens definidos
ITEM_1 = Item(nome="1", peso=3, valor=100, qnt=7)
ITEM_2 = Item(nome="2", peso=6, valor=200, qnt=2)
ITEM_3 = Item(nome="3", peso=4, valor=50, qnt=5)

# População definida
populacao_list = [
    Individuo(nome="1", item1=2, item2=2, item3=4),
    Individuo(nome="2", item1=4, item2=1, item3=3),
    Individuo(nome="3", item1=7, item2=0, item3=2),
    Individuo(nome="4", item1=1, item2=2, item3=4),
]

# Porcentagens originalmente definidas aleatoriamente
OCORRE_MUTACAO = 0.1
SELECIONAR_MELHOR_CROSSOVER = 0.63
SELECIONAR_PIOR_CROSSOVER = 0.27
TIPO_GENE_SELECAO = 0.77
INDIVIDUO_MUTACAO = 0.57
TAXA_MUTACAO = 0.08
GENE_A_SER_MUTADO = 0.45
QNTD_GENE_MUTACAO = 0.58


def init_app():
    helper = CrossoverHelper(ITEM_1, ITEM_2, ITEM_3)
    print("1º Etapa - Criação Indivíduos")
    print()
    print("INDIVÍDUOS")
    for index, individuo in enumerate(populacao_list):
        # print("---------------------------------------------")
        print(individuo)
    print("_____________________________________________")

    """ CLASSIFICAÇÃO
    """
    # Ordenando população baseado no valor somado (quanto maior, mais a cima)
    sorted_populacao = sorted(
        populacao_list, key=helper.sort_by_valor_sum, reverse=True
    )

    print("2º Etapa - Classificação")
    print()
    print("INDIVÍDUOS ORDENADOS POR VALOR")
    for index, individuo in enumerate(sorted_populacao):
        # print("---------------------------------------------")
        print(individuo)
    print("_____________________________________________")

    # Dividindo população pelos melhores e piores (divido por 2)
    midpoint = len(sorted_populacao) // 2
    best_half = sorted_populacao[:midpoint]
    worst_half = sorted_populacao[midpoint:]

    # Definindo o melhor e o pior, baseado na porcentagem definida
    best_selected = helper.select_to_crossover(
        best_half, SELECIONAR_MELHOR_CROSSOVER, worst_half=False
    )
    worst_selected = helper.select_to_crossover(
        worst_half, SELECIONAR_PIOR_CROSSOVER, worst_half=True
    )

    print("3º Etapa - Selecionar indivíduo para crossover")
    print()
    print(f"MELHOR SELECIONADO (porcentagem = {SELECIONAR_MELHOR_CROSSOVER})")
    print(best_selected)

    print(f"PIOR SELECIONADO (porcentagem = {SELECIONAR_PIOR_CROSSOVER})")
    print(worst_selected)
    print("_____________________________________________")

    """ CROSSOVER
    """
    print("4º Etapa - crossover")
    print()
    selected_gene = helper.select_gene(TIPO_GENE_SELECAO)
    print(
        f"ITEM {selected_gene} A SOFRER CROSSOVER (porcentagem = {TIPO_GENE_SELECAO})"
    )
    # Invertendo genes baseado na porcentagem definida.
    best_selected, worst_selected = helper.swap_genes(
        selected_gene, best_selected, worst_selected
    )

    print(f"MELHOR SELECIONADO APÓS CROSSOVER")
    print(best_selected)
    print(f"PIOR SELECIONADO APÓS CROSSOVER")
    print(worst_selected)
    print("_____________________________________________")

    """ MUTAÇÃO
    """
    print("5º Etapa - Mutação")
    print()
    if OCORRE_MUTACAO < TAXA_MUTACAO:
        print("NAO OCORRE MUTACAO")
        sys.exit()

    # Qual sofre mutacao
    individuo_a_ser_mutado = helper.select_mutation_individuo(
        [best_selected, worst_selected], INDIVIDUO_MUTACAO
    )
    print(f"INDIVIDUO A SER MUTADO (porcentagem = {INDIVIDUO_MUTACAO})")
    print(individuo_a_ser_mutado)

    print()
    # Qual gene a ser mutado
    index = helper.select_gene(GENE_A_SER_MUTADO)
    print(f"GENE A SER MUTADO (porcentagem = {INDIVIDUO_MUTACAO})")
    print(f"Item {index}")

    print()
    # Quantidade de genes a ser mutado
    gene_mutado = helper.qntd_to_change_gene(index, QNTD_GENE_MUTACAO)
    print(f"QUANTIDADE DE GENE A SER MUTADO (porcentagem = {QNTD_GENE_MUTACAO})")
    print(gene_mutado)

    print()
    # Modificando o individuo com o gene modificado
    individuo_a_ser_mutado = helper.change_gene(
        index, individuo_a_ser_mutado, gene_mutado
    )
    print(f"INDIVIDUO APÓS MUTAÇÃO")
    print(individuo_a_ser_mutado)
    print("_____________________________________________")

    """ RESULTADO FINAL, COM A MUTAÇÃO FEITA
    """
    print()
    print("INDIVÍDUOS APÓS CROSSOVER")
    for index, individuo in enumerate(populacao_list):
        # print("---------------------------------------------")
        if individuo.nome == individuo_a_ser_mutado.nome:
            populacao_list[index] = individuo_a_ser_mutado
            print(individuo_a_ser_mutado)
        else:
            print(individuo)
    print("_____________________________________________")


if __name__ == "__main__":
    init_app()
