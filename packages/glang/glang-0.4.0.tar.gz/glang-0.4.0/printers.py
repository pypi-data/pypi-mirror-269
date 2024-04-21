import traceback

import gdb
import gdb.printing
import gdb.types


class SmartPtrIterator:
    def __init__(self, val):
        self.val = val

    def __iter__(self):
        return self

    def __next__(self):
        if self.val is None:
            raise StopIteration
        self.val, val = None, self.val
        return ("data()", val)


class PtrPrinter(gdb.ValuePrinter):
    def __init__(self, val: gdb.Value):
        self.val = val

    def to_string(self):
        return self.val.type.name

    def children(self):
        return SmartPtrIterator(self.val["data"].referenced_value())


class OptionalPrinter(gdb.ValuePrinter):
    def __init__(self, val: gdb.Value):
        self.val = val

    def to_string(self):
        try:
            if self.val["_ptr"] == 0:
                return f"{self.val.type.name} [empty]"

            return self.val.type.name
        except Exception:
            traceback.print_exc()

    def children(self):
        try:
            itypename = (
                self.val.type.name.removeprefix("Optional<")
                .removesuffix(">")
                .removesuffix("&")
                .removesuffix("mut")
                .strip()
            )
            itype: gdb.Type = gdb.lookup_type(itypename)

            if self.val["_ptr"] == 0:
                return SmartPtrIterator(None)

            return SmartPtrIterator(
                self.val["_ptr"].cast(itype.pointer()).referenced_value()
            )
        except Exception:
            traceback.print_exc()


class RB_NodePrinter(gdb.ValuePrinter):
    def __init__(self, val: gdb.Value):
        self.val = val

    def to_string(self):
        return self.val.type.name

    def children(self):
        try:
            return iter(
                [
                    ("key", self.val["key"]),
                    ("left", self.val["left"]),
                    ("right", self.val["right"]),
                ]
            )
        except Exception:
            traceback.print_exc()


def build_pretty_printer():
    pp = gdb.printing.RegexpCollectionPrettyPrinter("graphene-std")
    pp.add_printer("Ptr", "^Ptr<.*>$", PtrPrinter)
    pp.add_printer("Optional", "^Optional<.*&>$", OptionalPrinter)
    pp.add_printer("RB_Node", "^RB_Node<.*>$", RB_NodePrinter)
    return pp


gdb.printing.register_pretty_printer(gdb.current_objfile(), build_pretty_printer())
