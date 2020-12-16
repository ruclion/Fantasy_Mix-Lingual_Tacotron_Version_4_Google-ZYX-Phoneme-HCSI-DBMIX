import os
from tqdm import tqdm
import databaker_G2P_1 as g2p_1
import pinyin_G2P_2 as g2p_2


in_path = '/ceph/home/hujk17/TTS.DataBaker.zhcmn.enus.F.DB6.emotion/CN/000001-010000.txt'
out_dir = 'databaker_MIX_Phoneme'


def write_metadata(metadata, out_dir, out_path):
	with open(os.path.join(out_dir, out_path), 'w', encoding='utf-8') as f:
		for m in tqdm(metadata):
			f.write('|'.join([str(x) for x in m]) + '\n')
		print('len:', len(metadata))
	return True



def main():
    os.makedirs(out_dir, exist_ok=True)
    meta = g2p_1.build_from_path_CN(in_path, use_prosody = True)
    finished = write_metadata(meta, out_dir, 'DBMIX_CN_meta_pingyin.csv.txt')
    print('tag:', finished)
    print('0:', '|'.join(meta[0]))

    meta_symbol = []
    for x in meta:
        # ['009937', 'you3-le5 pen1-shui3-qiang1-de5.']
        basename = x[0]
        pinyin = x[1]
        pinyin_symbol_list = g2p_2.pinyin_to_symbols(pinyin)
        # _代表分字符, 空格, -, ,号, .号代表韵律
        meta_symbol.append([basename, '_'.join(pinyin_symbol_list)])

    finished = write_metadata(meta_symbol, out_dir, 'DBMIX_CN_meta_symbol_split.csv.txt')
    print('tag:', finished)
    print('0:', '|'.join(meta_symbol[0]))

    # 需要再来个声调embedding到声韵母上的

    # ans1 = g2p_2.pinyin_to_symbols('ma1 ma1 dang1 shi2 biao3 shi4 er2 zi5 kai1 xin1 de5 xiang4 huar1 yi2 yang4')
    # ans2 = g2p_2.pinyin_to_symbols('ma1-ma1 dang1-shi2 biao3-shi4, er2-zi5 kai1-xin1-de5 / xiang4-huar1 yi2-yang4.')
    # # TODO
    # ans3 = g2p_2.pinyin_to_symbols('ma1-ma1 dang1-shi2 biao3-shi4, er2-zi5 kai1-xin1-de5 / xiang4-huar1 yi2-yang4?')
    # print(ans1)
    # print(ans2)
    # print(ans3)


if __name__ == "__main__":
    main()


