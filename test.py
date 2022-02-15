from dna_contamination import DNAContamination
from useful_data_structures.chain_hash_map import ChainHashMap



def test(s, k, l):
    """
    The test function allows to verify the operation of the class DNAContamination going to identify all 'inside of a file, the k contaminants with the highest degree of contamination, given a threshold level
    """
    contaminer = DNAContamination(s, l)
    id_string_map = ChainHashMap(cap=1000)

    with open( "./target_batch.fasta", "r") as file:
        
        while True:
            id = file.readline()
            if id == '':
                break
            id = int(id[1:])
            contaminant = file.readline()[:-1]
            id_string_map[contaminant] = id
            contaminer.addContaminant(contaminant)
    string = ''


    max_contaminants = contaminer.getContaminants(k)
    all_contaminants = []
    for contaminant in max_contaminants:
        all_contaminants.append(id_string_map[contaminant])

    for contaminant in sorted(all_contaminants):
        string += ", " + str(contaminant)
    return string[2:]



if __name__ == "__main__":
    s="TGGTGTATGAGCTACCAGCCGTGCGAAACTCATACTATTATCTAATCAGGGACAATACCTCAGGCAGGACTGTGCTGTGTAGATAGCTGGAGAGTATTTCTGATTGTCTCCGAGGGGTGTAAAGGTACTTGCAAGGCCACTCAACTCATGCAGCGTTTCCATTTGAGTTGCCTTGAGTAAACGTCAACGCAGCTGGGAGTAGTACCTCTTGGAGGTTGTGACCGCCGCTGCCCGCATGGACAGACGCACGGAAATGTATTAACACTAACTATACT"
    print(test(s, 20, 7))
    




