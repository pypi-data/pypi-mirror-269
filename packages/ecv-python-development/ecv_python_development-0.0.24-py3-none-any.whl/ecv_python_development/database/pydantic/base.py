from __future__ import annotations

from typing import Any, Callable, List, Optional

from pydantic import Field

"""
check full documentation for fields at: https://docs.pydantic.dev/latest/concepts/fields/

"""


def field(
    default: Optional[str] = None,
    default_factory: Optional[Callable[..., Any]] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    validation_alias: Optional[str] = None,
    serialization_alias: Optional[str] = None,
    examples: Optional[List[Any]] = None,
    exclude: Optional[str] = None,
) -> Any:

    parameters = {
        key: value
        for key, value in locals().items()
        if value is not None and key != "parameters"
    }
    """
    These are the parameters I find to be extremely useful.
    
    I limited the parameters to this for easier readability. 
    
    This custom field is to enforce strict types.
    
    """
    return Field(**parameters, strict=True)


"""
Sample Implementation

from uuid import UUID, uuid4

class User(BaseModel):
    id: UUID = field(default_factory=uuid4)
    name: str = field(default="John Doe", min_length=1, description="name of the User")
    
user = User(name="warren")
print(user.json())

"""
