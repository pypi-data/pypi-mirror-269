# coding: utf-8

"""
    Trieve API

    Trieve OpenAPI Specification. This document describes all of the operations available through the Trieve API.

    The version of the OpenAPI document: 0.7.2
    Contact: developers@trieve.ai
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from trieve_py_client.models.chunk_filter import ChunkFilter
from typing import Optional, Set
from typing_extensions import Self

class RecommendChunksRequest(BaseModel):
    """
    RecommendChunksRequest
    """ # noqa: E501
    filters: Optional[ChunkFilter] = None
    limit: Optional[Annotated[int, Field(strict=True, ge=0)]] = Field(default=None, description="The number of chunks to return. This is the number of chunks which will be returned in the response. The default is 10.")
    negative_chunk_ids: Optional[List[StrictStr]] = Field(default=None, description="The ids of the chunks to be used as negative examples for the recommendation. The chunks in this array will be used to filter out similar chunks.")
    negative_tracking_ids: Optional[List[StrictStr]] = Field(default=None, description="The tracking_ids of the chunks to be used as negative examples for the recommendation. The chunks in this array will be used to filter out similar chunks.")
    positive_chunk_ids: Optional[List[StrictStr]] = Field(default=None, description="The ids of the chunks to be used as positive examples for the recommendation. The chunks in this array will be used to find similar chunks.")
    positive_tracking_ids: Optional[List[StrictStr]] = Field(default=None, description="The tracking_ids of the chunks to be used as positive examples for the recommendation. The chunks in this array will be used to find similar chunks.")
    recommend_type: Optional[StrictStr] = Field(default=None, description="The type of recommendation to make. This lets you choose whether to recommend based off of `semantic` or `fulltext` similarity. The default is `semantic`.")
    slim_chunks: Optional[StrictBool] = Field(default=None, description="Set slim_chunks to true to avoid returning the content and chunk_html of the chunks. This is useful for when you want to reduce amount of data over the wire for latency improvement. Default is false.")
    strategy: Optional[StrictStr] = Field(default=None, description="Strategy to use for recommendations, either \"average_vector\" or \"best_score\". The default is \"average_vector\". The \"average_vector\" strategy will construct a single average vector from the positive and negative samples then use it to perform a pseudo-search. The \"best_score\" strategy is more advanced and navigates the HNSW with a heuristic of picking edges where the point is closer to the positive samples than it is the negatives.")
    __properties: ClassVar[List[str]] = ["filters", "limit", "negative_chunk_ids", "negative_tracking_ids", "positive_chunk_ids", "positive_tracking_ids", "recommend_type", "slim_chunks", "strategy"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of RecommendChunksRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of filters
        if self.filters:
            _dict['filters'] = self.filters.to_dict()
        # set to None if filters (nullable) is None
        # and model_fields_set contains the field
        if self.filters is None and "filters" in self.model_fields_set:
            _dict['filters'] = None

        # set to None if limit (nullable) is None
        # and model_fields_set contains the field
        if self.limit is None and "limit" in self.model_fields_set:
            _dict['limit'] = None

        # set to None if negative_chunk_ids (nullable) is None
        # and model_fields_set contains the field
        if self.negative_chunk_ids is None and "negative_chunk_ids" in self.model_fields_set:
            _dict['negative_chunk_ids'] = None

        # set to None if negative_tracking_ids (nullable) is None
        # and model_fields_set contains the field
        if self.negative_tracking_ids is None and "negative_tracking_ids" in self.model_fields_set:
            _dict['negative_tracking_ids'] = None

        # set to None if positive_chunk_ids (nullable) is None
        # and model_fields_set contains the field
        if self.positive_chunk_ids is None and "positive_chunk_ids" in self.model_fields_set:
            _dict['positive_chunk_ids'] = None

        # set to None if positive_tracking_ids (nullable) is None
        # and model_fields_set contains the field
        if self.positive_tracking_ids is None and "positive_tracking_ids" in self.model_fields_set:
            _dict['positive_tracking_ids'] = None

        # set to None if recommend_type (nullable) is None
        # and model_fields_set contains the field
        if self.recommend_type is None and "recommend_type" in self.model_fields_set:
            _dict['recommend_type'] = None

        # set to None if slim_chunks (nullable) is None
        # and model_fields_set contains the field
        if self.slim_chunks is None and "slim_chunks" in self.model_fields_set:
            _dict['slim_chunks'] = None

        # set to None if strategy (nullable) is None
        # and model_fields_set contains the field
        if self.strategy is None and "strategy" in self.model_fields_set:
            _dict['strategy'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RecommendChunksRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "filters": ChunkFilter.from_dict(obj["filters"]) if obj.get("filters") is not None else None,
            "limit": obj.get("limit"),
            "negative_chunk_ids": obj.get("negative_chunk_ids"),
            "negative_tracking_ids": obj.get("negative_tracking_ids"),
            "positive_chunk_ids": obj.get("positive_chunk_ids"),
            "positive_tracking_ids": obj.get("positive_tracking_ids"),
            "recommend_type": obj.get("recommend_type"),
            "slim_chunks": obj.get("slim_chunks"),
            "strategy": obj.get("strategy")
        })
        return _obj


