from matplotlib import pyplot as plt

""""

Задание 1

0) Повторение понятий из биологии (ДНК, РНК, нуклеотид, протеин, кодон)

1) Построение статистики по входящим в последовательность ДНК нуклеотидам 
для каждого гена (например: [A - 46, C - 66, G - 23, T - 34])

2) Перевод последовательности ДНК в РНК (окей, Гугл)

3) Перевод последовательности РНК в протеин*


*В папке files вы найдете файл rna_codon_table.txt - 
в нем содержится таблица переводов кодонов РНК в аминокислоту, 
составляющую часть полипептидной цепи белка.


Вход: файл dna.fasta с n-количеством генов

Выход - 3 файла:
 - статистика по количеству нуклеотидов в ДНК
 - последовательность РНК для каждого гена
 - последовательность кодонов для каждого гена

 ** Если вы умеете в matplotlib/seaborn или еще что, 
 welcome за дополнительными баллами за
 гистограммы по нуклеотидной статистике.
 (Не забудьте подписать оси)

P.S. За незакрытый файловый дескриптор - караем штрафным дезе.

"""

# read the file dna.fasta

path = input('enter path to dna.fasta file')

with open(path) as dna:
    dna = dna.read()


def dna_parser(dna):
    """parses dna or rna in order to separate and extract pairs of genes and nucleotide chains"""
    dna_separated = dna.split('>')
    dna_separated.remove('')
    dna_separated = [gene.split('\n', 1) for gene in dna_separated]
    return dna_separated


def translate_from_dna_to_rna(dna):
    """your code here"""

    dna_separated = dna_parser(dna)

    genes = []

    for pair in dna_separated:
        pair = ('>' + pair[0], '\n' + pair[1].replace('T', 'U'))
        genes.append(pair)

    rna = ''

    for pair in genes:
        rna += pair[0] + pair[1]

    return rna


def count_nucleotides(dna):
    """your code here"""

    dna_separated = dna_parser(dna)

    dna_nucleotides = ['A', 'C', 'G', 'T']
    num_of_nucleotides = []
    genes = []

    for pair in dna_separated:
        genes.append(tuple(pair))

    for pair in genes:
        counts = []
        for nucleotide in dna_nucleotides:
            counts.append(pair[1].count(nucleotide))
        num_of_nucleotides.append((pair[0], {k: v for (k, v) in zip(dna_nucleotides, counts)}))

    return num_of_nucleotides


def translate_rna_to_protein(rna):
    """your code here"""

    codon_table = path.replace('dna.fasta', 'rna_codon_table.txt')

    with open(codon_table) as codons:
        codons = codons.read()
    codons = codons.replace('\n', '   ').split('   ')
    codons = set(codons)
    codons.remove('')
    codons = {k: v for (k, v) in [codon.split(' ') for codon in codons]}

    rna_separated = dna_parser(rna)
    genes = []

    for pair in rna_separated:
        genes.append((pair[0], pair[1].replace('\n', '')))

    protein = []

    for pair in genes:
        pre_amino_acids = []
        index = 3
        for i in range(len(pair[1]) // 3):
            pre_amino_acids.append(pair[1][index - 3: index])
            index += 3

        protein.append('>' + pair[0] + '\n' + ''.join([codons[codon] for codon in pre_amino_acids]))

    return protein


def histogram(statistics):

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))
    colors = ['#94b8b8', '#bf4040']

    for entry in statistics:
        data = entry[1]
        stats = [v for v in data.values()]
        nucleotides = [n for n in data.keys()]

        axs[statistics.index(entry)].bar(nucleotides, stats, color=colors[statistics.index(entry)])
        axs[statistics.index(entry)].set_title(entry[0])
        axs[statistics.index(entry)].set_xlabel('Nucleotides')
        axs[statistics.index(entry)].set_ylabel('Quantity')
    plt.show()


rna = translate_from_dna_to_rna(dna)
statistics = count_nucleotides(dna)
amino_acids = translate_rna_to_protein(rna)
histogram(statistics)

with open('rna.txt', 'w') as r, open('statistics.txt', 'w') as s, open('amino_acids.txt', 'w') as a:
    r.write(rna)
    statistics_for_biologists = ['>' + entry[0] + '\n' + str(entry[1])[1:-1].replace(':', '-') for entry in statistics]
    s.write('\n'.join(str(x).replace("'", '') for x in statistics_for_biologists))
    a.write('\n'.join(str(x) for x in amino_acids))
