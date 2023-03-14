from typing import Tuple, Optional


def fast_median_approx(data : Tuple[int], indices : Tuple[int], chunk_size : int) -> int :
    len_indices = len(indices)
    assert len_indices > 0

    if len_indices == 1 :
        return indices[0]

    offset = 0
    recur_indices = []
    while True :
        if offset >= len_indices : break
        indices_chunk : Tuple[int] = indices[offset:min(offset+chunk_size, len_indices)]
        sorted_chunk = sorted(tuple((data[index], index) for index in indices_chunk))
        median = sorted_chunk[len(sorted_chunk) // 2][1]
        recur_indices.append(median)
        offset += chunk_size

    recur_indices = tuple(recur_indices)
    return fast_median_approx(data, recur_indices, chunk_size)

def split(data : Tuple[int], pivot : int) -> Tuple[Tuple[int, ...], Tuple[int, ...]] :
    less = tuple(index for (index, num) in enumerate(data) if num < pivot)
    more = tuple(index for (index, num) in enumerate(data) if num > pivot)
    return less, more


class LazyQuantile :
    def __init__(self, vs : Tuple[int, ...], ws : Tuple[int, ...], offset: int):
        assert len(vs) == len(ws)

        # branch field
        self.v : Optional[int] = None
        self.w : Optional[int] = None
        self.l : Optional[LazyQuantile] = None
        self.r : Optional[LazyQuantile] = None

        # leaf field
        self.vs = vs
        self.ws = ws

        # quantile range
        self.min = offset
        self.max = offset + sum(self.ws, 0)

    def get_quantile(self, w) -> Optional[int] :

        # lazy split
        if self.v is None :
            # empty node
            if len(self.vs) == 0 :
                return None

            else :
                median_index = fast_median_approx(self.vs, tuple(i for i in range(len(self.vs))), 5)
                self.v = self.vs[median_index]
                self.w = self.ws[median_index]
                left, right = split(self.vs, self.v)
                self.l = LazyQuantile(tuple(self.vs[index] for index in left), tuple(self.ws[index] for index in left), self.min)
                self.min = self.l.max
                self.max = self.min + self.w
                self.r = LazyQuantile(tuple(self.vs[index] for index in right), tuple(self.ws[index] for index in right), self.max)
                self.vs = None
                self.ws = None

        if self.min <= w < self.max :
            return self.v
        elif self.min > w :
            return self.l.get_quantile(w)
        else :
            return self.r.get_quantile(w)

def main():
    vs = (4, 3, 1, 6, 5, 9)
    ws = (2, 7, 3, 4, 8, 9)
    Q = LazyQuantile(vs, ws, 0)

    print(f'{Q.get_quantile(10)=}')
    print(f'{Q.get_quantile(11)=}')
    print(f'{Q.get_quantile(11)=}')
    print(f'{Q.get_quantile(-1)=}')
    print(f'{Q.get_quantile(100)=}')

if __name__ == '__main__':
    main()
