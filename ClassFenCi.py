# HanLP源代码的授权协议为 Apache License 2.0 https://github.com/hankcs/HanLP#%E6%BA%90%E4%BB%A3%E7%A0%81
# 本模块基于https://github.com/hankcs/HanLP制作

import hanlp
import json
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)

class FenCi(object):
    def __init__(self):
        self.tok = hanlp.load(hanlp.pretrained.tok.FINE_ELECTRA_SMALL_ZH, tasks='tok/fine') #加载模型
        self.tokc = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH, tasks='tok/coarse') # fine为细分；coarse为粗分；tok*一起使用
        self.con = hanlp.load(hanlp.pretrained.pos.CTB9_POS_ELECTRA_SMALL)
        self.all = hanlp.pipeline() \
            .append(hanlp.utils.rules.split_sentence, output_key='sentences') \
            .append(hanlp.load('FINE_ELECTRA_SMALL_ZH'), output_key='tok') \
            .append(hanlp.load('CTB9_POS_ELECTRA_SMALL'), output_key='pos') \
            .append(hanlp.load('MSRA_NER_ELECTRA_SMALL_ZH'), output_key='ner', input_key='tok') \
            .append(hanlp.load('CTB9_DEP_ELECTRA_SMALL', conll=0), output_key='dep', input_key='tok')\
            .append(hanlp.load('CTB9_CON_ELECTRA_SMALL'), output_key='con', input_key='tok')
    
    def tok(self, *args):
        with open('dict_force.json', 'r+', encoding='utf-8') as f:
            dict_force = json.load(f)
        self.tok.dict_force = dict_force
        with open('dict_combine.json', 'r+', encoding='utf-8') as f:
            d = json.loads(f.read())
            set_combine = set(d.keys())
            logging.info(set_combine)
        self.tok.dict_combine = set_combine
        return self.tok(list(args))
    
    # 强制模式 大词分小词
    def tok_separate(self, i, *args):
        with open('dict_force.json', 'r', encoding='utf-8') as f:
            dict_force = json.loads(f.read())
            dict_force[i] = list(args)
        with open('dict_force.json', 'w', encoding='utf-8') as f:
            content = json.dumps(dict_force)
            f.write(content)

    # 合并模式 优先级低于统计模式
    def tok_merge(self, tp):
        logging.info('tp2: {}'.format(tp))
        with open('dict_combine.json', 'r', encoding='utf-8') as f:
            d = json.loads(f.read())
            set_combine = set(d.keys())
            logging.info(set_combine)
            set_combine = set_combine | set(tp)
            logging.info(set_combine)
            dict_combine = {}
            for i in set_combine:
                dict_combine[i] = 0
        with open('dict_combine.json', 'w', encoding='utf-8') as f:
            content = json.dumps(dict_combine)
            f.write(content)
    
    # 全局字典
    def tok_all(self, s):
        t = self.all(s)
        return json.dumps(t)
    
    def tok_con(self, s):
        return self.con(s)
if __name__ == '__main__':
    fc = FenCi()
    # print(fc.tok('来张雷姆涩图'))
    # fc.tok_merge(('雷姆', '涩图'))
    # fc.tok_separate()
    a = fc.tok_all('我爱你但你却爱着他')
    print(a)
    print(type(a))