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

from dataclasses import dataclass, field


@dataclass
class ProjectCheckResult:
  """Class to represent the information when a project is checked."""

  project_errors: list[str] = field(default_factory=list)
  """Errors found in the project setup."""
  project_warnings: list[str] = field(default_factory=list)
  """Warnings found in the project setup."""
  security_errors: list[str] = field(default_factory=list)
  """Errors found during the security handoff check."""
  security_warnings: list[str] = field(default_factory=list)
  """Warnings found during the security handoff check."""
  design_errors: list[str] = field(default_factory=list)
  """Errors found during the design handoff check."""
  design_warnings: list[str] = field(default_factory=list)
  """Warnings found during the design handoff check."""

  def project_error(self, msg: str) -> None:
    """Add an error to the project errors list.

    Args:
        msg (str): The error message.
    """
    self.project_errors.append(msg)

  def project_warning(self, msg: str) -> None:
    """Add a warning to the project warnings list.\

    Args:
        msg (str): The warning message.
    """
    self.project_warnings.append(msg)

  def security_error(self, msg: str) -> None:
    """Add an error to the security errors list.

    Args:
        msg (str): The error message.
    """
    self.security_errors.append(msg)

  def security_warning(self, msg: str) -> None:
    """Add a warning to the security warnings list.

    Args:
        msg (str): The warning message.
    """
    self.security_warnings.append(msg)

  def design_error(self, msg: str) -> None:
    """Add an error to the design errors list.

    Args:
        msg (str): The error message.
    """
    self.design_errors.append(msg)

  def design_warning(self, msg: str) -> None:
    """Add a warning to the design warnings list.

    Args:
        msg (str): The warning message.
    """
    self.design_warnings.append(msg)

  def has_warnings(self) -> bool:
    """Check if there are any warnings.

    Returns:
        bool: True if there are warnings or errors, False otherwise.
    """
    return bool(
      self.project_warnings or self.security_warnings or self.design_warnings or
      self.has_errors()
    )

  def has_errors(self) -> bool:
    """Check if there are any errors.

    Returns:
        bool: True if there are errors, False otherwise.
    """
    return bool(self.project_errors or self.security_errors or self.design_errors)

  def merge(self, other: ProjectCheckResult) -> ProjectCheckResult:
    """Merge two ProjectCheckResult objects.

    Args:
        other (ProjectCheckResult): The other object to merge.

    Returns:
        ProjectCheckResult: The merged object.
    """
    return ProjectCheckResult(
      project_errors=self.project_errors + other.project_errors,
      project_warnings=self.project_warnings + other.project_warnings,
      security_errors=self.security_errors + other.security_errors,
      security_warnings=self.security_warnings + other.security_warnings,
      design_errors=self.design_errors + other.design_errors,
      design_warnings=self.design_warnings + other.design_warnings,
    )

  def merge_into(self, other: ProjectCheckResult) -> None:
    """Merge two ProjectCheckResult objects into this object.

    Args:
        other (ProjectCheckResult): The other object to merge.
    """
    self.project_errors += other.project_errors
    self.project_warnings += other.project_warnings
    self.security_errors += other.security_errors
    self.security_warnings += other.security_warnings
    self.design_errors += other.design_errors
    self.design_warnings += other.design_warnings

  def to_dict(self) -> dict[str, list[str]]:
    """Convert the object to a dictionary.

    Returns:
        dict: The dictionary.
    """
    ret_val = {}

    if len(self.project_errors) != 0:
      ret_val["project_errors"] = self.project_errors
    if len(self.project_warnings) != 0:
      ret_val["project_warnings"] = self.project_warnings
    if len(self.security_errors) != 0:
      ret_val["security_errors"] = self.security_errors
    if len(self.security_warnings) != 0:
      ret_val["security_warnings"] = self.security_warnings
    if len(self.design_errors) != 0:
      ret_val["design_errors"] = self.design_errors
    if len(self.design_warnings) != 0:
      ret_val["design_warnings"] = self.design_warnings

    return ret_val
