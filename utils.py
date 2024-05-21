class CrossoverHelper:
    def __init__(self, ITEM_1, ITEM_2, ITEM_3):
        self.ITEM_1 = ITEM_1
        self.ITEM_2 = ITEM_2
        self.ITEM_3 = ITEM_3

    def sort_by_valor_sum(self, individuo):
        sum_value = 0
        sum_value += self.ITEM_1.valor * individuo.item1
        sum_value += self.ITEM_2.valor * individuo.item2
        sum_value += self.ITEM_3.valor * individuo.item3
        return sum_value

    def sort_by_weight_sum(self, individuo):
        return sum(item.peso for item in individuo.itens)

    def select_to_crossover(self, half: list, percentage, worst_half=False):
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
                selected_value = half[1]
            elif difference_first < difference_last:
                selected_value = half[0]
            else:
                selected_value = half[1]

        return selected_value

    def select_gene(self, percentage):
        if percentage < 1 / 3:
            return 1
        elif percentage < 2 / 3:
            return 2
        else:
            return 3

    def swap_genes(self, position, best_selected, worst_selected):
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

    def select_mutation_individuo(self, populacao_list, percentage):
        index = 1 if percentage > 0.50 else 0
        return populacao_list[index]

    # quantidade a ser mutada
    def qntd_to_change_gene(self, index, percentage):
        if index == 1:
            max_qnt = self.ITEM_1.qnt
        elif index == 2:
            max_qnt = self.ITEM_2.qnt
        elif index == 3:
            max_qnt = self.ITEM_3.qnt

        step_size = 1 / (max_qnt + 1)

        # Determine which range the percentage falls into
        for i in range(max_qnt + 1):
            if percentage <= (i + 1) * step_size:
                return i

    def change_gene(self, index, individuo, gene):
        if index == 1:
            individuo.item1 = gene
        elif index == 2:
            individuo.item2 = gene
        elif index == 3:
            individuo.item3 = gene

        return individuo
