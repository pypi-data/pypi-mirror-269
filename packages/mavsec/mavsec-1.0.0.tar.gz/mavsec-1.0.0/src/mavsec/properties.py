#####################################################################################
# A tool for the creation of JasperGold SVP principle tcl files.
# Copyright (C) 2024  RISCY-Lib Contributors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#####################################################################################

from __future__ import annotations
from typing import ClassVar, Any, TypeAlias

import enum

from dataclasses import dataclass, field
from mavsec.general import ProjectCheckResult
from mavsec.schema import Schema

import jinja2


def tcl_escape_string(s: str) -> str:
  """Escapes a string for TCL."""
  s = s.replace("{", "\\{").replace("}", "\\}")
  s = s.replace("[", "\\[").replace("]", "\\]")
  s = s.replace(" ", "").replace("\n", "").replace("\t", "")
  return s


class SpecialRtlPaths(enum.StrEnum):
  """Enum for special RTL paths."""
  OUTPUTS = enum.auto()
  INPUTS = enum.auto()

  @classmethod
  def from_str(cls, s: str) -> SpecialRtlPaths:
    """Converts a string to a special RTL path."""
    if s.lower() in ["outputs", "@outputs"]:
      return cls.OUTPUTS
    if s.lower() in ["inputs", "@inputs"]:
      return cls.INPUTS
    raise ValueError(f"Special RTL path {s} not found.")

  def design_info(self) -> str:
    if self == SpecialRtlPaths.OUTPUTS:
      return "output"
    if self == SpecialRtlPaths.INPUTS:
      return "input"
    raise ValueError(f"Special RTL path {self} not found.")

AnyRtlPath = str | SpecialRtlPaths


@dataclass
class PropertyType():

  name: str
  """The name of the property type."""
  description: str
  """A brief description of the property type."""
  meta: dict[str, type | TypeAlias] = field(default_factory=dict)
  """The information needed to generate the property."""
  spv: str | list[str] | None = None
  """The SVP principle in jinja for the property type."""

  property_types: ClassVar[dict[str, PropertyType]] = {}

  def __post_init__(self):
    if self.name in self.property_types:
      raise ValueError(f"Property type {self.name} already exists.")

    self.property_types[self.name] = self

  @classmethod
  def get_type(cls, name: str) -> PropertyType:
    """Gets a property type by name."""
    if name not in cls.property_types:
      raise ValueError(f"Property type {name} not found.")
    return cls.property_types[name]

  def check(self, meta: dict, name: str) -> ProjectCheckResult:
    """Check the property type."""
    ret_val = ProjectCheckResult()

    for key, val in self.meta.items():
      if key not in meta:
        ret_val.design_error(f"Property {name} (type {self.name}) missing value for {key}.")
      elif not isinstance(meta[key], val):
        ret_val.design_error(f"Property {name} (type {self.name}) value {key} is not type {val}.")
      elif isinstance(meta[key], str):
        if meta[key] == '':
          ret_val.design_error(f"Property {name} (type {self.name}) value {key} is empty.")

    return ret_val


SecureKeyProperty = PropertyType(
  "SecureKey",
  "A property that ensures a given key is stored correctly.",
  {"key_loc": AnyRtlPath, "key_size": int, "public_bus": AnyRtlPath},
  "check_spv -create -name {{ name }} -from {{ key_loc }} -to {{ public_bus }}{{precond}}"
)

SecureKeyIntegrityProperty = PropertyType(
  "SecureKeyIntegrity",
  "A property that ensures a given key is not overwritten incorrectly.",
  {"key_loc": AnyRtlPath, "key_size": int, "public_bus": AnyRtlPath},
  "check_spv -create -name {{ name }} -from {{ public_bus }} -to {{ key_loc }}{{precond}}"
)

SecureKeyGenProperty = PropertyType(
  "SecureKeyGen",
  "A property that ensures a given generated key is stored correctly.",
  {
    "public_key_loc": AnyRtlPath,
    "private_key_loc": AnyRtlPath,
    "key_size": int,
    "public_bus": AnyRtlPath
  },
  [
    "check_spv -create -name {{ name }}_priv2bus -from {{ private_key_loc }} -to {{ public_bus }}{{precond}}",  # noqa: E501
    "check_spv -create -name {{ name }}_priv2pub -from {{ private_key_loc }} -to {{ public_key_loc }}{{precond}}"  # noqa: E501
  ]
)

SecureExternalMemoryProperty = PropertyType(
  "SecureExternalMemory",
  "A property that ensures a given external memory is secure.",
  {"memory_if": AnyRtlPath, "memory_controller": AnyRtlPath, "public_bus": AnyRtlPath},
  [
    "check_spv -create -name {{ name }}_bus -from {{ public_bus }} -to {{ memory_if }}{{precond}}",  # noqa: E501
    "check_spv -create -name {{ name }}_ctrl -from {{ memory_controller }} -to {{ memory_if }}{{precond}}"  # noqa: E501
  ]
)

SecureInternalStorageProperty = PropertyType(
  "SecureInternalStorage",
  "A property that ensures a given internal storage is not able to be accessed.",
  {"storage_loc": AnyRtlPath, "storage_size": int, "public_bus": AnyRtlPath},
  "check_spv -create -name {{ name }} -from {{ storage_loc }} -to {{ public_bus }}{{precond}}"
)

