from random import shuffle


class CSP:
    def __init__(self, variables, domains, neighbours, constraints):
        self.variables = variables
        self.domains = domains
        self.neighbours = neighbours
        self.constraints = constraints

    def backtracking_search(self):
        return self.recursive_backtracking({})

    def recursive_backtracking(self, assignment): # implement SE EXERCISE
        if self.is_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            if self.is_consistent(var, value, assignment):
                assignment[var] = value
                result = self.recursive_backtracking(assignment)
                if result is not None:
                    return result
                assignment[var] = None
        return None

    def select_unassigned_variable(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return variable

    def is_complete(self, assignment):
        for variable in self.variables:
            if variable not in assignment:
                return False
        return True

    def order_domain_values(self, variable, assignment):
        all_values = self.domains[variable][:]
        # shuffle(all_values)
        return all_values

    def is_consistent(self, variable, value, assignment):
        if not assignment:
            return True

        for constraint in self.constraints.values():
            for neighbour in self.neighbours[variable]:
                if neighbour not in assignment:
                    continue

                neighbour_value = assignment[neighbour]
                if not constraint(variable, value, neighbour, neighbour_value):
                    return False
        return True


def create_southamerica_csp():
    costarica, panama, colombia, venezuela, ecuador, peru, guyana, suriname, guyane, brasil, bolivia, paraguay, chile, uruguay, argentina = 'Costarica', 'Panama', 'Colombia', 'Venezuela', 'Ecuador', 'Peru', 'Guyana', 'Suriname', 'Guyane', 'Brasil', 'Bolivia', 'Paraguay', 'Chile', 'Uruguay', 'Argentina'
    values = ['Red', 'Green', 'Blue', 'Yellow']
    variables = [costarica, panama, colombia, venezuela, ecuador, peru, guyana, suriname, guyane, brasil, bolivia, paraguay, chile, uruguay, argentina]
    domains = {
        costarica: values[:],
        panama: values[:],
        colombia: values[:],
        venezuela: values[:],
        ecuador: values[:],
        peru: values[:],
        guyana: values[:],
        suriname: values[:],
        guyane: values[:],
        brasil: values[:],
        bolivia: values[:],
        paraguay: values[:],
        chile: values[:],
        uruguay: values[:],
        argentina: values[:],
    }
    neighbours = {
        costarica: [panama],
        panama: [costarica, colombia],
        colombia: [panama, venezuela, ecuador, peru, brasil],
        venezuela: [colombia, brasil, guyana],
        ecuador: [peru, colombia],
        peru: [ecuador, brasil, bolivia, chile, colombia],
        guyana: [venezuela, brasil, suriname],
        suriname: [guyana, guyane, brasil],
        guyane: [suriname, brasil],
        brasil: [guyane, suriname, guyana, venezuela, colombia, peru, bolivia, paraguay, argentina, uruguay],
        bolivia: [peru, chile, argentina, paraguay, brasil],
        paraguay: [brasil, bolivia, argentina],
        chile: [peru, bolivia, argentina],
        uruguay: [argentina, brasil],
        argentina: [chile, bolivia, paraguay, brasil, uruguay],
    }

    def constraint_function(first_variable, first_value, second_variable, second_value): # So borders dont have same color
        return first_value != second_value

    constraints = {
        costarica: constraint_function,
        panama: constraint_function,
        colombia: constraint_function,
        venezuela: constraint_function,
        ecuador: constraint_function,
        peru: constraint_function,
        guyana: constraint_function,
        suriname: constraint_function,
        guyane: constraint_function,
        brasil: constraint_function,
        bolivia: constraint_function,
        paraguay: constraint_function,
        chile: constraint_function,
        uruguay: constraint_function,
        argentina: constraint_function,
    }

    return CSP(variables, domains, neighbours, constraints)


if __name__ == '__main__':
    australia = create_southamerica_csp()
    result = australia.backtracking_search()
    for area, color in sorted(result.items()):
        print("{}: {}".format(area, color))

# modify the program from the exercise to use 4 colors and map of SA