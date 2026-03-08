from __future__ import annotations

from threading import Lock

from app.schemas import ProductRecord


class InMemoryProductStore:
    def __init__(self) -> None:
        self._records: dict[str, ProductRecord] = {}
        self._lock = Lock()

    def put(self, record: ProductRecord) -> None:
        with self._lock:
            self._records[record.product_id] = record

    def get(self, product_id: str) -> ProductRecord | None:
        return self._records.get(product_id)

    def update(self, product_id: str, record: ProductRecord) -> None:
        with self._lock:
            self._records[product_id] = record


store = InMemoryProductStore()
