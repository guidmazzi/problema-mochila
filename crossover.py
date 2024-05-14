import random
import sys

OCORRE_MUTACAO = 0.1
SELECIONAR_MELHOR_CROSSOVER = 0.63
SELECIONAR_PIOR_CROSSOVER = 0.27
TIPO_GENE_SELECAO = 0.77
INDIVIDUO_MUTACAO = 0.57
TAXA_MUTACAO = 0.8


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
        for item in self.itens:
            weight += item.peso

        return weight

    def get_value(self) -> int:
        sum_value = 0
        sum_value += ITEM_1.valor * self.item1
        sum_value += ITEM_2.valor * self.item2
        sum_value += ITEM_3.valor * self.item3

        return sum_value

    def __str__(self) -> str:
        return f"Nome: {self.nome} | Item 1: {self.item1} | Item 2: {self.item2} | Item 3: {self.item3}"


ITEM_1 = Item(nome="1", peso=3, valor=100, qnt=7)
ITEM_2 = Item(nome="2", peso=6, valor=200, qnt=2)
ITEM_3 = Item(nome="3", peso=4, valor=50, qnt=5)


populacao_list = [
    Individuo(nome="1", item1=2, item2=2, item3=4),
    Individuo(nome="2", item1=4, item2=1, item3=3),
    Individuo(nome="3", item1=7, item2=0, item3=2),
    Individuo(nome="4", item1=1, item2=2, item3=4),
]

# print(populacao_list[3].get_weight())
# print(populacao_list[3].get_value())


def sort_by_valor_sum(individuo):
    sum_value = 0
    sum_value += ITEM_1.valor * individuo.item1
    sum_value += ITEM_2.valor * individuo.item2
    sum_value += ITEM_3.valor * individuo.item3
    return sum_value


def sort_by_weight_sum(individuo):
    return sum(item.peso for item in individuo.itens)


""" CLASSIFICAÇÃO
"""
sorted_populacao = sorted(populacao_list, key=sort_by_valor_sum, reverse=True)

midpoint = len(sorted_populacao) // 2
best_half = sorted_populacao[:midpoint]
worst_half = sorted_populacao[midpoint:]


def select_to_crossover(half: list, percentage, worst_half=False):
    sum_value = half[0].get_value() + half[1].get_value()
    likely_first = half[0].get_value() / sum_value
    likely_last = half[1].get_value() / sum_value

    difference_first = abs(likely_first - percentage)
    difference_last = abs(likely_last - percentage)

    if worst_half:
        if likely_first == 0.5:
            selected_value = half[0]
        elif difference_first < difference_last:
            selected_value = half[1]
        else:
            selected_value = half[0]
    else:
        if likely_first == 0.5:
            selected_value = half[0]  # ERRADO, era pra ser 1 ao inves de 0
        elif difference_first < difference_last:
            selected_value = half[0]
        else:
            selected_value = half[1]

    return selected_value


best_selected = select_to_crossover(
    best_half, SELECIONAR_MELHOR_CROSSOVER, worst_half=False
)
worst_selected = select_to_crossover(
    worst_half, SELECIONAR_PIOR_CROSSOVER, worst_half=True
)

""" CROSSOVER
"""


def select_gene_crossover(percentage):
    if percentage < 1 / 3:
        return 1
    elif percentage < 2 / 3:
        return 2
    else:
        return 3


def swap_genes(position, best_selected, worst_selected):
    if position == 1:
        best_item = best_selected.item1
        worst_item = worst_selected.item1
        best_selected.item1 = worst_item
        worst_selected.item1 = best_item
    elif position == 2:
        best_item = best_selected.item2
        worst_item = worst_selected.item2
        best_selected.item2 = worst_item
        worst_selected.item2 = best_item
    else:
        best_item = best_selected.item3
        worst_item = worst_selected.item3
        best_selected.item3 = worst_item
        worst_selected.item3 = best_item

    return best_selected, worst_selected


crossover_result = swap_genes(
    select_gene_crossover(TIPO_GENE_SELECAO), best_selected, worst_selected
)

for i in crossover_result:
    print(i)

""" Mutação
"""
if OCORRE_MUTACAO < TAXA_MUTACAO:
    print("NAO OCORRE MUTACAO")
    sys.exit()

# qual sofre mutacao


# quak gene a ser mutado

# quantidade a ser mutada

""" RESULTADO FINAL, COM A MUTAÇÃO FEITA
"""
