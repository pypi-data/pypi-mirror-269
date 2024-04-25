import copy
import enum
import json
import os
import pathlib
import shutil
import signal
import sys
import tempfile
import threading
from typing import Any, Dict, Iterator, List, Mapping, Optional, Sequence


def jsonify(
    documents: Sequence[Mapping[str, Any]],
    collection_name: str,
    database_name: str,
    path: str | pathlib.Path = "~/.jsonable/db.json",
) -> None:
    """Jsonify documents as a JSON file.

    Args:
        documents (Sequence[Mapping[str, Any]]): Documents to jsonify.
        path (str): Path to the JSON file.
        database_name (str): Name of the database.
        collection_name (str): Name of the collection.
    """
    client = Client(path)
    collection = client[database_name][collection_name]
    collection.insert(documents)


class Client(object):
    """Client for jsonableDB."""

    def __init__(
        self,
        path: str | pathlib.Path = "~/.jsonable/db.json",
    ) -> None:
        """Initialize the client given a path to a JSON file.

        Args:
            path (str | pathlib.Path): Path to the JSON file.
        """
        path = pathlib.Path(path)
        if str(path).startswith("~"):
            path = path.expanduser()
        self._path = path
        self._data = None
        self.load()  # automatically load
        self._dump_thread = None
        self.set_sigterm_handler()  # automatically set

    def __contains__(self, database_name: str) -> bool:
        """Syntactic sugar for the method `contains_database()`."""
        return self.contains_database(database_name)

    def __iter__(self) -> Iterator[str]:
        """Syntactic sugar for the method `list_database_names()`."""
        return iter(self.list_database_names())

    def __getitem__(self, database_name: str) -> "Database":
        """Syntactic sugar for the method `get_database()`."""
        return self.get_database(database_name)

    def __setitem__(self, database_name: str, database: "Database") -> bool:
        raise NotImplementedError

    def __delitem__(self, database_name: str) -> bool:
        """Syntactic sugar for the method `drop_database()`."""
        return self.drop_database(database_name)

    def _load(self) -> None:
        """Deserialize a JSON file to a Python dictionary."""
        try:
            with open(self._path, mode="rt", encoding="utf-8") as file:
                self._data = json.load(file)
        except ValueError:
            if self._path.stat().st_size == 0:  # file is empty
                self._data = {}
            else:  # file is not empty but not valid JSON
                raise RuntimeError

    @property
    def uri(self) -> str:
        """File URI of the JSON file."""
        return self._path.absolute().as_uri()

    def load(self) -> None:
        """Load data from a JSON file.

        Loading is automatic. This method should be never called in public.
        """
        if self._path.exists():  # file exists
            self._load()
        else:  # file does not exist
            self._path.parent.mkdir(exist_ok=True, parents=True)
            self._data = {}

    def set_sigterm_handler(self) -> None:
        """Assigns SIGTERM handler for graceful shutdown during dumping.

        Setting is automatic. This method should be never called in public.
        """

        def sigterm_handler(*args, **kwargs):
            if self._dump_thread is not None:
                self._dump_thread.join()
            sys.exit(0)

        signal.signal(signal.SIGTERM, sigterm_handler)

    def _dump(self) -> None:
        """Serialize a Python dictionary to a temporary file, then move to a
        JSON file.
        """
        with tempfile.NamedTemporaryFile(
            mode="wt",
            encoding="utf-8",
            delete=False,
        ) as file:
            json.dump(self._data, file, ensure_ascii=False, indent=4)
        if os.stat(file.name).st_size != 0:  # file is not empty
            shutil.move(file.name, self._path)

    def dump(self) -> None:
        """Dump data to a JSON file.

        Dumping is automatic. This method should be never called in public.
        """
        self._dump_thread = threading.Thread(target=self._dump)
        self._dump_thread.start()
        self._dump_thread.join()

    def contains_database(self, name: str) -> bool:
        """Check if a database with the given name exists or not.

        Args:
            name (str): Name of the database to check.

        Returns:
            bool: `True` if the database already exists, `False` otherwise.
        """
        if not isinstance(name, str):
            raise TypeError("database name must be a string")
        return name in self._data

    def list_database_names(self) -> List[str]:
        """Get a list of the names of all databases.

        Returns:
            List[str]: A list of the names of all databases.
        """
        return list(self._data)

    def list_databases(self) -> List["Database"]:
        """Get a list of all databases.

        Returns:
            List[Database]: A list of all databases.
        """
        return [Database(self, name) for name in self._data]

    def create_database(self, name: str) -> "Database":
        """Create a new database.

        Database creation is automatic. This method should be never called in public.

        Args:
            name (str): Name of the database to create.

        Returns:
            Database: The newly created database.
        """
        if self.contains_database(name):  # database already exists
            raise RuntimeError
        return Database(self, name)

    def get_database(self, name: str) -> "Database":
        """Get a database with the given name.

        If the database does not exist, it will be created automatically.

        Args:
            name (str): Name of the database to get.

        Returns:
            Database: The database with the given name.
        """
        if not self.contains_database(name):  # database does not exist
            return self.create_database(name)
        return Database(self, name)

    def drop_database(self, name: str) -> bool:
        """Drop a database with the given name.

        Args:
            name (str): Name of the database to drop.

        Returns:
            bool: `True` if the database was dropped successfully, `False` otherwise.
        """
        if not self.contains_database(name):  # database does not exist
            return False
        del self._data[name]
        self.dump()  # automatically dump
        return True


