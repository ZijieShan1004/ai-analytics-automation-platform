from pydantic import BaseModel


class Page(BaseModel):
    items: list
    total: int
    page: int
    size: int


# Create a simple in-memory page response.
def paginate(items: list, page: int = 1, size: int = 20) -> Page:
    start = (page - 1) * size
    end = start + size
    return Page(items=items[start:end], total=len(items), page=page, size=size)