FaultTolerantFSMProperty = PropertyType(
  "FaultTolerantFSM",
  "A property that ensures a given FSM is fault tolerant.",
  {"fsm_state": AnyRtlPath, "inputs": AnyRtlPath, "outputs": AnyRtlPath},
)


@dataclass
class Property(Schema):
  name: str
  """The name of the property."""
  description: str
  """A brief description of the property."""
  meta: dict[str, Any] = field(default_factory=dict)
  """A dictionary of metadata for the property."""
  ptype: PropertyType | str | None = None
  """The type of the property."""
  preconditions: list[str] | None = None
  """The preconditions for the property."""

  def __post_init__(self):
    if isinstance(self.ptype, str):
      for ptype_name in PropertyType.property_types.keys():
        if ptype_name == self.ptype:
          self.ptype = PropertyType.property_types[ptype_name]
          break
      else:
        raise ValueError(f"Property type {self.ptype} not found.")

  def type_name(self) -> str:
    """Gets the name of the property type."""
    if isinstance(self.ptype, PropertyType):
      return self.ptype.name
    return str(self.ptype)

  def set_preconditions(self, preconditions: str | list[str]) -> None:
    """Sets the preconditions for the property."""
    if isinstance(preconditions, str):
      self.preconditions = preconditions.split("\n")
    else:
      self.preconditions = preconditions

    preconds: list[str] = []
    for precond in self.preconditions:
      pc = precond.strip()
      if pc != "":
        preconds.append(pc)

    self.preconditions = preconds

  def get_preconditions(self) -> str:
    """Gets the preconditions for the property."""
    if self.preconditions is None:
      return ""
    return "\n".join(self.preconditions)

  def to_svp(self) -> str:
    """Converts the property to an SVP principle."""
    if self.ptype is None:
      return f"# No property type available for {self.name}."
    if isinstance(self.ptype, str):
      self.ptype = PropertyType.get_type(self.ptype)

    if self.ptype.spv is None:
      return f"# No SVP principle available for {self.name} ({self.ptype.name})."

    # Create the loops to handle multiple inputs/outputs
    loops: dict[str, SpecialRtlPaths] = {}
    for key, val in self.meta.items():
      if isinstance(val, str) and val.startswith("@"):
        loops[key] = SpecialRtlPaths.from_str(val[1:])

    print(loops)

    ret_val = ""
    indent_level = 0
    for loop_key, loop_val in loops.items():
      ret_val += "    " * indent_level
      ret_val += f"foreach {loop_key} in [get_design_info -list {loop_val.design_info()}] {'{'}\n"
      indent_level += 1

    # For each precondition, create an SVP principle
    preconditions: list[str] = []

    if self.preconditions is None:
      preconditions.append("")
    elif isinstance(self.preconditions, str):
      preconditions.append(self.preconditions)
    else:
      preconditions.extend(self.preconditions)

    spvs = self.ptype.spv
    if not isinstance(spvs, list):
      spvs = [spvs]

    for idx, precond in enumerate(preconditions):
      name = self.name
      loop_names = "_".join([f"${'{'}{key}{'}'}" for key in loops.keys()])
      if precond != "":
        name = f"{tcl_escape_string(self.name)}{loop_names}_precond{idx}"
      else:
        name = f"{tcl_escape_string(self.name)}{loop_names}"

      for spv in spvs:
        ret_val += "    " * indent_level
        ret_val += jinja2.Template(spv).render(
          name=name,
          precond=" -to_precond " + tcl_escape_string(precond) if precond != "" else "",
          **self.meta
        )
        ret_val += "\n"

    # Add closing for each loop
    for _ in loops.keys():
      indent_level -= 1
      ret_val += "    " * indent_level
      ret_val += "}\n"

    return ret_val

  def check(self) -> ProjectCheckResult:
    """Check the property."""
    ret_val = ProjectCheckResult()

    if self.name == '':
      ret_val.security_error("Property name not set.")
    if self.description == '':
      ret_val.security_warning(f"Property ({self.name}) description not set.")
    if self.ptype is None:
      ret_val.security_error(f"Property ({self.name}) type not set.")
      return ret_val

    if isinstance(self.ptype, str):
      self.ptype = PropertyType.get_type(self.ptype)

    return ret_val.merge(self.ptype.check(self.meta, self.name))

  @classmethod
  def ptype_from_str(cls, prop: str) -> PropertyType:
    """Gets a property type from a string."""
    for ptype in PropertyType.property_types.values():
      if ptype.name == prop:
        return ptype
    raise ValueError(f"Property type {prop} not found.")

  @classmethod
  def from_dict(cls, d: dict) -> Property:
    """Converts the SVP principle to a property."""
    if "preconditions" not in d:
      d["preconditions"] = None

    return cls(
      name=d["name"],
      description=d["description"],
      meta=d["meta"],
      ptype=cls.ptype_from_str(d["ptype"]),
      preconditions=d["preconditions"]
    )

  @classmethod
  def available_types(cls) -> list[PropertyType]:
    """Returns all the available property types."""
    return list(PropertyType.property_types.values())

  def to_dict(self) -> dict:
    """Convert the object to a dictionary."""
    ret_val = {
        "name": self.name,
        "description": self.description,
        "meta": self.meta,
        "ptype": self.type_name(),
      }

    if self.preconditions is not None:
      ret_val["preconditions"] = self.preconditions

    return ret_val
