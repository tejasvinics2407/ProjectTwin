def find_impact(graph, changed_file):

    affected_files = set()

    to_visit = [changed_file]

    while to_visit:

        current_file = to_visit.pop()

        for source, target in graph.edges():

            if target == current_file and source not in affected_files:

                if source != changed_file:
                    affected_files.add(source)
                    to_visit.append(source)

    affected_files = sorted(affected_files)

    return {
        "changed_file": changed_file,
        "affected_files": affected_files,
        "impact_count": len(affected_files)
    }