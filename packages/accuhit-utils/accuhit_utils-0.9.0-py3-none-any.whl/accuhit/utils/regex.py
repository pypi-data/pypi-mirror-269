# -*- coding: utf-8 -*-
import re
from enum import Enum


class RegexFilter(Enum):
    date = re.compile("[12]\d{3}[-/.](0?[1-9]|1[0-2])[-/.](0[1-9]|[12]\d|3[01]|0?[1-9])")
    time = re.compile("([0-1][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]")
    time2 = re.compile("([0-1][0-9]|2[0-3]):[0-5][0-9]")
    url = re.compile("(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?")
    space = re.compile("\s+")
    tab = re.compile("\t+")
    XD = re.compile("(x|X+)(d|D+)")
    smile = re.compile("[w+]")
    zh_symbol = re.compile("[～·！＠＃＄％＾＆＊（）＿＋『』「」｜：“，。？；、＝〈〉《》【】〔〕〖〗〝〞︰︳︴﹉﹊﹋﹌﹍﹎﹏﹐﹑﹔﹕﹖﹝﹞﹟﹠﹡﹢﹤﹦﹨﹩﹪﹫＂＇￣]+")
    # ch_symbol = re.compile("[^\u4e00-\u9fa5]")
    en_symbol = re.compile("[\/\|\\\(\)\{\}\[\]\$\^\?\*\+\-\"\'`~!@#%:&_=;><,.•‘’“”…‹›]+")
    JP = re.compile("[\u0800-\u4e00]+")
    KR = re.compile("[\x3130-\x318F\uAC00-\uD7FFh]+")
    ZH = re.compile("[\u4e00-\u9fa5]+")  # 匹配中文字
    reduplication = re.compile("(.)\\1+|(.{2})\\2+")  # 匹配疊字
    emoji = re.compile(
        u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF]|[\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    ch_bopomofo = re.compile(u'([\u3105-\u3129\u02CA\u02C7\u02CB\u02D9])')


def filter_symbol(content, *args):
    if content:
        for regex in args:
            content = regex.sub("", content)
    return content


def filter_space(content):
    en_txt = re.compile("\s{,1}[\w]+\s{,1}").findall(content)
    regex = re.compile("(\w|\s)*[A-Za-z](\w|\s)$")
    for idx, en in enumerate(en_txt):
        if regex.match(en):
            continue
        en_txt[idx] = re.compile("\s+").sub("", en)
    return "".join(en_txt)


def filter_html_tag(content):
    html_tag = re.compile('<.*?>|&\w+;')
    return html_tag.sub("", content)


def filter_datetime(content):
    # datetime = re.compile("\d+年|\d+月|\d+日|\d+點\d+分")
    datetime = re.compile("\d+\)?\s?日|\d+\s?月|\d+\s?年|\d+\s?點\d+\s?分")
    return datetime.sub("", content)


def filter_reduplication(content):
    new_content = ""
    last_end = 0
    for match in RegexFilter.reduplication.value.finditer(content):
        w = match.group()
        start_idx = match.start()
        if last_end != start_idx:
            new_content += content[last_end:start_idx]
        if re.compile("(.)\\1+").match(w):
            # 單字相疊
            new_content += w[0]
        else:
            # 雙字相疊
            new_content += w[:2]
        last_end = match.end()
    if last_end < len(content):
        new_content += content[last_end:]
    return content if len(new_content) == 0 else new_content
