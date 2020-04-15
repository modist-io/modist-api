# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Stephen Bunn <stephen@bunn.io>
# ISC License <https://opensource.org/licenses/isc>

"""Custom Alembic operations for our own nuances."""

from typing import Any, Optional

from alembic.operations import Operations, MigrateOperation


@Operations.register_operation("create_refresh_updated_at_trigger")
class CreateRefreshUpdatedAtTriggerOperation(MigrateOperation):
    """The Alembic operation to create a ``updated_at`` trigger attached to a table."""

    def __init__(self, table_name: str, schema_name: str = "public"):
        """Initialize the Alembic operation for creating an ``updated_at`` trigger.

        :param str table_name: The name of the table to attach the trigger to
        :param str schema_name: The name of the schema which the given table lives in,
            optional, defaults to "public"
        """

        self.table_name = table_name
        self.schema_name = schema_name

    @classmethod
    def create_refresh_updated_at_trigger(
        cls, operations, table_name: str, **kwargs
    ) -> Any:
        """Invoke the create ``udpated_at`` trigger operation.

        :param operations: The Alembic operations context to invoke the current
            operation within
        :param str table_name: The name of the table to invoke the create
            trigger operation with
        :return: The response of the invoked operation
        :rtype: Any
        """

        return operations.invoke(cls(table_name, **kwargs))

    def reverse(self) -> Any:
        """Trigger the operation to reverse the create ``updated_at`` trigger operation.

        :return: The result of the reverse operation
        :rtype: Any
        """

        return DropRefreshUpdatedAtTriggerOperation(
            self.table_name, schema_name=self.schema_name
        )


@Operations.register_operation("drop_refresh_updated_at_trigger")
class DropRefreshUpdatedAtTriggerOperation(MigrateOperation):
    """The Alembic operation to drop an ``updated_at`` trigger attached to a table."""

    def __init__(self, table_name: str, schema_name: str = "public"):
        """Initialize the Alembic operation for dropping an ``updated_at`` trigger.

        :param str table_name: The name of the table to drop the trigger from
        :param str schema_name: The name of the schema which the given table lives in,
            optional, defaults to "public"
        """

        self.table_name = table_name
        self.schema_name = schema_name

    @classmethod
    def drop_refresh_updated_at_trigger(
        cls, operations, table_name: str, **kwargs
    ) -> Any:
        """Invoke the drop ``udpated_at`` trigger operation.

        :param operations: The Alembic operations context to invoke the current
            operation within
        :param str table_name: The name of the table to invoke the drop
            trigger operation with
        :return: The response of the invoked operation
        :rtype: Any
        """

        return operations.invoke(cls(table_name, **kwargs))

    def reverse(self) -> Any:
        """Trigger the operation to reverse the drop ``updated_at`` trigger operation.

        :return: The result of the reverse operation
        :rtype: Any
        """

        return CreateRefreshUpdatedAtTriggerOperation(
            self.table_name, schema_name=self.schema_name
        )


@Operations.implementation_for(CreateRefreshUpdatedAtTriggerOperation)
def create_refresh_updated_at_trigger(
    operations, operation: CreateRefreshUpdatedAtTriggerOperation
) -> Any:
    """Create an trigger to automatically update ``updated_at`` on a given table.

    :param operations: The Alembic operation context to execute the operation within
    :param CreateRefreshUpdatedAtTriggerOperation operation: The operation context
    :return: The result of the execution of the creation of the trigger
    :rtype: Any
    """

    return operations.execute(
        f"CREATE TRIGGER {operation.table_name!s}_refresh_updated_at_trigger "
        f"BEFORE UPDATE ON {operation.schema_name!s}.{operation.table_name!s} "
        "FOR EACH ROW EXECUTE PROCEDURE refresh_updated_at()"
    )


@Operations.implementation_for(DropRefreshUpdatedAtTriggerOperation)
def drop_refresh_updated_at_trigger(
    operations, operation: DropRefreshUpdatedAtTriggerOperation
) -> Any:
    """Drop an existing trigger on a given table that automatically updates ``updated_at``.

    :param operations: The Alembic operation context to execute the operation within
    :param DropRefreshUpdatedAtTriggerOperation operation: The operation context
    :return: The result of the execution of the dropping of the trigger
    :rtype: Any
    """

    operations.execute(
        f"DROP TRIGGER IF EXISTS {operation.table_name!s}_refresh_updated_at_trigger "
        f"ON {operation.schema_name!s}.{operation.table_name!s}"
    )


