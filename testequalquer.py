transaction_propertys = {
            # Valor, new_value, comparator
            # Se new_value for diferente de comparator
            # Defina Valor como new_value
            "date": {"new_value": 1, "comparator": 1},
            "description": {"new_value": 2, "comparator":2},
        }

print(transaction_propertys.items())
#dict_items([('date', {'new_value': 1, 'comparator': 1}), ('description', {'new_value': 2, 'comparator': 2})])


for k, (v1, v2) in transaction_propertys.items():
    print(k)
    print(v1)
    print(v2)

    #date
    # new_value
    # comparator
    # description
    # new_value
    # comparator