from __future__ import annotations

from copy import copy, deepcopy
from itertools import count
from operator import itemgetter
from types import SimpleNamespace
from typing import List

from anytree import Node, NodeMixin, PostOrderIter, RenderTree

from mathesis.forms import Formula

sign = SimpleNamespace(
    **{
        "POSITIVE": "True",
        "NEGATIVE": "False",
    }
)


class Sequent(NodeMixin):
    """A sequent is a pair of premises and conclusions."""

    __items = []

    def __init__(
        self, left: List[Formula], right: List[Formula], parent=None, children=None
    ):
        super().__init__()
        items = []
        for fml in left:
            item = SequentItem(fml, sign.POSITIVE)
            items.append(item)
        for fml in right:
            item = SequentItem(fml, sign.NEGATIVE)
            items.append(item)
        self.items = items
        self.parent = parent
        if children:
            self.children = children

    def __getitem__(self, index):
        if index == 0:
            return self.left
        elif index == 1:
            return self.right

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, value):
        for item in value:
            item.sequent = self
        self.__items = value

    @property
    def name(self):
        return str(self)

    @property
    def left(self):
        return [item for item in self.items if item.sign == sign.POSITIVE]

    @property
    def right(self):
        return [item for item in self.items if item.sign == sign.NEGATIVE]

    # @property
    def tautology(self):
        left = set(str(item.fml) for item in self.left)
        right = set(str(item.fml) for item in self.right)
        if left.intersection(right):
            return True
        else:
            return False

    def latex(self, arrow=r"\Rightarrow"):
        return "{} {} {}".format(
            ", ".join(map(lambda x: f"{x.fml.latex()}", self.left)),
            arrow,
            ", ".join(map(lambda x: f"{x.fml.latex()}", self.right)),
        )

    def __str__(self):
        return "{} ⇒ {}".format(
            ", ".join(map(lambda x: f"{x.name}", self.left)),
            ", ".join(map(lambda x: f"{x.name}", self.right)),
        )


class SequentItem:
    n = None
    sequent = None

    def __init__(
        self, fml: Formula, sign, n: int | None = None, sequent: Sequent | None = None
    ):
        self.fml = fml
        self.sign = sign
        self.n = n
        self.sequent = sequent

    def clone(self):
        clone = deepcopy(self)
        clone.__dict__ = deepcopy(clone.__dict__)
        return clone

    @property
    def name(self):
        return str(self)

    def __str__(self) -> str:
        return str(self.fml)


class SequentTree:
    """A tree of sequents."""

    def __init__(self, premises, conclusions):
        self.counter = count(1)
        self.bookkeeper = dict()
        left, right = (premises, conclusions)
        sequent = Sequent(left, right)
        for item in sequent.items:
            item.n = next(self.counter)
            self.bookkeeper[item.n] = item
        self.root = sequent

    def __getitem__(self, index):
        return self.bookkeeper[index]

    def _apply(self, target: Node, rule):
        queue_items = itemgetter("queue_items")(rule.apply(target, self.counter))

        new_sequents = []

        for branch in queue_items:
            for node in branch.items:
                self.bookkeeper[node.n] = node
            branch.parent = target.sequent
            new_sequents.append(branch)

        return new_sequents

    def apply(self, target: Node, rule):
        self._apply(target, rule)
        return self

    def tree(self, number=True):
        output = ""
        for pre, fill, node in RenderTree(self.root):
            output += "{}{}\n".format(
                pre,
                "{} ⇒ {}".format(
                    ", ".join(
                        map(
                            lambda x: str(x) + (f" {x.n}" if number else ""),
                            node.left,
                        )
                    ),
                    ", ".join(
                        map(
                            lambda x: str(x) + (f" {x.n}" if number else ""),
                            node.right,
                        )
                    ),
                ),
            )
        return output

    def latex(self, number=False, arrow=r"\Rightarrow"):
        output = ""
        for node in PostOrderIter(self.root):
            tmpl = ""
            if len(node.children) == 0:
                tmpl = r"\AxiomC{{${}$}}"
            elif len(node.children) == 1:
                tmpl = r"\UnaryInfC{{${}$}}"
            elif len(node.children) == 2:
                tmpl = r"\BinaryInfC{{${}$}}"
            output += tmpl.format(node.latex()) + "\n"
        return """\\begin{{prooftree}}\n{}\\end{{prooftree}}""".format(output)
