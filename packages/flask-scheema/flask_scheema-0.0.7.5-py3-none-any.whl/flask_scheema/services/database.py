from functools import wraps
from typing import Callable, Union, Dict, List, Optional, Any
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

import sqlalchemy
from flask import request
from sqlalchemy import desc, inspect, Column, and_, func, ForeignKey
from sqlalchemy.exc import IntegrityError, DataError
from sqlalchemy.orm import Query, Session, class_mapper

from flask_scheema.api.utils import get_primary_keys
from flask_scheema.exceptions import CustomHTTPException
from flask_scheema.services.operators import (
    aggregate_funcs,
    get_pagination,
    get_all_columns_and_hybrids,
    get_select_fields,
    create_conditions_from_args,
    get_models_for_join,
    get_table_and_column,
    get_column_and_table_name_and_operator,
    get_check_table_columns,
)
from flask_scheema.specification.utilities import get_related_classes_and_attributes
from flask_scheema.utilities import get_config_or_model_meta


def add_dict_to_query(f: Callable) -> Callable:
    """
    Adds a dictionary to the query result, this is for they result is an SQLAlchemy result object and not an ORM model,
    used when there are custom queries, etc.

    Returns:
        dict: Dictionary containing a query result and count.

    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        output = f(*args, **kwargs)
        if isinstance(output, dict):
            try:
                if isinstance(output["query"], list):
                    output["dictionary"] = [
                        result._asdict() for result in output["query"]
                    ]
                output["dictionary"] = output["query"]._asdict()

            except AttributeError:
                pass

        return output

    return decorated_function


def add_page_totals_and_urls(f: Callable) -> Callable:
    """
        Adds page totals and urls to the query result.

    Args:
            f (Callable): The function to decorate.

        Returns:
            Callable: The decorated function.

    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        """
                Gets the output of the function and append the page totals and urls to the output.

        Args:
            **kwargs:
        Returns:

        """
        output = f(*args, **kwargs)
        limit = output.get("limit")
        page = output.get("page")
        total_count = output.get("total_count")

        parsed_url = urlparse(request.url)
        query_params = parse_qs(parsed_url.query)

        next_url = None
        previous_url = None
        current_page = None
        total_pages = None

        # Calculate total_pages and current_page
        if total_count and limit:
            total_pages = -(
                -total_count // limit
            )  # Equivalent to math.ceil(count / limit)
            current_page = page

            # Update the 'page' query parameter for the next and previous URLs
            query_params["limit"] = [str(limit)]
            query_params["page"] = [str(page + 1)]
            next_query_string = urlencode(query_params, doseq=True)

            query_params["page"] = [str(page - 1)]
            prev_query_string = urlencode(query_params, doseq=True)

            # Determine if there are next and previous pages
            next_page = page + 1 if (page + 1) * limit < total_count else None
            prev_page = page - 1 if page > 1 else None

            # Construct next and previous URLs
            next_url = (
                urlunparse(parsed_url._replace(query=next_query_string))
                if next_page is not None
                else None
            )
            previous_url = (
                urlunparse(parsed_url._replace(query=prev_query_string))
                if prev_page is not None
                else None
            )

        if isinstance(output, dict):
            try:
                output["next_url"] = next_url
                output["previous_url"] = previous_url
                output["current_page"] = current_page
                output["total_pages"] = total_pages
            except AttributeError:
                pass

        return output

    return decorated_function


def apply_pagination(query: Union[Query], page: int = 0, limit: int = 20) -> list[Any]:
    """
        Paginates a given query.


    Args:
            query (Query): Original SQLAlchemy query.
            page (int): Page number for pagination.
            limit (int): Number of items per page.

        Returns:
            Query: Paginated query results.
    """
    return query.paginate(page=page, per_page=limit, error_out=False)


