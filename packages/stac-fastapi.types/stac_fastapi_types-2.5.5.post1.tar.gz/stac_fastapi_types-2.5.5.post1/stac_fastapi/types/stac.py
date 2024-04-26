"""STAC types."""
import sys
from typing import Any, Dict, List, Literal, Optional, Union

from stac_pydantic.shared import BBox

# Avoids a Pydantic error:
# TypeError: You should use `typing_extensions.TypedDict` instead of
# `typing.TypedDict` with Python < 3.9.2.  Without it, there is no way to
# differentiate required and optional fields when subclassed.
if sys.version_info < (3, 9, 2):
    from typing_extensions import TypedDict
else:
    from typing import TypedDict

NumType = Union[float, int]


class LandingPage(TypedDict, total=False):
    """STAC Landing Page."""

    type: str
    stac_version: str
    stac_extensions: Optional[List[str]]
    id: str
    title: str
    description: str
    conformsTo: List[str]
    links: List[Dict[str, Any]]


class Conformance(TypedDict):
    """STAC Conformance Classes."""

    conformsTo: List[str]


class Catalog(TypedDict, total=False):
    """STAC Catalog."""

    type: str
    stac_version: str
    stac_extensions: Optional[List[str]]
    id: str
    title: Optional[str]
    description: str
    links: List[Dict[str, Any]]


class Collection(Catalog, total=False):
    """STAC Collection."""

    keywords: List[str]
    license: str
    providers: List[Dict[str, Any]]
    extent: Dict[str, Any]
    summaries: Dict[str, Any]
    assets: Dict[str, Any]


class Item(TypedDict, total=False):
    """STAC Item."""

    type: Literal["Feature"]
    stac_version: str
    stac_extensions: Optional[List[str]]
    id: str
    geometry: Dict[str, Any]
    bbox: BBox
    properties: Dict[str, Any]
    links: List[Dict[str, Any]]
    assets: Dict[str, Any]
    collection: str


class ItemCollection(TypedDict, total=False):
    """STAC Item Collection."""

    type: Literal["FeatureCollection"]
    features: List[Item]
    links: List[Dict[str, Any]]
    context: Optional[Dict[str, int]]


class Collections(TypedDict, total=False):
    """All collections endpoint.

    https://github.com/radiantearth/stac-api-spec/tree/master/collections
    """

    collections: List[Collection]
    links: List[Dict[str, Any]]
