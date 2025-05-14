from dataclasses import dataclass, field
from library.random_number_utils import RandomUtils

@dataclass(frozen=True, order=True, slots=True)
class Book:
    name: str
    author: str
    id: str = field(default_factory=RandomUtils.generate_random_id)

    @property
    def search_string(self):
        return f"{self.name} {self.author}"
