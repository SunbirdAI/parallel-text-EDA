import json
import re
import xml.etree.ElementTree as ET

def extract_alignments(path_to_file, eng_first = True):
    
    alignment_dict = dict()

    tree = ET.parse(path_to_file)
    root = tree.getroot()


    for child in root:
        for grand_child in child:
            #print( grand_child.attrib["xtargets"])
            first_sentences = grand_child.attrib["xtargets"].split(";")[0].split()
            second_sentences = grand_child.attrib["xtargets"].split(";")[1].split()
            for first_sentence, second_sentence in zip(first_sentences, second_sentences):
                if eng_first:
                    alignment_dict[int(first_sentence)] = int(second_sentence)
                else: 
                    alignment_dict[int(second_sentence)] = int(first_sentence)


    return alignment_dict

def extract_sentences(path_to_file):
    tree = ET.parse(path_to_file)
    root = tree.getroot()

    extracted_sentences = dict()
    for child in root:
        extracted_sentences[ int(child.attrib["id"]) ] = child.text

    return extracted_sentences


def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def align_sentences(accumulator_dict, eng_sentences_dict, other_sentences_dict, alignment_dict, other_language ,minimum_length = 30):

    for eng_sentence_index in alignment_dict.keys():
        #eng_sentence_index = int(eng_sentence_index)
        try:
            en_sentence = eng_sentences_dict[eng_sentence_index]
        except KeyError:
            continue
        
        if len(en_sentence) < minimum_length:
                continue

        try:            
            other_sentence_index = alignment_dict[eng_sentence_index]
        except KeyError:
            continue

        
        other_sentence = other_sentences_dict[other_sentence_index]
        #other_sentence = int(other_sentence)

        try:
            if len(accumulator_dict[eng_sentence_index]["eng"]) > 0:
                pass
            else:
                accumulator_dict[eng_sentence_index]["eng"].append(en_sentence)
            try: #If this fails there have been previous sentence values but there is not for this language
                accumulator_dict[eng_sentence_index][other_language].append(other_sentence)
            except KeyError:
                accumulator_dict[eng_sentence_index][other_language] = [other_sentence]
        except KeyError:
            accumulator_dict[eng_sentence_index] = {"eng": [en_sentence], other_language: [other_sentence]}

            
    return accumulator_dict

#function that takes accumulator dict and outputs a jsonl file
def output_jsonl(accumulator_dict, output_path):
    with open(output_path, "w") as outfile:
        for sentence_index in accumulator_dict.keys():
            outdict = {
                "text": accumulator_dict[sentence_index]
            }
            json.dump(outdict, outfile)
            outfile.write("\n")


# with open(OUTPUT_DIR + mozilla101_path, "w") as outfile:
#     for ach_idx, en_idx in ach_en_alignment_dict.items():
#         en_sentence, ach_sentence = eng_sentences[en_idx], acholi_sentences[ach_idx]
#         en_sentence, ach_sentence = striphtml(en_sentence), striphtml(ach_sentence)
        
    
#         outdict = {
#             "text": {
#             "ach": ach_sentence,
#             "eng": en_sentence
#             }
#         }
#         json.dump(outdict, outfile)
#         outfile.write("\n")
