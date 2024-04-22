try:
  import pytest
  if __name__ == '__main__':
    import os
    base = os.path.dirname(__file__)
    pytest.main([base, '--verbose'])
except ImportError:
  ...