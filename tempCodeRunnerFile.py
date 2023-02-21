r() as pool:
    #     for k in sorted(dataBySize.keys()):
    #         print(f"Graph: {len(graph)}")
    #         chunkSize = max(1, len(dataBySize[k]) // workers)
    #         results = list(pool.map(analyze, [graph]*len(dataBySize), dataBySize[k], chunksize=chunkSize))
            
    #         print(f"Finished analyzing layer-{k}")
    #         print(f"Result len: {len(results)}")
            
    #         for result in results:
    #             for action in result:
    #                 apply_insert(graph, *action)