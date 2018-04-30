
def assign_numer (hub_metric, soln_bens, soln_dmgs):
    if (sum(soln_bens) == 0): return 0

    if (hub_metric=='ETB'): return sum(set(soln_bens))
    elif(hub_metric=='control'): return max(soln_bens)
    elif(hub_metric == 'Bin'): return sum(soln_bens)

    else: print("ERROR in fitness.assign_hub_numer(): unknown hub metric " + str(hub_metric))


def assign_denom (hub_metric, soln_bens, all_bens):
    if (sum(soln_bens) == 0): return 1

    if (hub_metric=='ETB' or hub_metric=='Bin'): return sum(all_bens)
    elif(hub_metric=='control'): return len(soln_bens) #for ex.

    else: return 1