@Operations.register_operation("create_refresh_depth_and_lineage_trigger")
class CreateRefreshDepthAndLineageTriggerOperation(MigrateOperation):
    """The Alembic operation to create a ``refresh_depth_and_lineage`` trigger."""

    def __init__(self, table_name: str, schema_name: str = "public"):
        """Alembic operation for creating a ``refresh_depth_and_lineage`` trigger.

        :param str table_name: The name of the table to create the trigger in
        :param str schema_name: The name of the schema which the given table lives in,
            optional, defaults to "public"
        """

        self.table_name = table_name
        self.schema_name = schema_name

    @classmethod
    def create_refresh_depth_and_lineage_trigger(
        cls, operations, table_name: str, **kwargs
    ) -> Any:
        """Invoke the create ``refresh_depth_and_lineage`` trigger operation.

        :param operations: The Alembic operations context to invoke the current
            operation within
        :param str table_name: The name of the table to invoke the create
            trigger operation with
        :return: The response of the invoked operation
        :rtype: Any
        """

        return operations.invoke(cls(table_name, **kwargs))

    def reverse(self) -> Any:
        """Trigger the reverse of the create ``refresh_depth_and_lineage`` trigger operation.

        :return: The result of the reverse operation
        :rtype: Any
        """

        return DropRefreshDepthAndLineageTriggerOperation(
            self.table_name, schema_name=self.schema_name
        )


@Operations.register_operation("drop_refresh_depth_and_lineage_trigger")
class DropRefreshDepthAndLineageTriggerOperation(MigrateOperation):
    """The Alembic operation to drop an ``refresh_depth_and_lineage`` trigger."""

    def __init__(self, table_name: str, schema_name: str = "public"):
        """Alembic operation for dropping a ``refresh_depth_and_lineage`` trigger.

        :param str table_name: The name of the table to drop the trigger from
        :param str schema_name: The name of the schema which the given table lives in,
            optional, defaults to "public"
        """

        self.table_name = table_name
        self.schema_name = schema_name

    @classmethod
    def drop_refresh_depth_and_lineage_trigger(
        cls, operations, table_name: str, **kwargs
    ) -> Any:
        """Invoke the drop ``refresh_depth_and_lineage`` trigger operation.

        :param operations: The Alembic operations context to invoke the current
            operation within
        :param str table_name: The name of the table to invoke the drop trigger
            opreation with
        :return: The response of the invoked operation
        :rtype: Any
        """

        return operations.invoke(cls(table_name, **kwargs))

    def reverse(self) -> Any:
        """Trigger the reverse of the drop ``refresh_depth_and_lineage`` trigger operation.

        :return: The result of the reverse operation
        :rtype: Any
        """

        return CreateRefreshDepthAndLineageTriggerOperation(
            self.table_name, schema_name=self.schema_name
        )


@Operations.implementation_for(CreateRefreshDepthAndLineageTriggerOperation)
def create_refresh_depth_and_lineage_trigger(
    operations, operation: CreateRefreshDepthAndLineageTriggerOperation
) -> Any:
    """Create an trigger to automatically call ``refresh_depth_and_lineage``.

    :param operations: The Alembic operation context to execute the operation within
    :param CreateRefreshUpdatedAtTriggerOperation operation: The operation context
    :return: The result of the execution of the creation of the trigger
    :rtype: Any
    """

    return operations.execute(
        f"CREATE TRIGGER {operation.table_name!s}_refresh_depth_and_lineage_trigger "
        f"BEFORE INSERT OR UPDATE ON {operation.schema_name!s}.{operation.table_name!s}"
        " FOR EACH ROW EXECUTE PROCEDURE refresh_depth_and_lineage()"
    )


@Operations.implementation_for(DropRefreshDepthAndLineageTriggerOperation)
def drop_refresh_depth_and_lineage_trigger(
    operations, operation: DropRefreshDepthAndLineageTriggerOperation
) -> Any:
    """Drop an existing trigger on a given table that calls ``refresh_depth_and_lineage``.

    :param operations: The Alembic operation context to execute the operation within
    :param DropRefreshUpdatedAtTriggerOperation operation: The operation context
    :return: The result of the execution of the dropping of the trigger
    :rtype: Any
    """

    operations.execute(
        "DROP TRIGGER IF EXISTS "
        f"{operation.table_name!s}_refresh_depth_and_lineage_trigger "
        f"ON {operation.schema_name!s}.{operation.table_name!s}"
    )