def apply_order_by(args_dict: Dict, query: Query, base_model: callable) -> Query:
    """
        Applies order_by conditions to a query.
        Use "-" prefix for descending order.
        Example: "-id,name"


    Args:
        args_dict (dict): Dictionary containing filtering and pagination conditions.
        query (Query): The query to sort.
        base_model (Base): The base model for the query.

    Returns:
        Query: The sorted query.
    """

    if "order_by" in args_dict:
        order_by = args_dict["order_by"]
        if isinstance(order_by, str):
            order_by = order_by.split(",")

        for order_key in order_by:
            descending = False
            if order_key.startswith("-"):
                descending = True
                order_key = order_key[1:]

            column = get_table_and_column(order_key, base_model)
            if column:
                if descending:
                    query = query.order_by(desc(order_key))
                else:
                    query = query.order_by(order_key)

    return query


class CrudService:
    def __init__(self, model, session: Session):
        """
                Initializes the CrudService instance.


        Args:
            model (Callable): SQLAlchemy model class for CRUD operations.
            session (Session): SQLAlchemy session.

        """
        self.model = model
        self.session = session

    def get_model_by_name(self, field_name: str):
        """
                Gets a model by name.

        Args:
            field_name (str): The name of the model to get.

        Returns:
            object: The model class.

        Raises:
            Exception: If the model does not have a relationship with the current model.

        """

        # Check for relationships between the fetched model and self.model
        relationships = inspect(self.model).relationships
        related_model = relationships.get(field_name)

        if related_model is None:
            raise CustomHTTPException(
                401,
                f"Field {field_name} does not represent a relationship in model {self.model.__name__}",
            )

        return related_model.mapper.class_

    def get_query_from_args(self, args_dict: Dict[str, Union[str, int]]) -> Query:
        """
                Filters a query based on request arguments. Handles filtering, sorting, pagination and aggregation.

        Args:
            args_dict (dict): Dictionary containing filtering and pagination conditions.

        Returns:
            Query: The filtered query.

        """
        # columns in the model

        # get the models to join
        join_models: Dict = get_models_for_join(args_dict, self.get_model_by_name)

        # get all columns in the model
        all_columns, all_models = get_all_columns_and_hybrids(
            self.model, join_models
        )  # table name, column name, column

        # create the conditions
        conditions: List = [
            x
            for x in create_conditions_from_args(
                args_dict, self.model, all_columns, all_models, join_models
            )
            if x is not None
        ]

        # # create the aggregates
        # aggregates: Optional[Dict[str, Optional[str]]] = create_aggregate_conditions(
        #     args_dict
        # )

        # # apply the aggregates
        # if aggregates:
        #     aggregate_columns = self.calculate_aggregates(aggregates, all_columns)
        #     # combine the select fields with the aggregate columns
        #     select_fields = select_fields + aggregate_columns

        # get the select fields
        allow_select = get_config_or_model_meta(
            "API_ALLOW_SELECT_FIELDS", model=self.model, default=True
        )
        query = None
        if allow_select:
            select_fields: List[Callable] = get_select_fields(
                args_dict, self.model, all_columns
            )
            # create the query
            if select_fields:
                query: Query = self.session.query(*select_fields)

        if not query:
            query: Query = self.session.query(self.model)

        # # join the models
        # for k, v in join_models.items():
        #     query = query.join(v)

        # groupby_columns: List[Callable] = get_group_by_fields(
        #     args_dict, all_columns, self.model
        # )
        # # apply the groupby
        # if groupby_columns:
        #     query = query.group_by(*groupby_columns)

        # apply the conditions
        if conditions and get_config_or_model_meta(
            "API_ALLOW_FILTER", model=self.model, default=True
        ):
            query = query.filter(and_(*conditions))

        # Handle Sorting
        if get_config_or_model_meta(
            "API_ALLOW_ORDER_BY", model=self.model, default=True
        ):
            query = apply_order_by(args_dict, query, self.model)

        return query

    def calculate_aggregates(
        self, aggregate_conditions: Dict, all_columns: Dict[str, Dict[str, Column]]
    ):
        """
                Applies aggregate conditions to a query and returns the aggregated query.


        Args:
            aggregate_conditions (Dict): List of aggregate conditions.
            all_columns (dict): Dictionary of all columns in the model.

        Returns:
            List: List of aggregated columns.


        """
        # Separate groupby from other aggregate functions
        aggregate_columns = []

        for key, value in aggregate_conditions.items():
            column_name, table_name, agg_func = get_column_and_table_name_and_operator(
                key, self.model
            )
            column, column_name = get_check_table_columns(
                table_name, column_name, all_columns
            )

            aggregate_func = aggregate_funcs.get(agg_func)
            if aggregate_func:
                # added this so we can have the label if we want it
                column = aggregate_func(column)
                if value:
                    column = column.label(value)
                aggregate_columns.append(column)

        # Apply other aggregate functions
        # if aggregate_columns:
        #     query = query.with_entities(*aggregate_columns)
        #
        # # Apply groupby first, if exists
        # if groupby_columns:
        #     query = query.group_by(*groupby_columns)

        return aggregate_columns

    def add_soft_delete_filter(self, query):
        show_deleted = request.args.get("include_deleted", None)
        deleted_attr = get_config_or_model_meta(
            "API_SOFT_DELETE_ATTRIBUTE", default=None
        )
        soft_delete_values = get_config_or_model_meta(
            "API_SOFT_DELETE_VALUES", default=False
        )

        if not show_deleted and deleted_attr:
            # Identify all unique models (or aliased models) in the query
            models = set()
            for desc in query.column_descriptions:
                if desc["type"] is not None:
                    # Use inspect and getattr to check for aliased or direct models
                    insp = inspect(desc["entity"])
                    model = getattr(insp, "mapper", None).class_ if insp else None
                    if model:
                        models.add(model)

            # Apply the filter to all identified models
            for model in models:
                if hasattr(model, deleted_attr):
                    deleted_column = getattr(model, deleted_attr)
                    if isinstance(soft_delete_values, list) and soft_delete_values:
                        query = query.filter(deleted_column == soft_delete_values[0])
                    else:
                        # Handle case where soft_delete_values is not a list or is an empty list
                        query = query.filter(deleted_column == soft_delete_values[0])

        return query

    @add_page_totals_and_urls
    @add_dict_to_query
    def get_query(
        self,
        args_dict: Dict[str, Union[str, int]],
        lookup_val: Optional[Union[int, str]] = None,
        alt_field: Optional[str] = None,
        many: Optional[bool] = True,
        other_model=None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
                Retrieves a list of objects from the database, optionally paginated.


        Args:
            args_dict (dict): Dictionary containing filtering and pagination conditions.
                Extracts 'order_by' from args_dict for sorting. Use "-" prefix for descending order.
            lookup_val (Optional[int]): The id of the object to return.
            alt_field (Optional[str]): An alternative field to search by.
            many (Optional[bool]): Whether to return many objects or not.
            other_model (db.model): The model to join with.

        Returns:
            dict: Dictionary containing a query result and count.

        """
        pk = get_primary_keys(self.model)
        query = self.get_query_from_args(args_dict)

        soft_delete = get_config_or_model_meta("API_SOFT_DELETE", default=False)
        if soft_delete:
            query = self.add_soft_delete_filter(query)

        if lookup_val:  # and not multiple:

            if alt_field:
                query = query.filter_by(**{alt_field: lookup_val})
            else:
                query = query.filter(pk == lookup_val)

            if many:
                results = query.all()
            else:
                results = query.first()

            if not results:
                raise CustomHTTPException(
                    404, f"{self.model.__name__} not found with {pk.key} {lookup_val}"
                )

            return {"query": results}

        else:

            if other_model:
                pk = get_primary_keys(other_model)
                query = query.join(other_model).filter(pk == lookup_val)

            count = self.session.query(func.count()).select_from(query).scalar()
            page, limit = get_pagination(args_dict)
            if page or limit:
                query = apply_pagination(query, page, limit)

            if hasattr(query, "all"):
                results = query.all()
            else:
                results = query.items

            return {
                "query": results,
                "total_count": count,
                "page": page,
                "limit": limit,
            }

    def create(self, **kwargs) -> object:
        """
        Creates a new object in the database, based on the provided data.

        Args:
            kwargs (dict): A dictionary of data to create the object with.

        Returns:
            object: The newly created SQLAlchemy object.

        """
        body = kwargs.get("deserialized_data")
        if not body:
            raise CustomHTTPException(400, "No data provided for creation.")

        try:
            new_model = self.model(**body)
            self.session.add(new_model)
            self.session.commit()
            return {"query": new_model}
        except IntegrityError as e:
            self.session.rollback()
            # Log the error as well if logging is setup
            # logging.error(f"IntegrityError: {e}")
            raise CustomHTTPException(400, f"Integrity error: {e.orig}")
        except DataError as e:
            self.session.rollback()
            # Log the error as well if logging is setup
            # logging.error(f"DataError: {e}")
            raise CustomHTTPException(400, f"Data error: {e.orig}")
        except Exception as e:
            self.session.rollback()
            # Catch-all for any other unforeseen errors
            # logging.error(f"Unexpected error: {e}")
            raise CustomHTTPException(500, "An unexpected error occurred.")

    def update(self, **kwargs) -> dict:
        """
        Updates an object in the database, based on the provided id and data.

        Kwargs:
            lookup_val (int): The id of the object to update.
            deserialized_data (dict): The data to update the object with.

        Returns:
            dict: The updated object if successful, or an error message if not.
        """
        lookup_val = kwargs.get("lookup_val")
        if not lookup_val:
            raise CustomHTTPException(400, "No lookup value provided for update.")

        obj = self.get_query(request.args.to_dict(), lookup_val, many=False)["query"]
        if obj:
            body = kwargs.get("deserialized_data")
            if body is None:
                raise CustomHTTPException(400, "No data provided for update.")
            try:
                for key, value in body.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                    else:
                        raise CustomHTTPException(
                            400, f"Invalid field '{key}' for update."
                        )
                self.session.commit()
                return {"query": obj}

            except Exception as e:
                self.session.rollback()
                raise CustomHTTPException(500, f"Unexpected error during update: {e}")
        else:
            raise CustomHTTPException(404, "Object not found for update.")

    def delete(self, *args, **kwargs) -> dict:
        """
        Deletes an object from the database, with optional cascading delete.
        If cascade_delete is True, deletes the object and its related objects.
        If not_null_only is True, only deletes related objects with not null constraints.

        Kwargs:
            lookup_val (int): The ID of the object to delete.
            cascade_delete (bool, optional): Whether to cascade delete. Defaults to False.
            not_null_only (bool, optional): Whether to delete only related objects with not null constraints. Defaults to False.

        Returns:
            dict: "complete": True if the object was successfully deleted, False otherwise.
        """
        lookup_val = kwargs.get("lookup_val")
        if not lookup_val:
            raise CustomHTTPException(400, "No lookup value provided for deletion.")

        # Extract query parameters for cascade_delete and not_null_only
        args = request.args.to_dict()

        allow_delete_related = get_config_or_model_meta(
            "API_ALLOW_DELETE_RELATED", model=self.model, default=True
        )
        allow_delete_dependants = get_config_or_model_meta(
            "API_ALLOW_DELETE_DEPENDENTS", model=self.model, default=True
        )
        delete_related = args.get("delete_related", "")
        delete_dependents = args.get("delete_dependents", "").lower() in [
            "1",
            "true",
        ]
        related_models = get_related_classes_and_attributes(self.model)

        obj = self.get_query(kwargs, lookup_val, many=False)["query"]

        if not obj:
            raise CustomHTTPException(404, "Object not found for deletion.")

        if delete_related and not allow_delete_related:
            raise CustomHTTPException(400, "Deleting related models is not allowed.")

        if delete_dependents and not allow_delete_dependants:
            raise CustomHTTPException(
                400, "Recursively deleting dependant models is not allowed."
            )

        try:
            with self.session.no_autoflush:
                if delete_related:
                    for attr in delete_related.split(","):
                        try:
                            related_attr, related_cls = [
                                x for x in related_models if attr in x[1]
                            ]
                            if related_attr:
                                self.delete_related(related_attr)
                        except ValueError as e:
                            raise CustomHTTPException(
                                409, f"Related attribute {attr} not found."
                            )

                if delete_dependents:
                    # Recursively delete all related objects
                    self.delete_dependents(obj)

                self.delete_or_soft(obj)
                self.session.commit()
                return {"complete": True}

        except sqlalchemy.exc.IntegrityError as e:
            self.session.rollback()

            related = [x[1].strip() for x in related_models]

            error_message = f"Deletion blocked by related data."
            if allow_delete_related:
                error_message += " You can use the 'delete_related' query parameter to delete related objects directly adjacent to this resource."
            if allow_delete_dependants:
                error_message += " You can use the 'delete_dependants=1' query parameter to delete all dependant objects."

            raise CustomHTTPException(409, error_message)

    def delete_related(self, related_attribute):
        """
        Deletes related objects from the database.
        """

        values = getattr(self.model, related_attribute)
        if isinstance(values, (list, tuple, set)):
            for value in values:
                self.delete_or_soft(value)
        else:

            self.delete_or_soft(values)

    def delete_dependents(self, obj, processed=None):
        """
        Recursively delete objects that are solely dependent on the parent object,
        using a set of processed items to avoid infinite recursion.
        """
        if processed is None:
            processed = set()

        processed.add(obj)

        # Iterate over all relationships of the object's class to find dependent objects
        for relationship in class_mapper(obj.__class__).relationships:
            related_obj = getattr(obj, relationship.key, None)

            if related_obj is not None:
                if isinstance(related_obj, (list, set)):
                    for item in related_obj:
                        if item not in processed and self.has_dependent_existence(
                            obj, relationship
                        ):
                            self.delete_dependents(item, processed)
                            self.delete_or_soft(item)
                            processed.add(item)
                else:
                    if related_obj not in processed and self.has_dependent_existence(
                        obj, relationship
                    ):
                        self.delete_dependents(related_obj, processed)
                        self.delete_or_soft(related_obj)
                        processed.add(related_obj)

    def has_dependent_existence(self, obj, relationship):
        """
        Determines if the relationship indicates a dependent existence of the related object.
        """
        # Check if the relationship is configured with delete or delete-orphan cascade
        is_cascade_delete = (
            "delete" in relationship.cascade or "delete-orphan" in relationship.cascade
        )

        # Correctly check for non-nullable foreign keys in the relationship
        has_non_nullable_fk = False
        for fk in relationship.remote_side:
            # Access the column directly from the ForeignKey, checking its nullable property
            if not fk.nullable:
                has_non_nullable_fk = True
                break

        # Advanced: Consider polymorphic identities if applicable, indicating potential dependency
        # This section remains speculative as detailed previously
        is_polymorphic_dependent = False
        # Your polymorphic dependency logic here...

        # Determine dependency based on relationship attributes and additional logic
        is_dependent = (
            is_cascade_delete or has_non_nullable_fk or is_polymorphic_dependent
        )
        return is_dependent

    def delete_or_soft(self, obj):
        soft_delete = get_config_or_model_meta("API_SOFT_DELETE", default=False)
        soft_delete_attr = get_config_or_model_meta(
            "API_SOFT_DELETE_ATTRIBUTE", default=None
        )
        soft_delete_vals = get_config_or_model_meta(
            "API_SOFT_DELETE_VALUES", default=None
        )
        if soft_delete:
            setattr(obj, soft_delete_attr, soft_delete_vals[1])
        else:
            self.session.delete(obj)
