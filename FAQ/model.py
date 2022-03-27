from deeppavlov import configs, train_model
from deeppavlov.core.common.file import read_json
from pprint import pprint


class TrainError(Exception):
    pass


class Faq:
    """В данном классе будет реализован простой intent detection"""

    def __init__(self, file):
        # self.model_conf = read_json(configs.faq.fasttext_tfidf_autofaq)
        # self.model_conf['dataset_reader']['data_path'] = file
        # self.model_conf['dataset_reader']['data_url'] = None
        # self.model_conf['metadata']['variables']['ROOT_PATH'] = '/home/user/src/deeppavlov'

        # ++++++++
        self.model_conf = read_json(configs.faq.tfidf_autofaq)
        self.model_conf['dataset_reader']['data_path'] = file
        self.model_conf['dataset_reader']['data_url'] = None
        self.model_conf['chainer']['pipe'][3]['top_n'] = 1

        # self.model_conf = read_json(configs.faq.tfidf_logreg_autofaq)
        # self.model_conf['dataset_reader']['data_path'] = file
        # -----------------------------------
        # self.model_conf = read_json(configs.faq.fasttext_avg_autofaq)
        # self.model_conf['dataset_reader']['data_path'] = file
        # self.model_conf['dataset_reader']['data_url'] = None
        # self.model_conf['metadata']['variables']['ROOT_PATH'] = '/home/user/src/deeppavlov'

        self.faq = None

    def train(self):
        self.faq = train_model(self.model_conf)

    def infer(self, question):
        if not self.faq:
            raise TrainError('Model needs to train')
        return self.faq([question])


if __name__ == '__main__':
    faq = Faq('servicedumps.csv')
    faq.train()
    answer = faq.infer('У меня нет прописки')
    # print(answer[0][0], answer[1][0])
    print(answer)