class Database(object):
    """Database level operations for jsonableDB."""

    def __init__(self, client: Client, name: str) -> None:
        """Get or create a new database.

        Args:
            client (Client): Client to get or create the database in.
            name (str): Name of the database.
        """
        if not isinstance(name, str):
            raise TypeError("database name must be a string")
        self.client = client
        self.name = name
        if self.name in self.client:  # database already exists
            self._data = self.client._data[self.name]
        else:  # database does not exist
            self._data = {}
            self.client._data[self.name] = self._data
            self.client.dump()  # automatically dump

    def __contains__(self, collection_name: str) -> bool:
        """Syntactic sugar for the method `contains_collection()`."""
        return self.contains_collection(collection_name)

    def __iter__(self) -> Iterator[str]:
        """Syntactic sugar for the method `list_collection_names()`."""
        return iter(self.list_collection_names())

    def __getitem__(self, collection_name: str) -> "Collection":
        """Syntactic sugar for the method `get_collection()`."""
        return self.get_collection(collection_name)

    def __setitem__(
        self, collection_name: str, collection: "Collection"
    ) -> bool:
        raise NotImplementedError

    def __delitem__(self, collection_name: str) -> bool:
        """Syntactic sugar for the method `drop_collection()`."""
        return self.drop_collection(collection_name)

    def dump(self) -> None:
        """Dump data to the JSON file.

        Dumping is automatic. This method should be never called in public.
        """
        self.client.dump()

    def contains_collection(self, name: str) -> bool:
        """Check if a collection with the given name exists or not in the database.

        Args:
            name (str): Name of the collection to check.

        Returns:
            bool: `True` if the collection already exists, `False` otherwise.
        """
        if not isinstance(name, str):
            raise TypeError("collection name must be a string")
        return name in self._data

    def list_collection_names(self) -> List[str]:
        """Get a list of the names of all collections in the database.

        Returns:
            List[str]: A list of the names of all collections in the database.
        """
        return list(self._data)

    def list_collections(self) -> List["Collection"]:
        """Get a list of all collections in the database.

        Returns:
            List[Collection]: A list of all collections in the database.
        """
        return [Collection(self, name) for name in self._data]

    def create_collection(self, name: str) -> "Collection":
        """Create a new collection in the database.

        Collection creation is automatic. This method should be never called in public.

        Args:
            name (str): Name of the collection to create.

        Returns:
            Collection: The newly created collection in the database.
        """
        if self.contains_collection(name):  # collection already exists
            raise RuntimeError
        return Collection(self, name)

    def get_collection(self, name: str) -> "Collection":
        """Get a collection with the given name in the database.

        If the collection does not exist, it will be created automatically.

        Args:
            collection_name (str): Name of the collection to get.

        Returns:
            Collection: The collection with the given name in the database.
        """
        if not self.contains_collection(name):  # collection does not exist
            return self.create_collection(name)
        return Collection(self, name)

    def drop_collection(self, name: str) -> bool:
        """Drop a collection with the given name in the database.

        Args:
            name (str): Name of the collection to drop.

        Returns:
            bool: `True` if the collection was dropped successfully, `False` otherwise.
        """
        if not self.contains_collection(name):  # collection does not exist
            return False
        del self._data[name]
        self.dump()  # automatically dump
        return True


