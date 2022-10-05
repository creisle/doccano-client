from __future__ import annotations

from typing import Generic, List, Optional, TypeVar

from doccano_client.models.label import Category, Label, Span
from doccano_client.repositories.label import LabelRepository
from doccano_client.repositories.label_type import LabelTypeRepository

T = TypeVar("T", bound=Label)


class LabelUseCase(Generic[T]):
    def __init__(self, repository: LabelRepository, label_type_repository: LabelTypeRepository = None):
        self._repository = repository
        self._label_type_repository = label_type_repository

    def find_by_id(self, project_id: int, example_id: int, label_id: int) -> T:
        """Find a label by id

        Args:
            project_id (int): The id of the project to find
            example_id (int): The id of the example
            label_id (int): The id of the label to find

        Returns:
            T: The found label
        """
        return self._repository.find_by_id(project_id, example_id, label_id)

    def list(self, project_id: int, example_id: int) -> List[T]:
        """Return all labels

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example

        Returns:
            T: The labels in the project.
        """
        return self._repository.list(project_id, example_id)

    def delete(self, project_id: int, example_id: int, label_id: int):
        """Delete a label.

        Args:
            project_id (int): The project id
            example_id (int): The id of the example
            label_id (int): The label id
        """
        label = self.find_by_id(project_id, example_id, label_id)
        self._repository.delete(project_id, label)

    def delete_all(self, project_id: int, example_id: int):
        """Delete all labels

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
        """
        self._repository.delete_all(project_id, example_id)


class CategoryUseCase(LabelUseCase[Category]):
    def create(
        self, project_id: int, example_id: int, label: int | str, human_annotated=False, confidence=0.0
    ) -> Category:
        """Create a new category label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Category: The created category label

        Raises:
            ValueError: If the label type repository is not set
        """
        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id  # type: ignore

        category = Category(example=example_id, label=label, manual=human_annotated, prob=confidence)
        return self._repository.create(project_id, category)

    def update(
        self,
        project_id: int,
        example_id: int,
        label_id: int,
        label: Optional[int | str] = None,
        human_annotated: bool = None,
        confidence: float = None,
    ) -> Category:
        """Update a category label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label_id (int): The id of the label
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Category: The updated category label

        Raises:
            ValueError: If the label type repository is not set
        """
        category = self.find_by_id(project_id, example_id, label_id)

        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id  # type: ignore

        category = Category(
            id=category.id,
            example=example_id,
            label=label or category.label,
            manual=human_annotated or category.manual,
            prob=confidence or category.prob,
        )
        return self._repository.update(project_id, category)


class SpanUseCase(LabelUseCase[Span]):
    def create(
        self,
        project_id: int,
        example_id: int,
        start_offset: int,
        end_offset: int,
        label: int | str,
        human_annotated: bool = False,
        confidence: float = 0.0,
    ) -> Span:
        """Create a new span label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            start_offset (int): The start offset of the span
            end_offset (int): The end offset of the span
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Span: The created span label

        Raises:
            ValueError: If the label type repository is not set
        """
        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id  # type: ignore

        span = Span(
            example=example_id,
            start_offset=start_offset,
            end_offset=end_offset,
            label=label,
            manual=human_annotated,
            prob=confidence,
        )
        return self._repository.create(project_id, span)

    def update(
        self,
        project_id: int,
        example_id: int,
        label_id: int,
        start_offset: Optional[int] = None,
        end_offset: Optional[int] = None,
        label: Optional[int | str] = None,
        human_annotated: bool = None,
        confidence: float = None,
    ) -> Span:
        """Update a span label

        Args:
            project_id (int): The id of the project
            example_id (int): The id of the example
            label_id (int): The id of the label
            start_offset (int): The start offset of the span
            end_offset (int): The end offset of the span
            label (int | str): The label to create
            human_annotated (bool): Whether the label is human annotated. Defaults to False.
            confidence (float): The confidence of the label. Defaults to 0.0.

        Returns:
            Span: The updated span label

        Raises:
            ValueError: If the label type repository is not set
        """
        span = self.find_by_id(project_id, example_id, label_id)

        if self._label_type_repository is None:
            raise ValueError("LabelTypeRepository is not set")

        if isinstance(label, str):
            label_type = self._label_type_repository.find_by_name(project_id, label)
            label = label_type.id

        span = Span(
            id=span.id,
            example=example_id,
            start_offset=start_offset or span.start_offset,
            end_offset=end_offset or span.end_offset,
            label=label or span.label,
            manual=human_annotated or span.manual,
            prob=confidence or span.prob,
        )
        return self._repository.update(project_id, span)
