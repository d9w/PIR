import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def test_valid_window(window, test_level = 5):
    """
    window : the window in the signal that has to be tested
    
    This funtion test the window to insure that it doesn't contain the signal of interest (spike)
    """
    #non zero ?
    second = np.percentile(window, 2)
    thirtyth = np.percentile(window, 30)
    #print(str(second) + "\t" + str(thirtyth) + "\t" + str(second/thirtyth))
    if abs(second/thirtyth) < test_level : 
        return True
    else : 
        return False
    
def init_noise_levels(signal, fs, 
                      noise_window_size = 0.01,
                      required_valid_windows = 100,
                      old_noise_level_propagation = 0.8, 
                      test_level = 5,
                      estimator_type = "RMS",
                      percentile_value = 25):
    
    if estimator_type == "RMS":
        return init_noise_levels_RMS(signal, fs, 
                      noise_window_size = noise_window_size,
                      required_valid_windows = required_valid_windows,
                      old_noise_level_propagation = old_noise_level_propagation, 
                      test_level = test_level,
                      percentile_value = percentile_value)
        
    elif estimator_type == "MAD":
        return init_noise_levels_MAD(signal, fs, 
                      noise_window_size = noise_window_size,
                      required_valid_windows = required_valid_windows,
                      old_noise_level_propagation = old_noise_level_propagation, 
                      test_level = test_level,
                      percentile_value = percentile_value)
    
    else: return None
    
    
def init_noise_levels_RMS(signal, fs, 
                      noise_window_size = 0.01,
                      required_valid_windows = 100,
                      old_noise_level_propagation = 0.8, 
                      test_level = 5,
                      percentile_value = 25):
    
    nb_valid_windows = 0
    list_RMS = []
    noise_levels = []
    
    noise_level = -1
    
     
    #boucle en indice
#    for window_index in range(0,len(signal)-(len(signal)%int(fs*noise_window_size)),int(fs*noise_window_size)):
    for window_index in range(0,len(signal),int(fs*noise_window_size)):
        test = test_valid_window(signal.iloc[window_index: window_index + int(fs*noise_window_size)], test_level)
        if nb_valid_windows < required_valid_windows:
            if test == True :
                RMS = np.sqrt(np.mean(signal.iloc[window_index: window_index + int(fs*noise_window_size)]**2))
                list_RMS.append(RMS)
                nb_valid_windows += 1
            
            if nb_valid_windows == required_valid_windows:
                noise_level = np.percentile(list_RMS, percentile_value)
                for elm in range(0, window_index, int(fs*noise_window_size)):
                    noise_levels.append(noise_level)
                
        else :
            """if test == True:
                if (window + int(fs*noise_window_size)) > (len(signal)-1) :
                    N25 = np.percentile(abs(signal.iloc[window:]), 25)
                else :
                    N25 = np.percentile(abs(signal.iloc[window: window + int(fs*noise_window_size)]), 25)
                noise_level = old_noise_level_propagation*noise_level + (1-old_noise_level_propagation)*N25
            noise_levels.append(noise_level)"""
            if test == True:
                if (window_index + int(fs*noise_window_size)) > (len(signal)-1) :
                    RMS = np.sqrt(np.mean(signal.iloc[window_index:]**2))
                else :
                    RMS = np.sqrt(np.mean(signal.iloc[window_index: window_index + int(fs*noise_window_size)]**2))
                list_RMS.append(RMS)
                NX = np.percentile(list_RMS, percentile_value)
                new_noise_level = old_noise_level_propagation*noise_level + (1-old_noise_level_propagation)*NX
                noise_level = new_noise_level
            noise_levels.append(noise_level)
            
    #cas ou il n'y a pas eut 100 fenetres de bruit valides rencontrees
    if noise_level == -1:
        
        #cas ou aucune fenetre valide n'a ete rencontree
        if noise_levels == []:
            for elm in range(0, len(signal), int(fs*noise_window_size)):
                noise_levels.append(0)
            
        else:
            noise_level = np.percentile(list_RMS, percentile_value)
            for elm in range(0, len(signal), int(fs*noise_window_size)):
                noise_levels.append(noise_level)
        
    
    noise_levels.append(noise_level)        
    plt.figure()
    plt.plot(list_RMS)
    plt.xlabel('Time Windows')
    plt.title('RMS values')
    plt.grid(True)
                
    return noise_levels

