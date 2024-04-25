# -*- coding: UTF-8 -*-
""""
Created on 24.01.22
Module for reading document datasets.

:author:     Martin Dočekal
"""

import inspect
import math
import multiprocessing
import traceback
from abc import ABC, abstractmethod

from typing import Union, List, Generator, Optional, Any, Callable

from windpyutils.parallel.own_proc_pools import FunctorWorker, FunctorWorkerFactory, FactoryFunctorPool

from oapapersloader.document import Document


class DocumentDataset(ABC):
    """
    Abstract class for datasets of documents.

    :ivar stub_mode: True activates stub mode which provides stub documents.
        Stub documents are documents that might not contain whole content, but just short "preview".
        Also, the citation matching (matching bibliography in dataset) might be omitted.
    """

    def __init__(self):
        self._transform = None
        self._transform_with_index = False
        self.stub_mode = False
        self.preload_filter = None

    @abstractmethod
    def __len__(self):
        """
        Number of documents in dataset.
        """
        pass

    def __iter__(self) -> Generator[Union[Document, Any], None, None]:
        """
        sequence iteration over whole file
        :return: generator of documents or transformed documents when the transformation is activated
        """
        yield from self.iter_range()

    def iter_range(self, f: int = 0, t: Optional[int] = None,
                   unordered: bool = False) -> Generator[Union[Document, Any], None, None]:
        """
        sequence iteration over given range
        :param f: from
        :param t: to
        :param unordered: if True the documents are not returned in order
            might speed up the iteration in multiprocessing mode
        :return: generator of documents or transformed documents when the transformation is activated
        """
        if t is None:
            t = len(self)
        for i in range(f, t):
            yield self[i]

    @property
    def transform(self):
        """
        Transformation that should be applied on a document.
        """
        return self._transform

    @transform.setter
    def transform(self, t: Optional[Union[Callable[[Document], Any], Callable[[Document, int], Any]]]):
        """
        Sets transformation that should be applied on a document.

        :param t: new transformation
            accepts document and returns transformed document
            voluntary accepts document and its index and returns transformed document
        """
        self._transform = t
        self._transform_with_index = t is not None and len(inspect.signature(t).parameters) == 2

    @property
    def transform_with_index(self):
        """
        Whether the transformation accepts document and its index.
        """
        return self._transform_with_index

    def apply_transform(self, doc: Document, index: int) -> Any:
        """
        Applies transformation on a document.

        :param doc: document to transform
        :param index: index of the document
        :return: transformed document
        """
        if self._transform is None:
            return doc
        elif self._transform_with_index:
            return self._transform(doc, index)
        else:
            return self._transform(doc)

    def __getitem__(self, selector: Union[int, slice]) -> Union[Document, List[Document]]:
        """
        Get document from dataset.

        :param selector: line number (from zero) or slice
        :return: the document, or list of documents when the slice is used
        """

        if isinstance(selector, slice):
            return [self._get_item(i) for i in range(len(self))[selector]]
        else:
            return self._get_item(selector)

    @abstractmethod
    def _get_item(self, selector: int) -> Union[Document, Any]:
        """
        Get document from dataset.

        :param selector: id of a document
        :return: the document or transformed document
        """
        pass


class DatasetMultProcWorker(FunctorWorker):
    """
    Helper for multiprocessing.
    Allows to obtain documents in parallel.
    """

    def __init__(self, dataset: DocumentDataset, max_chunks_per_worker: float = math.inf):
        super().__init__(max_chunks_per_worker)
        self.dataset = dataset

    def begin(self):
        if hasattr(self.dataset.transform, "begin"):
            self.dataset.transform.begin()

    def end(self):
        if hasattr(self.dataset.transform, "end"):
            self.dataset.transform.end()

    def __call__(self, i: int) -> Document:
        """
        Obtains document on given index.

        :param i: index of given document
        :return: the document
        """
        try:
            return self.dataset[i]
        except Exception as e:
            print(f"There was an exception in process {multiprocessing.current_process()}")
            traceback.print_exc()
            raise e


class DatasetMultProcWorkerFactory(FunctorWorkerFactory):
    """
    Factory for creating dataset workers.
    """

    def __init__(self, dataset: DocumentDataset, max_chunks_per_worker: float = math.inf):
        """
        :param dataset: dataset it should work on
        :param max_chunks_per_worker: Defines maximal number of chunks that a worker will do before it will stop
            New worker will replace it when used with pool that supports replace queue.

            This is particular useful when you observe increasing memory, as it seems there is a known problem
                with that: https://stackoverflow.com/questions/21485319/high-memory-usage-using-python-multiprocessing
        """
        self.dataset = dataset
        self.max_chunks_per_worker = max_chunks_per_worker

    def create(self) -> DatasetMultProcWorker:
        return DatasetMultProcWorker(self.dataset, self.max_chunks_per_worker)


