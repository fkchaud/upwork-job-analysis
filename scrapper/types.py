from typing import TypedDict

from typing_extensions import NotRequired


class AtomJobDict(TypedDict):
    job_url: str
    title: str
    description: str
    budget: NotRequired[int]
    post_date: str
    category: str
    skills: list[str]
    country: str
