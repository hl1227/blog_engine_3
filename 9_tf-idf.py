import os,json,config


class TfIdf:
    def __init__(self):
        self.weighted = False
        self.documents = []
        self.corpus_dict = {}
    def add_document(self, doc_name, list_of_words):
        # building a dictionary
        doc_dict = {}
        for w in list_of_words:
            doc_dict[w] = doc_dict.get(w, 0.) + 1.0
            self.corpus_dict[w] = self.corpus_dict.get(w, 0.0) + 1.0
        # normalizing the dictionary
        length = float(len(list_of_words))
        for k in doc_dict:
            doc_dict[k] = doc_dict[k] / length
        # add the normalized document to the corpus
        self.documents.append([doc_name, doc_dict])
    def similarities(self, list_of_words):
        """Returns a list of all the [docname, similarity_score] pairs relative to a list of words."""
        # building the query dictionary
        query_dict = {}
        for w in list_of_words:
            query_dict[w] = query_dict.get(w, 0.0) + 1.0
        # normalizing the query
        length = float(len(list_of_words))
        for k in query_dict:
            query_dict[k] = query_dict[k] / length
        # computing the list of similarities
        sims = []
        for doc in self.documents:
            score = 0.0
            doc_dict = doc[1]
            for k in query_dict:
                if k in doc_dict:
                    score += (query_dict[k] / self.corpus_dict[k]) + (
                      doc_dict[k] / self.corpus_dict[k])
            sims.append([doc[0], score])
        return sims

def tf_idf(keyword):
    table = TfIdf()
    for file_name in os.listdir(f'./content_txt'):
        f_content_txt=open(f'./content_txt/{file_name}','r',encoding='utf-8')
        table.add_document(file_name, f_content_txt.read().replace('\n', '').replace('.', '').lower().split(' '))
        f_content_txt.close()

    relation_value=f_relation_json.get(keyword.lower())
    if relation_value:
        relation_list=relation_value.lower().split(',')
    else:relation_list=[]
    if ' ' in keyword:
        keyword_list =[keyword.lower()]+keyword.lower().split(' ')+relation_list
    else:
        keyword_list = [keyword.lower()] + relation_list
    tf_idf_list=table.similarities(keyword_list)
    # # print(table.documents)
    # #print(tf_idf_list)

    sorte_list=sorted(tf_idf_list,key=lambda i:i[1],reverse=True)
    txt_name=[]
    for sorte in sorte_list[:config.TF_IDF_SAVE_COUNT]:
        if sorte[1]>0:
            print(f'{keyword}:{sorte[1]}')
            txt_name.append(sorte[0])
    json_dict[keyword]=txt_name

if __name__ == '__main__':

    f_keyword=open('./keyword.txt','r',encoding='utf-8')
    f_keyword_list=f_keyword.readlines()
    f_keyword.close()

    f_relation=open('./relation.txt','r',encoding='utf-8')
    f_relation_json=json.loads(f_relation.read().replace('\n',''))
    f_relation.close()

    f_json = open('./tf_idf_data.json', 'w+', encoding='utf-8')
    json_dict = {}
    for keyword in f_keyword_list:
        tf_idf(keyword.replace('\n',''))

    f_json.write(json.dumps(json_dict) + '\n')
    f_json.close()
