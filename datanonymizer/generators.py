class DataGenerator:
    def __init__(self, provider, unique_retries_limit: int = 10, **kwargs):
        self.provider = provider
        self.already_seen = {}
        self.bloom_filter = set()
        self.unique_retries_limit = unique_retries_limit
        self.kwargs = kwargs

    def __call__(self, value):
        if value not in self.already_seen:
            for _ in range(self.unique_retries_limit):
                result = self.provider(**self.kwargs)
                hashed = hash(result)
                if hashed not in self.bloom_filter:
                    self.bloom_filter.add(hashed)
                    break
            else:
                raise ValueError(f"Cannot provide an unique value for {self}")

            self.already_seen[value] = result

        return self.already_seen[value]
