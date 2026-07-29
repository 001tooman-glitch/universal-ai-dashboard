def detect_scenario(tables):

    if len(tables) < 2:
        return "single"

    structures = []

    for df in tables.values():
        structures.append(set(df.columns))

    base_structure = structures[0]

    similarities = []

    for structure in structures[1:]:

        similarity = (
            len(base_structure.intersection(structure))
            / len(base_structure.union(structure))
        )

        similarities.append(similarity)

    average_similarity = sum(similarities) / len(similarities)

    if average_similarity >= 0.9:
        return "time_series"

    return "relational"
