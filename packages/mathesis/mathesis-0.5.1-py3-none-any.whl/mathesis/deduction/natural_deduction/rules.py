from copy import copy, deepcopy
from itertools import count
from typing import Literal

from anytree import Node

from mathesis import forms
from mathesis.deduction.sequent_calculus import Sequent, SequentItem, rules
from mathesis.deduction.tableau import sign, signed_rules


def _apply(target, new_items, counter, preserve_target=True):
    branch_items = new_items
    new_target = None

    for item in target.sequent.items:
        if item != target or preserve_target:
            node = item.clone()
            node.n = next(counter)
            if item == target:
                new_target = node
            branch_items.append(node)

    branch_sequent = Sequent([], [], parent=target.sequent)
    branch_sequent.items = branch_items

    if preserve_target:
        return branch_sequent, target
    else:
        return branch_sequent


class Rule:
    pass


class IntroductionRule(Rule):
    pass


class EliminationRule(Rule):
    pass


class EFQ(Rule):
    def __init__(self, intro: Node):
        self.intro = intro

    def apply(self, target, counter=count(1)):
        assert target.sign == sign.POSITIVE, "Invalid application"
        # TODO: Fix this
        assert str(target.fml) == "⊥", "Not an atom"
        item = SequentItem(
            self.intro.fml,
            sign=sign.POSITIVE,
            n=next(counter),
        )
        sq, _target = _apply(target, [item], counter)

        # Subproof
        item.subproof = Node(
            item,
            parent=target.sequent.right[0].subproof,
            children=[target.subproof],
        )
        # target.subproof = Node(target, children=[item.subproof])
        # _target.sequent.right[0].subproof = target.sequent.right[0].subproof
        sq.right[0].subproof = target.sequent.right[0].subproof

        if sq.tautology():
            target.sequent.right[0].subproof.children = item.subproof.children

        return {
            "queue_items": [sq],
            "counter": counter,
        }


