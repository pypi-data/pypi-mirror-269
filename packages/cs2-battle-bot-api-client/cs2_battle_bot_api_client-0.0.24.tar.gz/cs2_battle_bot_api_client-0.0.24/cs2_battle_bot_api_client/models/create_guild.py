from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CreateGuild")


@_attrs_define
class CreateGuild:
    """
    Attributes:
        name (str):
        guild_id (str):
        owner_id (str):
        owner_username (str):
    """

    name: str
    guild_id: str
    owner_id: str
    owner_username: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        name = self.name

        guild_id = self.guild_id

        owner_id = self.owner_id

        owner_username = self.owner_username

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "name": name,
                "guild_id": guild_id,
                "owner_id": owner_id,
                "owner_username": owner_username,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        guild_id = d.pop("guild_id")

        owner_id = d.pop("owner_id")

        owner_username = d.pop("owner_username")

        create_guild = cls(
            name=name,
            guild_id=guild_id,
            owner_id=owner_id,
            owner_username=owner_username,
        )

        create_guild.additional_properties = d
        return create_guild

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
