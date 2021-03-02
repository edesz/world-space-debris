#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from collections.abc import Iterable


def my_flatten(iterable):
    for value in iterable:
        if isinstance(value, Iterable):
            yield from my_flatten(value)
        else:
            yield value
