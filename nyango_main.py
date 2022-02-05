# -*- encoding: utf-8 -*-

import re
import MeCabUse
import sys


def main(input_text):

    # 品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音
    mecab_list = MeCabUse.morphological_analysis(input_text)

    # print(mecab_list)

    # 猫語辞書
    neko_dict = {"ニャ", "ナ", "ヌ", "ネ", "サ", "ナ",
                 "ヤ", "ラ", "ザ", "バ"}

    def neko_check(word, neko_dict):
        """猫語になる文字を含んでいるかどうか"""
        for character in word:
            if character in neko_dict:
                return True
        return False

    output_text = ""
    for mecab_word in mecab_list:
        if (mecab_word[-2] == "ヌ" and mecab_word[1] == "助動詞") or\
                (mecab_word[-2] == "ナイ" and mecab_word[1] == "形容詞"):
            # 否定形の「ぬ」を「にゃい」に変換
            output_text += "にゃいにゃ"
        elif mecab_word[-2] in {"ネコ"}:
            # ネコをにゃんに変換
            output_text += "にゃん"
        # 猫語辞書に入っているか and 名詞か
        elif neko_check(mecab_word[-2], neko_dict) and mecab_word[1] in {"名詞", "助動詞", "形容詞", "動詞"}:
            # ニャ変換
            for character in mecab_word[-2]:
                # print(character)
                character = "にゃ" if character in neko_dict else character
                output_text += character
        else:
            output_text += mecab_word[0]  # 表層形

    def iikiri_check(text):
        """末尾が言い切りの形か"""
        iikiri = ["だ", "だろ", "です", "ます", "ある",
                  "た", "る", "が", "か", "く", "せん", "ない"]
        for word in iikiri:
            if text.endswith(word):
                return True
        return False

    # 最後が言い切り形のときににゃを追加{
    special_characters_re = re.compile(r"^[\u3000-\u303F]+$")
    temp = output_text.replace(
        "。", "。<<SPLIT_TAG>>").replace("、", "、<<SPLIT_TAG>>").replace("」", "」<<SPLIT_TAG>>")  # 句読点カッコ閉じる
    output_text = ""

    if temp in "<<SPLIT_TAG>>":
        # 句読点カッコ閉じるが存在する場合
        for sentence in temp.split("<<SPLIT_TAG>>"):  # 句読点で区切る
            temp_sentence = special_characters_re.sub("", sentence)  # 記号を削除
            if iikiri_check(temp_sentence):
                # 最後の記号文字列の左ににゃを挿入
                for i, character in enumerate(reversed(sentence)):
                    if not special_characters_re.match(character):
                        output_text += sentence[:-i]+"にゃ"+sentence[-i:]
                        break
            else:
                output_text += sentence
    else:
        # 句読点カッコ閉じるが存在しない場合
        output_text = temp+"にゃん"

    return output_text


if __name__ == "__main__":
    # input_text = "吾輩は猫である。名前はまだ無い。どこで生れたかとんと見当がつかぬ。何でも薄暗いじめじめした所でニャーニャー泣いていた事だけは記憶している。"
    input_text = sys.argv[1]
    output_text = main(input_text)

    print("<入力文>")
    print(input_text)
    print()
    print("<出力結果>")
    print(output_text)