class Collection(object):
    """Collection level operations for jsonableDB."""

    def __init__(self, database: Database, name: str) -> None:
        """Get or create a collection.

        Args:
            database (Database): Database to get or create a collection in.
            name (str): Name of the collection.
        """
        if not isinstance(name, str):
            raise TypeError("collection name must be a string")
        self.database = database
        self.name = name
        if self.name in self.database:  # collection already exists
            self._data = self.database._data[self.name]
        else:  # collection does not exist
            self._data = []
            self.database._data[self.name] = self._data
            self.database.dump()  # automatically dump

    def __len__(self) -> int:
        """Get the number of documents in the collection."""
        return len(self._data)

    def __iter__(self) -> Iterator["Document"]:
        """Get an iterator of the documents in the collection."""
        return iter(self._data)

    def dump(self) -> None:
        """Dump data to the JSON file.

        Dumping is automatic. This method should be never called in public.
        """
        self.database.dump()

    def insert_one(self, document: Mapping[str, Any]) -> None:
        """Insert a single document into the collection.

        Args:
            document (Document): Document to insert.
        """
        try:
            document = copy.deepcopy(dict(document))
        except TypeError:
            raise TypeError("document must be a mapping")
        if not document:
            raise ValueError("document cannot be empty")
        for key, value in document.items():
            if not isinstance(key, str):
                raise TypeError("document keys must be strings")
            # TODO: check value types
        self._data.append(document)
        self.dump()  # automatically dump

    def insert(self, documents: Sequence[Mapping[str, Any]]) -> None:
        """Insert document(s) into the collection.

        Args:
            documents (Sequence[Mapping[str, Any]]): Document(s) to insert.
        """
        for document in documents:
            self.insert_one(document)

    def find(
        self,
        filter: Optional[Mapping[str, Any]] = None,
        sort: Optional[Mapping[str, Any]] = None,
    ) -> List["Document"]:
        """Get all documents from the collection that match the given filter.

        Args:
            filter (Mapping[str, Any], optional): Filter to apply. Defaults to
        `None` to include all documents.
            sort (Mapping[str, Any], optional): Sort order to apply. Defaults to
        `None` to not sort the matching documents.

        Returns:
            List[Document]: All the documents that match the given filter.
        """
        if filter is None:  # without filter
            data = copy.deepcopy(self._data)
        else:  # with filter
            try:
                filter = dict(filter)
            except TypeError:
                raise TypeError("filter must be a mapping")
            data = copy.deepcopy(self._data)
            for key, value in filter.items():
                if not isinstance(key, str):
                    raise TypeError("filter keys must be strings")
                data = copy.deepcopy([d for d in data if d[key] == value])
        if sort is None:  # without sort
            return data
        else:  # with sort
            try:
                sort = dict(sort)
            except TypeError:
                raise TypeError("sort must be a mapping")
            if len(list(sort.items())) != 1:
                raise ValueError("sort must have exactly one key-value pair")
            key, value = list(sort.items())[0]
            if not isinstance(key, str):
                raise TypeError("sort keys must be strings")
            if not isinstance(value, SortOrder):
                raise TypeError(
                    "sort values must be either `jsonable.SortOrder.Ascending` or `jsonable.SortOrder.Descending`"
                )
            return sorted(data, key=lambda x: x[key], reverse=value.value)

    def delete(self, filter: Optional[Mapping[str, Any]] = None) -> None:
        if filter is None:  # without filter
            self._data = []
        else:  # with filter
            documents = self.find(filter=filter)
            for document in documents:
                self._data.remove(document)
        self.dump()  # automatically dump

    def update(self, filter: Optional[Mapping[str, Any]] = None) -> None:
        raise NotImplementedError


Document = Dict[str, Any]


class SortOrder(enum.Enum):

    ASCENDING = False
    DESCENDING = True