def init_noise_levels_MAD(signal, fs, 
                      noise_window_size = 0.01,
                      required_valid_windows = 100,
                      old_noise_level_propagation = 0.8, 
                      test_level = 5,
                      percentile_value = 25):
    
    nb_valid_windows = 0
    list_MAD = []
    noise_levels = []
     
    #boucle en indice
    for window_index in range(0,len(signal),int(fs*noise_window_size)):
        test = test_valid_window(signal.iloc[window_index: window_index + int(fs*noise_window_size)], test_level)
        if nb_valid_windows < required_valid_windows:
            if test == True :
                ###RMS = np.sqrt(np.mean(signal.iloc[window_index: window_index + int(fs*noise_window_size)]**2))
                MAD = scipy.stats.median_absolute_deviation(signal.iloc[window_index: window_index + int(fs*noise_window_size)])
                list_MAD.append(MAD)
                nb_valid_windows += 1
            
            if nb_valid_windows == required_valid_windows:
                noise_level = np.percentile(list_MAD, percentile_value)
                for elm in range(0, window_index, int(fs*noise_window_size)):
                    noise_levels.append(noise_level)
                
        else :
            """if test == True:
                if (window + int(fs*noise_window_size)) > (len(signal)-1) :
                    N25 = np.percentile(abs(signal.iloc[window:]), 25)
                else :
                    N25 = np.percentile(abs(signal.iloc[window: window + int(fs*noise_window_size)]), 25)
                noise_level = old_noise_level_propagation*noise_level + (1-old_noise_level_propagation)*N25
            noise_levels.append(noise_level)"""
            if test == True:
                if (window_index + int(fs*noise_window_size)) > (len(signal)-1) :
                    ###RMS = np.sqrt(np.mean(signal.iloc[window_index:]**2))
                    MAD = scipy.stats.median_absolute_deviation(signal.iloc[window_index:])
                else :
                    ###RMS = np.sqrt(np.mean(signal.iloc[window_index: window_index + int(fs*noise_window_size)]**2))
                    MAD = scipy.stats.median_absolute_deviation(signal.iloc[window_index: window_index + int(fs*noise_window_size)])
                list_MAD.append(MAD)
                NX = np.percentile(list_MAD, percentile_value)
                new_noise_level = old_noise_level_propagation*noise_level + (1-old_noise_level_propagation)*NX
                noise_level = new_noise_level
            noise_levels.append(noise_level)
    
    noise_levels.append(noise_levels)        
    plt.figure()
    plt.plot(list_MAD)
    plt.xlabel('Time Windows')
    plt.title('MAD values')
    plt.grid(True)
                
    return noise_levels



#find spike

