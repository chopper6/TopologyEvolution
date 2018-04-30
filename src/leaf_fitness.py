def node_score (leaf_metric, B, D):
    if (B+D==0): return 0

    if (leaf_metric=='RGAR'):
        if (B==0 and D > 0 or D==0 and B > 0): return 1
        else: return 0

    else: print("ERROR in fitness.node_leaf_score(): unknown leaf metric: " + str(leaf_metric))

