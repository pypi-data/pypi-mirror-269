# Thick dicts

The Thick dict grows thicker (wider) rather than taller.

## Installation
```sh
python -m pip install thick
```

## Reasoning
Why use a Thick? Why even make this?

Basically, I, personally, ran into cases like this a few times while developing Python:

```py
foo = {
    "a": ComplexObjectName1,
    "b": ComplexObjectName2,
    "c": ComplexObjectName1,
    ...
}
```

In this case, typing out such a dictionary, especially one with more entries, violates the DRY principle (a personal favorite) and can be quite error-prone.

Perhaps you would try to map a tuple of key to a value:
```py
foo = {
    ("a", "c", ...): ComplexObjectName1,
    ("b", ...): ComplexObjectName2,
    ...
}
```

But, obviously, this breaks on a call like:
```py
"a" in foo
```

Enter the Thick dict. Given an iterible (but not a string) of keys, or multiple keys mapped to one value, the Thick automatically deduplicates values, and uses set logic to determine if a given key is a subset of any key.

Constructing a Thick dict can come from any existing mapping:
```py
from thick import Thick
my_thick = Thick({
    "a": ComplexObjectName1,
    "b": ComplexObjectName2,
    "c": ComplexObjectName1,
    ...
})

print(my_thick)

{("a", "c", ...): ComplexObjectName1, ("b", ..): ComplexObjectName2, ...}
```

However, those keys are not simple tuples, as such:
```py
print("a" in my_thick)
True

print("c" in my_thick)
True

print(("c", "a") in my_thick)
True # Order doesn't matter

print("b" in my_thick)
True

print(("a", "b") in my_thick)
False # not a subset of a single key
```

## Caveats:
Thick dicts have to have a couple of opinionated decisons to make them work:

1. using a str type as a key does not result in the set of that str iterable:
```py
my_thick = Thick()
my_thick["foo"] = "bar"

# Does this:
{("foo",): "bar"}

# Rather than this:
{("f", "o"): "bar"}
```

2. Iterables (hashable ones, anyway) can be parts of keys, but will be automatically split if used as input
```py
my_thick = Thick({(1, 2, 3): "foo"})
# results in:
{((2, 1, 3): "foo"} # Order is not guaranteed

# However
my_thick_iterable_key = Thick({((1, 2, 3),): "foo"})
# results in:
{((1, 2, 3),): "foo"}

(2, 1, 3) in my_thick
True

(2, 1, 3) in my_thick_iterable_key
False

2 in my_thick
True

2 in my_thick_iterable_key
False
```

### But I just want the normal dictionary!
Good news! You can use the more-simple, D.R.Y. method for construction, and then get the desired dict directly out!
```py
my_thick = Thick({
    ("a", "b", "c"): foo,
    ("d", "e", "f"): bar,
    ...
    })

normal_dict = my_thick.thin()
{
    "a": foo,
    "b": foo,
    "c": foo,
    "d": bar,
    "e": bar,
    "f": bar,
    ...
}
```


## Is this really worth it?

Probably not! I intend to use this in a few of my other personal projects, but I also wanted some more experiencing putting up a pip/PyPI package, and I thought the name was fun (and a little risque, to be fair).

I don't expect anyone else to use this, but, if it does end up being useful, please let me know! If you find any bugs or have any feature requests, please create a GitHub issue!
