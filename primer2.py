import time

#takes in a sequence and breaks it up into subsequences of length 18. Returns a list of these subsequences.
def get_subsequences(sequence):
    subsequence_list = []
    for x in range(len(sequence)-17):

        subsequence_list.append(sequence[x:(x+18)])

    return subsequence_list

#Takes a sequence and compares it to a list of sequences. Returns the highest number of matches in a sequence it had.
def initial_sequence_match_rate(sequence, sequence_list):
    best_match = 0
    temp = 0

    for x in sequence_list:

        for i in range(len(x)):

            if x[i] == sequence[i]:
                temp = temp + 1

        if temp > best_match:
            best_match = temp

        temp = 0

    return best_match

#Takes in the ranked sequences, removes sequences with a match rate of 0 - 13
def remove_too_degen(ranking):

    for x in range(14):

        ranking[x] = []

    return ranking

#Takes in the ranked sequences, removes sequences with a match rate of 16-18
def remove_attachs_to_unwanted(ranking):

    for x in range(3):

        ranking[len(ranking)-x-1] = []

    return ranking

#takes in a list of ranked subsequences and a sequence list. For each sequence in the list it gets all possible subsequences and compares them to the all of the ranked subseqeunces adjusting the ranked subsequences accordingly. It removes all subsequences that dont match the sequences enough as they will be too degenerate.
def sequence_match_rate(ranked_subsequences, sequence_list):

    for sequence in sequence_list:
        subsequence_list = get_subsequences(sequence)
        ranking = []

        for x in range(19):
            ranking.append([])

        for x in ranked_subsequences:

            if x != []:

                for subsequence in x:
                    num = initial_sequence_match_rate(subsequence, subsequence_list)#############
                    ranking[num].append(subsequence)

        ranked_subsequences = remove_too_degen(ranking)

    return ranked_subsequences

#takes in a list of ranked subsequences and a sequence list. For each sequence in the list it gets all possible subsequences and compares them to the all of the ranked subseqeunces adjusting the ranked subsequences accordingly. It removes all subsequences that match the sequences as they are from the unwanted list
def remove_unwanted_matches(ranked_subsequences, unwanted_sequences):
    i = 0

    for sequence in unwanted_sequences:
        start = time.time()
        subsequence_list = get_subsequences(sequence)
        ranking = []

        for x in range(19):
            ranking.append([])

        for x in ranked_subsequences:

            if x != []:

                for subsequence in x:
                    num = initial_sequence_match_rate(subsequence, subsequence_list)#############
                    ranking[num].append(subsequence)

        ranked_subsequences = remove_attachs_to_unwanted(ranking)
        elapsed = time.time() - start
        print("Compared against sequence", i, "/", len(unwanted_sequences), "Seconds taken:", elapsed)
        i = i + 1

    return ranked_subsequences

start_time = time.time()
####################### reads in file and saves only the sequences from it
with open("bacteria.RDP.Hugenholtz.combined.no_dup.fasta") as f:
    content = f.readlines()
content = [x.strip() for x in content] 
sequence_list = content[1::2]
elapsed_time = time.time() - start_time
print("Checkpoint 1/5 Reached:", elapsed_time)
start_time = time.time()


#creates a list of sequences that we want copies(0-10) of and a list we do not want copies of(11->end of list).
wanted_sequences = sequence_list[0:10]
unwanted_sequences = sequence_list
del unwanted_sequences[0:10]
elapsed_time = time.time() - start_time
print("Checkpoint 2/5 Reached:", elapsed_time)
start_time = time.time()


#gets the subsequences for the first two wanted sequences and creates a ranking of the subsequences based on how much they matched. Removes subseqeunces that dont match enough
subsequences_main = get_subsequences(wanted_sequences[0])
subsequences_second = get_subsequences(wanted_sequences[1])
ranking = []

for x in range(19):
    ranking.append([])

for sequence in subsequences_main:
    num = initial_sequence_match_rate(sequence, subsequences_second)
    ranking[num].append(sequence)

ranking = remove_too_degen(ranking)
elapsed_time = time.time() - start_time
print("Checkpoint 3/5 Reached:", elapsed_time)
start_time = time.time()



#uses the ranking made from the first two wanted sequences to check the ranked subsequences against the other 8 wanted sequences.
ranking = sequence_match_rate(ranking, wanted_sequences[2:])
potentially_viable = []
for x in ranking:
    if x != []:
        for subsequence in x:
            potentially_viable.append(subsequence)
elapsed_time = time.time() - start_time
print("Checkpoint 4/5 Reached:", elapsed_time, "check point 5 can take 1343 seconds to finish")
start_time = time.time()


#uses the ranking to check against the unwanted sequences (9735) and to remove the subsequences that match with them too much
ranking = remove_unwanted_matches(ranking, unwanted_sequences)
elapsed_time = time.time() - start_time
print("Checkpoint 5/5 Reached:", elapsed_time)
viable = []

for x in ranking:

    if x != []:

        for subsequence in x:
            viable.append(subsequence)

#if there are subsequences that are still viable it prints them out. If there are not it prints out the sequences that were potentially viable as they still attach to the unwanted set
if viable == []:
    
    print("There are no subsequences that will attach to the wanted set but not the unwanted set. The set that will attach to the wanted set and will also attach to the unwanted set is :")
    
    for x in potentially_viable:
        print(x)
else:
    print("The viable options are:")

    for x in viable:
        print(x)
