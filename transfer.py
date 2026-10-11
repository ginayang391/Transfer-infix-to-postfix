#11420343楊詠晴
# -*- coding: utf-8 -*-
import re
from operator import add, sub, mul, truediv

OPS = {'+': (1, add), '-': (1, sub), '*': (2, mul), '/': (2, truediv), '^': (3, pow)}


def tokenize(s):
    """切分 token：數字（多位數/小數）、運算子、括號；空白略過"""
    tokens = re.findall(r'\d+\.?\d*|\.\d+|[-+*/^()]|\S', s)
    for t in tokens:
        if not (t[0].isdigit() or t[0] == '.' or t in OPS or t in '()'):
            raise ValueError(f"無法辨識的字元：{t}")
    return tokens


def to_postfix(tokens):
    """調車場演算法：中序 -> 後序"""
    out, st = [], []
    for t in tokens:
        if t in OPS:
            # 堆疊頂優先權較高，或相同且為左結合(非 ^)時，先彈出
            while st and st[-1] != '(' and (OPS[st[-1]][0] > OPS[t][0] or
                                            (OPS[st[-1]][0] == OPS[t][0] and t != '^')):
                out.append(st.pop())
            st.append(t)
        elif t == '(':
            st.append(t)
        elif t == ')':
            while st and st[-1] != '(':
                out.append(st.pop())
            if not st:
                raise ValueError("括號不對稱：多了 ')'")
            st.pop()
        else:
            out.append(t)
    while st:
        if st[-1] == '(':
            raise ValueError("括號不對稱：缺少 ')'")
        out.append(st.pop())
    return out


def evaluate(postfix):
    """堆疊求值後序式"""
    st = []
    for t in postfix:
        if t in OPS:
            if len(st) < 2:
                raise ValueError("運算式錯誤：運算元不足")
            b, a = st.pop(), st.pop()
            if t == '/' and b == 0:
                raise ZeroDivisionError("除以零")
            st.append(OPS[t][1](a, b))
        else:
            st.append(float(t))
    if len(st) != 1:
        raise ValueError("運算式錯誤：缺少運算子或運算元")
    return st[0]


def run(expr):
    print(f"中序式：{expr}")
    try:
        post = to_postfix(tokenize(expr))
        r = evaluate(post)
        print(f"後序式：{' '.join(post)}")
        print(f"結果：{int(r) if r == int(r) else r}")
        return r
    except (ValueError, ZeroDivisionError, OverflowError) as e:
        print(f"[錯誤] {e}")


if __name__ == "__main__":
    print("=== 內建測資 ===")
    for expr, expect in [("(6 + 4) * 5", 50), ("(56 + 12) * 3 - 4", 200)]:
        print("驗證：", "通過" if run(expr) == expect else "失敗", "\n")

    print("=== 互動模式（輸入 q 離開）===")
    while (s := input("請輸入運算式 > ").strip()).lower() != 'q':
        if s:
            run(s)