def find_spike(signal, initial_index, noise_levels, fs, spike_info, 
               window_size = 0.001, 
               noise_window_size = 0.01,
               threshold_factor = 3.5,
               maxseparation = 0.0008):
    
    offset_index = int(np.round(signal.index[0]*fs/1000))
    
    if initial_index < len(signal) + offset_index:
        i = initial_index
        for value in signal.iloc[initial_index-offset_index:]:
            threshold = threshold_factor*noise_levels[int(np.round((i/fs)//noise_window_size))]
            if value > threshold:
                while(True):
                    if i > initial_index + window_size*fs:
                        b_point = int(np.round(i - window_size*fs)) - offset_index
                    else :
                        b_point = initial_index - offset_index
                    if i < len(signal)+offset_index - window_size*fs-1:
                        e_point = int(np.round(i + window_size*fs)) - offset_index
                    else :
                        e_point = len(signal)

                    highest_value = signal.iloc[b_point: e_point].max()
                    
                    if highest_value == value : 
                        break
                    
                    else:
                        i = int(np.round(signal.iloc[b_point: e_point].idxmax()*fs/1000))
                        value = signal.iloc[i-offset_index] 
                
                
                
                if i == initial_index and i-offset_index-1>=0:
                    if signal.iloc[i-offset_index-1]>signal.iloc[i-offset_index]:
                        #print("Cas on est au mur gauche")
                        #décaler la limite de gauche jusqu'à la prochaine valeur en dessous du seuil
                        while signal.iloc[i-offset_index]>threshold:
                            i += 1
                        return i
               
                i_min = -33
                #partir à la recherche d'un min du spike
                for k in range(int(np.round(maxseparation*fs))):
                    if (i-offset_index+k) < len(signal)-1:
                        if signal.iloc[i-offset_index+k] < -threshold and signal.iloc[i-offset_index+k]<signal.iloc[i-offset_index+k+1]:
                            i_min = i+k
                            #print("i_min: "+str(i_min))
                            break
                    if (i-offset_index-k) > 0:
                        if signal.iloc[i-offset_index-k]<-threshold and signal.iloc[i-offset_index-k]<signal.iloc[i-offset_index-k-1]:
                            i_min = i-k
                            #print("i_min: "+str(i_min))
                            break
                if i_min == -33:
                    #on a pas rencontré de spike
                    #print("j'ai pas trouvé l'extremum minimum :'('")
                    while signal.iloc[i-offset_index]>threshold:
                        i += 1
                    return i
                else:
                    #récolte infos du spike
                    #print("J'ai trouvé un spike! et je l'enregistre :D")
                    #on cherche ensuite le premier depassement positif (indpos) et négatif (indneg)
                    indpos = i
                    indneg = i_min
                    
                    while signal.iloc[indpos-offset_index] > threshold:
                        indpos -= 1
                        if indpos == offset_index-1:
                            break
                    indpos += 1 #on obtient l'indice du premier dépassement positif
                    while signal.iloc[indneg-offset_index] < -threshold:
                        indneg -= 1
                        if indneg == offset_index-1:
                            break
                    indneg += 1 #on obtient l'indice du premier dépassement négatif
                    
                    #on cherhce le zéro entre les deux "bosses"
                    indzero = i
                    if(i>i_min): #le max est après
                        while signal.iloc[indzero-offset_index] > 0:
                            indzero -= 1
                    else:
                        while signal.iloc[indzero-offset_index] > 0:
                            indzero += 1
                        indzero -= 1
                    
                         # indice max, indice min, indice 1er depasssement pos, indice 1er depassement nég, 
                            # premier dépassement, indice du zero central,distance entre max et min, 
                            #variation d'amplitude entre min et max
                    spike_info.append([i, i_min, indpos, indneg, min(indpos,indneg), indzero, i-i_min, 
                                       abs(signal.iloc[i-offset_index]-signal.iloc[i_min-offset_index])])
                    return i+int(np.round(window_size*fs))
                
                break  
            i += 1
    return -44

#vérifier que le deuxième extrêmum n'est pas collé au mur de gauche ni de droite
            
def find_spikes(signal, noise_levels, fs, 
               window_size = 0.001, 
               noise_window_size = 0.01,
               threshold_factor = 3.5,
               maxseparation = 0.0008):
    
    initial = int(np.round(signal.index[0]*fs/1000))
    spike_info = []
    
    while initial != -44:
        initial = find_spike(signal, initial, noise_levels, fs, spike_info,
                             window_size = window_size, 
                             noise_window_size = noise_window_size,
                             threshold_factor = threshold_factor,
                             maxseparation = 0.0008)
    df_spike_info = pd.DataFrame(spike_info)
    df_spike_info.columns = ['indice_max','indice_min','indice_depass_positif','indice_depass_negatif', 'indice_1er_depass','indice_zero_central','i_max-i_min','Delta_amplitudes']

    return df_spike_info


#record spike

def record_spikes(signal, fs, spike_centers,
                  t_before = 0.001,
                  t_after = 0.002):
    
    data = np.array([[float(x) for x in range(int(np.round(fs*(t_before+t_after)))+1)]])
    
    initial_index = int(np.round(signal.index[0]*fs/1000))
    print('initial index:'+str(initial_index))
    
    for center in spike_centers:
        if center < int(np.round(fs*t_before)) + initial_index:
            spike = [0 for i in range(0, int(np.round(fs*t_before-(center-initial_index))))]
            #print('spike before concat:'+ str(len(spike)))
            #spike = np.concatenate(spike, signal.iloc[:center + int(np.round(fs*t_after))].values())
            spike = np.concatenate((spike, signal.values[:center + int(np.round(fs*t_after)) - initial_index]))
            #print('spike after concat:'+str(len(spike)))
            data = np.insert(data, len(data), spike, axis=0)
            
        elif center > int(np.round(len(signal)-fs*t_after)) + initial_index:
            #spike = signal.iloc[int(np.round(center-fs*t_before)):].values()
            spike = signal.values[int(np.round(center-fs*t_before))-initial_index:]
            #print('spike before concat:'+str(len(spike)))
            spike = np.concatenate((spike,[0 for i in range(0, int(np.round(fs*t_after-(len(signal)+initial_index-center))))]))
            #print('spike after concat:'+str(len(spike)))
            data = np.insert(data, len(data), spike, axis=0)
            
        else :
            #spike = signal.iloc[int(np.round(center - fs*t_before)): int(np.round(center + fs*t_after))+1].values()
            spike = signal.values[int(np.round(center - fs*t_before))-initial_index: int(np.round(center + fs*t_after))+1-initial_index]
            data = np.insert(data, len(data), spike, axis=0)

    print(np.shape(data))
    data = data.transpose()
    #print(data)
    spike_data = pd.DataFrame(data)
    
    return spike_data


def record_spikes_oneline(signal, fs, spike_centers,
                  t_before = 0.001,
                  t_after = 0.002):
    
    data = np.array(['NaN' for x in range(len(signal))])
    data = data.astype(float)
    times = np.array(['NaN' for x in range(len(signal))])
    times = times.astype(pd.Timestamp)
    
    for center in spike_centers:
        if center < int(np.round(fs*t_before)):
            data[:center + int(np.round(fs*t_after))] = signal.values[:center + int(np.round(fs*t_after))]
            times[:center + int(np.round(fs*t_after))] = signal.index[:center + int(np.round(fs*t_after))]
            
        elif center > int(np.round(len(signal)-fs*t_after)):
            data[int(np.round(center-fs*t_before)):] = signal.values[int(np.round(center-fs*t_before)):]
            times[int(np.round(center-fs*t_before)):] = signal.index[int(np.round(center-fs*t_before)):]
            
        else :
            data[int(np.round(center - fs*t_before)): int(np.round(center + fs*t_after))+1] = signal.values[int(np.round(center - fs*t_before)): int(np.round(center + fs*t_after))+1]
            times[int(np.round(center - fs*t_before)): int(np.round(center + fs*t_after))+1] = signal.index[int(np.round(center - fs*t_before)): int(np.round(center + fs*t_after))+1]

    spike_data_oneline = pd.DataFrame(data, index = times.astype(float))
    
    return spike_data_oneline