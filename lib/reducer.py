import util, math

#--------------------------------------------------------------------------------------------------
def reverse_reduction(net, sample_size, advice_sampling_threshold, advice, configs): #only version that handle Direct Evolution

    advice_upon = configs['advice_upon']
    BD_criteria = configs['BD_criteria']
    tolerance = int(configs['tolerance'])

    if  advice_sampling_threshold <=0:
        print ("WARNING: reverse_reduction yields empty set.")
        yield [{},{},0]
    else:
        if (advice != None): #ie direct evo, keep same advice
            for i in range(advice_sampling_threshold):
                yield [BDT_calculator(net, advice, tolerance, BD_criteria, advice_upon)]

        else:
            if (advice_upon == 'nodes'): samples = net.nodes()
            elif (advice_upon == 'edges'): samples = net.edges()
            else:
                print ("ERROR reverse_reduction: unknown advice_upon: " + str(advice_upon))
                return

            for i in range(advice_sampling_threshold):
                yield [ BDT_calculator   (net, util.advice (net, util.sample_p_elements(samples,sample_size), configs), tolerance, BD_criteria, advice_upon) ]


#--------------------------------------------------------------------------------------------------
def BDT_calculator (M, Advice, T_percentage, BD_criteria, advice_upon):
    BENEFITS, DAMAGES = {}, {}

    if (BD_criteria != 'both' and BD_criteria != 'source' and BD_criteria != 'target'):
        print("ERROR in reducer.BDT_calc_node: unknown BD_criteria: " + str(BD_criteria))
    
    for element in Advice.keys():
        if (advice_upon=='nodes'):
            target = element
            sources = M.predecessors(target)

            for source in sources:
                advice = Advice[target]

                if M.has_edge(source, target):

                    if M[source][target]['sign']==advice:      #in agreement with the Oracle
                        if (BD_criteria == 'both' or BD_criteria == 'source'):
                            ######### REWARDING the source node ###########
                            if source in BENEFITS.keys():
                                BENEFITS[source]+=1
                            else:
                                BENEFITS[source]=1
                                if source not in DAMAGES.keys():
                                    DAMAGES[source]=0

                        if (BD_criteria == 'both' or BD_criteria == 'target'):
                            ######### REWARDING the target node ###########
                            if target in BENEFITS.keys():
                                BENEFITS[target]+=1
                            else:
                                BENEFITS[target]=1
                                if target not in DAMAGES.keys():
                                    DAMAGES[target]=0

                    ###############################################
                    else:                                              #in disagreement with the Oracle
                        if (BD_criteria == 'both' or BD_criteria == 'source'):
                            ######### PENALIZING the source node ##########
                            if source in DAMAGES.keys():
                                DAMAGES[source]+=1
                            else:
                                DAMAGES[source]=1
                                if source not in BENEFITS.keys():
                                    BENEFITS[source]=0

                        if (BD_criteria == 'both' or BD_criteria == 'target'):
                            ######### PENALIZING the target node ##########
                            if target in DAMAGES.keys():
                                DAMAGES[target]+=1
                            else:
                                DAMAGES[target]=1
                                if target not in BENEFITS.keys():
                                    BENEFITS[target]=0
                        ###############################################

        elif (advice_upon=='edges'):
            advice = Advice[element]
            element = element.replace('(','').replace(')','').replace("'",'').replace(' ','')
            element = element.split(",")
            source = int(element[0])
            target = int(element[1])

            if (M.has_edge(source, target)):

                if M[source][target]['sign'] == advice:  # in agreement with the Oracle
                    if (BD_criteria == 'both' or BD_criteria == 'source'):
                        ######### REWARDING the source node ###########
                        M.node[source]['benefits'] += 1
                        if source in BENEFITS.keys():
                            BENEFITS[source] += 1
                        else:
                            BENEFITS[source] = 1
                            if source not in DAMAGES.keys():
                                DAMAGES[source] = 0


                    if (BD_criteria == 'both' or BD_criteria == 'target'):
                        ######### REWARDING the target node ###########
                        M.node[target]['benefits'] += 1
                        if target in BENEFITS.keys():
                            BENEFITS[target] += 1
                        else:
                            BENEFITS[target] = 1
                            if target not in DAMAGES.keys():
                                DAMAGES[target] = 0

                ###############################################
                else:  # in disagreement with the Oracle
                    if (BD_criteria == 'both' or BD_criteria == 'source'):
                        ######### PENALIZING the source node ##########
                        M.node[source]['damages'] += 1
                        if source in DAMAGES.keys():
                            DAMAGES[source] += 1
                        else:
                            DAMAGES[source] = 1
                            if source not in BENEFITS.keys():
                                BENEFITS[source] = 0

                    if (BD_criteria == 'both' or BD_criteria == 'target'):
                        ######### PENALIZING the target node ##########
                        M.node[target]['damages'] += 1
                        if target in DAMAGES.keys():
                            DAMAGES[target] += 1
                        else:
                            DAMAGES[target] = 1
                            if target not in BENEFITS.keys():
                                BENEFITS[target] = 0
                                ###############################################

        else:
            print ("ERROR reducer: unknown advice_upon: " + str(advice_upon))
            return
    
    T_edges = round (max (1, math.ceil (sum(DAMAGES.values())*(T_percentage/100))))

    assert len(BENEFITS.keys())==len(DAMAGES.keys())
    return BENEFITS, DAMAGES, T_edges
