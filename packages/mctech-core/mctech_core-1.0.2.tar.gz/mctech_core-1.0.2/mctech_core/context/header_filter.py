from typing import List, Literal, Callable

GroupName = Literal['tracing', 'misc', 'extras']


class PatternFilter:
    def __init__(self, group: GroupName, match: Callable[[str], bool]):
        self.group = group
        self.match = match


PATTERNS: List[PatternFilter] = [
    PatternFilter(
        group='tracing',
        match=lambda n: n == 'x-request-id' or n == 'x-ot-span-context'
    ),
    PatternFilter(
        group='tracing',
        match=lambda n: n.startswith('x-b3-')
    ),
    PatternFilter(
        group='miscHeaders',
        match=lambda n: n.startswith('x-forwarded-')
    )]


def process(headers: List[str], group: GroupName) -> List[str]:
    result: List[str] = []
    # 排除所有不是以'x-'开头的key
    for header in filter(lambda h: h.startswith('x-'), headers):
        # 排除满足$excludes集合中条件的
        pattern = next(filter(lambda p: p.match(header), PATTERNS), None)
        if pattern:
            if group == pattern.group:
                result.append(header)
        elif group == 'extras':
            result.append(header)
    return result
