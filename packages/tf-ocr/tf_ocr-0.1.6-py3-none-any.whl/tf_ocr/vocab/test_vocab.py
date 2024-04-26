from hypothesis import given, example, strategies as st
from .vocab import VOCABULARY, vectorize, stringify

# cache StringLookups
vectorize('1')
stringify(1)

@given(st.text(VOCABULARY, min_size=1, max_size=1))
def test_inverse1(x: str):
  assert stringify(vectorize(x)) == x
  
@given(st.integers(min_value=0, max_value=len(VOCABULARY)))
@example(0)
def test_inverse2(x: int):
  assert vectorize(stringify(x)) == x