class Negation:
    # Intro = signed_rules.NegativeNegationRule
    class Intro(IntroductionRule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Cannot apply introduction rule"
            assert isinstance(target.fml, forms.Negation), "Not a negation"
            subfml = target.fml.sub

            # TODO: Fix this
            falsum = forms.Atom("⊥")

            antec = SequentItem(subfml, sign=sign.POSITIVE, n=next(counter))
            conseq = SequentItem(
                falsum,
                sign=sign.NEGATIVE,
                n=next(counter),
            )
            sq = _apply(target, [antec, conseq], counter, preserve_target=False)

            # Subproof
            conseq.subproof = Node(
                conseq,
                children=[deepcopy(node.subproof) for node in target.sequent.left],
            )
            target.sequent.right[0].subproof.children = [conseq.subproof]
            antec.subproof = Node(
                antec,
                parent=conseq.subproof,
                children=[],
            )

            return {
                "queue_items": [sq],
                "counter": counter,
            }

    class Elim(EliminationRule):
        def __init__(self):
            pass

        def apply(self, target, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Cannot apply elimination rule"
            assert isinstance(target.fml, forms.Negation), "Not a negation"
            subfml = target.fml.sub

            # TODO: Better way to check conditions
            # premises = list(map(lambda x: str(x.fml), target.sequent.left))
            # assert str(subfml) in premises, f"`{str(subfml)}` must be in premises"
            subfml = next(
                filter(lambda x: str(x.fml) == str(subfml), target.sequent.left),
                None,
            )
            assert subfml, f"`{str(subfml)}` must be in premises"

            falsum = forms.Atom("⊥")
            item = SequentItem(falsum, sign=sign.POSITIVE, n=next(counter))
            sequent, target = _apply(target, [item], counter)

            # Subproof
            item.subproof = Node(
                item,
                children=[
                    deepcopy(subfml.subproof),
                    deepcopy(target.subproof),
                ],
                parent=target.sequent.right[0].subproof,
            )
            sequent.right[0].subproof = target.sequent.right[0].subproof

            return {
                "queue_items": [sequent],
                "counter": counter,
            }


class Conjunction:
    # Intro = signed_rules.NegativeConjunctionRule
    # class Intro(signed_rules.NegativeConjunctionRule, IntroductionRule):
    #     pass

    class Intro(IntroductionRule):
        def __init__(self):
            pass

        def apply(self, target, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Cannot apply introduction rule"
            assert isinstance(target.fml, forms.Conjunction), "Not a conjunction"

            branches = []

            for conj in target.fml.subs:
                conj = SequentItem(conj, sign=sign.NEGATIVE, n=next(counter))
                sequent = _apply(target, [conj], counter, preserve_target=False)
                branches.append(sequent)

            # Subproof
            for branch in branches:
                for item in branch.left:
                    if getattr(item, "subproof", None) is None:
                        item.subproof = Node(item)

                branch.right[0].subproof = Node(branch.right[0])
                branch.right[0].subproof.children = [
                    deepcopy(item.subproof) for item in branch.left
                ]

                if branch.tautology():
                    left_item = next(
                        filter(
                            lambda x: str(x.fml) == str(branch.right[0]), branch.left
                        ),
                        None,
                    )
                    branch.right[0].subproof.children = left_item.subproof.children

            target.sequent.right[0].subproof.children = [
                branch.right[0].subproof for branch in branches
            ]

            return {
                "queue_items": branches,
                "counter": counter,
            }

    # TODO: Choice of conjunct
    # Elim = signed_rules.PositiveConjunctionRule
    class Elim(EliminationRule):
        def __init__(self, conjunct: Literal["left", "right"]):
            self.conjunct = conjunct

        def apply(self, target, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Cannot apply elimination rule"
            assert isinstance(target.fml, forms.Conjunction), "Not a conjunction"

            conj1, conj2 = target.fml.subs
            if self.conjunct == "left":
                item = SequentItem(conj1, sign=sign.POSITIVE, n=next(counter))
            elif self.conjunct == "right":
                item = SequentItem(conj2, sign=sign.POSITIVE, n=next(counter))

            sq1, target = _apply(target, [item], counter)
            # sq2 = Sequent([target], [item], parent=target.sequent)

            # Subproof
            item.subproof = Node(
                item,
                children=[target.subproof],
                parent=target.sequent.right[0].subproof,
            )

            return {
                "queue_items": [sq1],
                "counter": counter,
            }


class Disjunction:
    # Intro = signed_rules.NegativeDisjunctionRule
    class Intro(IntroductionRule):
        def __init__(self, disjunct: Literal["left", "right"]):
            self.disjunct = disjunct

        def apply(self, target, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Sign is not negative"
            assert isinstance(target.fml, forms.Disjunction), "Not a disjunction"
            disj1, disj2 = target.fml.subs

            if self.disjunct == "left":
                item = SequentItem(disj1, sign=sign.NEGATIVE, n=next(counter))
            elif self.disjunct == "right":
                item = SequentItem(disj2, sign=sign.NEGATIVE, n=next(counter))

            sq = _apply(target, [item], counter, preserve_target=False)

            # Subproof
            item.subproof = Node(
                item,
                children=[deepcopy(item.subproof) for item in sq.left],
            )
            target.subproof.children = [item.subproof]
            # sq.right[0].subproof = target.sequent.right[0].subproof

            if sq.tautology():
                left_item = next(
                    filter(lambda x: str(x.fml) == str(item.fml), sq.left),
                    None,
                )
                target.subproof.children = [left_item.subproof]

            return {
                "queue_items": [sq],
                "counter": counter,
            }

    # Elim = signed_rules.PositiveDisjunctionRule
    class Elim(EliminationRule):
        def __init__(self):
            pass

        def apply(self, target, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Cannot apply elimination rule"
            assert isinstance(target.fml, forms.Disjunction), "Not a disjunction"

            branches = []

            for disj in target.fml.subs:
                disj = SequentItem(disj, sign=sign.POSITIVE, n=next(counter))
                sequent, target = _apply(target, [disj], counter)
                branches.append(sequent)

            # Subproof
            for branch in branches:
                for item in branch.left:
                    if getattr(item, "subproof", None) is None:
                        item.subproof = Node(item)

                branch.right[0].subproof = Node(branch.right[0])
                branch.right[0].subproof.children = [
                    deepcopy(item.subproof) for item in branch.left
                ]

            target.sequent.right[0].subproof.children = [
                branch.right[0].subproof for branch in branches
            ] + [target.subproof]

            return {
                "queue_items": branches,
                "counter": counter,
            }


class Conditional:
    # class Intro(signed_rules.NegativeConditionalRule, IntroductionRule):
    #     pass
    class Intro(IntroductionRule):
        def apply(self, target, counter=count(1)):
            assert target.sign == sign.NEGATIVE, "Cannot apply introduction rule"
            assert isinstance(target.fml, forms.Conditional), "Not a conditional"
            antec, conseq = target.fml.subs

            antec = SequentItem(antec, sign=sign.POSITIVE, n=next(counter))
            conseq = SequentItem(
                conseq,
                sign=sign.NEGATIVE,
                n=next(counter),
            )
            sq = _apply(target, [antec, conseq], counter, preserve_target=False)

            # Subproof
            conseq.subproof = Node(
                conseq,
                children=[deepcopy(node.subproof) for node in target.sequent.left],
            )
            target.sequent.right[0].subproof.children = [conseq.subproof]
            antec.subproof = Node(
                antec,
                parent=conseq.subproof,
                children=[],
            )

            return {
                "queue_items": [sq],
                "counter": counter,
            }

    class Elim(EliminationRule):
        def __init__(self):
            pass

        def apply(self, target, counter=count(1)):
            assert target.sign == sign.POSITIVE, "Cannot apply elimination rule"
            assert isinstance(target.fml, forms.Conditional), "Not a conditional"
            antec, conseq = target.fml.subs

            # TODO: Better way to check conditions
            antec = next(
                filter(lambda x: str(x.fml) == str(antec), target.sequent.left),
                None,
            )
            assert antec, "Antecendent does not match"

            # conclusion = str(target.sequent.right[0].fml)
            # print(conclusion)
            # assert str(conseq) == conclusion, "Consequent does not match"

            conseq = SequentItem(conseq, sign=sign.POSITIVE, n=next(counter))
            sequent, _target = _apply(target, [conseq], counter)

            # Subproof
            conseq.subproof = Node(
                conseq,
                children=[
                    deepcopy(antec.subproof),
                    deepcopy(target.subproof),
                ],
                parent=target.sequent.right[0].subproof,
            )
            # target.sequent.right[0].subproof = sequent.right[0].subproof
            sequent.right[0].subproof = target.sequent.right[0].subproof

            if sequent.tautology():
                target.sequent.right[0].subproof.children = conseq.subproof.children

            return {
                "queue_items": [sequent],
                "counter": counter,
            }
