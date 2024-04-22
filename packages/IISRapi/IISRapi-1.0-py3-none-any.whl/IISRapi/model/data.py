from typing import NamedTuple,List,Tuple

class Data(NamedTuple):
    ori_txt: str
    ret_txt: str=None
    ner_tags: List[Tuple[str, int, int]] = None
    punct: List[Tuple[str, int]] = None

