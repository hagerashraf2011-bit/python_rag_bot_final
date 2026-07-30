# =========================================================================
# Python knowledge base for the RAG tutor — CURATED FALLBACK ONLY.
#
# Priority order (see _load_documents() below): the app always tries
# data/scraped_documents.json (built by 00_scrape_documents.py from real
# docs.python.org pages) FIRST. The curated text in this file is used only
# when a topic's scrape failed, or the scrape has never been run at all —
# it exists so the pipeline (02..07, streamlit_app.py) never ends up with a
# missing or empty knowledge base just because of a network problem.
#
# Each document is one self-contained topic: explanation + why/when to use
# it + a common mistake + a code example. Entries run longer now (roughly
# 250-320 words) than the original ~180-word version, so 03_chunking.py's
# chunk_size was raised to match — every topic still survives as ONE whole
# chunk, so answers are never cut off mid-explanation.
# =========================================================================
import json
from pathlib import Path

_SCRAPED_PATH = Path(__file__).resolve().parent / "data" / "scraped_documents.json"

_fallback_documents = []


def add(id, title, category, text, is_current=True, replaces=None):
    doc = {"id": id, "title": title, "category": category, "is_current": is_current, "text": text.strip()}
    if replaces:
        doc["replaces"] = replaces  # id of the CURRENT doc this outdated entry conflicts with
    _fallback_documents.append(doc)


# ---------------------------------------------------------------- basics --
add("print_function", "The print() Function", "basics", """
print() writes output to the console. It accepts multiple values separated
by commas, and you can control the separator with sep and the ending
character with end (the default end is a newline, which is why each call
to print() normally starts a new line).

You'll reach for print() constantly while learning and debugging — it's
the fastest way to check what a variable actually holds at a given moment,
before you have proper tools like a debugger or logging. A common mistake
beginners make is forgetting that print() always converts its arguments to
strings for display, so print(1 + 1) shows 2, but print("1" + "1") shows
"11" because that's string concatenation, not addition.

Example:
print("Hello", "world")
print("A", "B", "C", sep=" - ")
print("no newline", end="")
print("this appears on the same line as above")
""")

add("variables_data_types", "Variables and Data Types", "basics", """
A variable is a name pointing to a value in memory. Python infers the type
automatically from the value; you never declare a type up front, and a
variable can be reassigned to a completely different type later — this is
called dynamic typing. Core built-in types are int, float, str, bool, list,
tuple, dict, and set.

Dynamic typing is convenient but it's also where a common bug creeps in:
reusing the same variable name for two different kinds of data in the same
function makes code confusing and error-prone, even though Python allows
it without complaint. A good habit is choosing a variable name that clearly
reflects what it stores, and sticking to one type per variable throughout
its lifetime.

Example:
age = 25
price = 19.99
name = "Alice"
is_active = True
print(type(age), type(price))   # <class 'int'> <class 'float'>
age = "twenty-five"             # legal, but usually a bad idea
""")

add("input_function", "Reading User Input", "basics", """
input() pauses the program, shows an optional prompt, and returns whatever
the user typed as a string. If you need a number, you must convert it
yourself with int() or float(), since input() never returns numeric types
— even if the user types "42", you get back the string "42", not the
integer 42.

This is one of the most common early bugs: trying to do math directly on
input() without converting it first raises a TypeError, because you can't
add an int to a str. It's also worth wrapping the conversion in a
try/except when you expect real users, since typing "abc" where a number
is expected will crash int() with a ValueError.

Example:
name = input("What is your name? ")
age_text = input("What is your age? ")
age = int(age_text)
print(f"{name} is {age} years old, and will be {age + 1} next year")
""")

add("type_casting", "Type Casting", "basics", """
Type casting converts a value from one type to another using functions
like int(), float(), str(), and bool(). This is common after reading text
input, or when combining numbers and strings, since Python does not
auto-convert strings and numbers in expressions the way some languages do.

Not every conversion is safe: int("3.5") raises a ValueError because "3.5"
isn't a valid integer literal — you'd need float("3.5") first, then
int(float("3.5")) if you specifically need a whole number. bool() casting
surprises people too: bool("False") is actually True, because any
non-empty string is truthy in Python, regardless of what it says.

Example:
text_number = "42"
number = int(text_number)
print(number + 8)              # 50
print(str(3.14) + " pi")       # "3.14 pi"
print(bool("False"))           # True — non-empty string, so truthy!
print(int(float("3.5")))       # 3
""")

add("arithmetic_operators", "Arithmetic Operators", "basics", """
Python supports +, -, *, / (true division, always returns a float), //
(floor division), % (modulo/remainder), and ** (exponent). Operator
precedence follows standard math rules (** binds tighter than * and /,
which bind tighter than + and -), and parentheses can override that order
whenever the default reading isn't what you want.

// and % are especially useful together: // gives you how many whole
times one number divides another, and % gives you what's left over — for
example, converting a total number of seconds into minutes and seconds.
A common surprise for beginners coming from other languages is that /
always returns a float in Python 3, even when both operands are integers
and the division is exact.

Example:
print(7 / 2)    # 3.5
print(7 // 2)   # 3
print(7 % 2)    # 1
print(2 ** 5)   # 32
total_seconds = 125
print(total_seconds // 60, "min", total_seconds % 60, "sec")  # 2 min 5 sec
""")

add("comparison_logical_operators", "Comparison and Logical Operators", "basics", """
Comparison operators (==, !=, <, >, <=, >=) compare two values and return
a boolean. Logical operators and, or, and not combine or invert boolean
expressions, and Python short-circuits them: it stops evaluating as soon
as the overall result is known, which matters when the second condition
has a side effect or could error out.

A frequent beginner mistake is confusing = (assignment) with == (equality
comparison) — writing `if x = 5:` is a syntax error in Python, which
actually helps catch this bug early, unlike some other languages. Another
subtlety: `and`/`or` return one of the actual operand values, not always
True/False, which is a handy trick for setting defaults.

Example:
age = 20
has_id = True
print(age >= 18 and has_id)   # True
print(not has_id)             # False
name = "" or "Guest"          # short-circuit trick for a default value
print(name)                   # Guest
""")

add("comments_docstrings", "Comments and Docstrings", "basics", """
A comment starts with # and is ignored by Python; it documents code for
humans and has zero effect on how the program runs. A docstring is a
string literal placed as the first statement in a module, function, or
class, used to describe what it does; unlike a comment, it's stored as an
actual attribute (__doc__) and is accessible at runtime through tools like
help() and IDEs' tooltips.

Good comments explain *why* something is done a certain way, not *what*
the code does line by line — the code itself already shows the "what."
Over-commenting obvious code (like `x = x + 1  # add one to x`) is a
common beginner habit that clutters files without adding real value.

Example:
def add(a, b):
    \"\"\"Return the sum of a and b.\"\"\"
    return a + b   # simple, no comment needed here

print(add.__doc__)   # "Return the sum of a and b."
help(add)             # shows the docstring in an interactive session
""")

add("booleans_none", "Booleans and None", "basics", """
bool has exactly two values, True and False, and is technically a subtype
of int (True equals 1, False equals 0 in arithmetic contexts). None
represents the absence of a value and is Python's null; it's commonly used
as a default argument, a placeholder before a real value exists, or a
function's implicit return when nothing else is returned.

A classic beginner bug is comparing to None with == instead of is: while
`x == None` usually works, `x is None` is the correct, recommended way,
because is checks true identity rather than relying on a possibly
overridden __eq__ method. Also remember that 0, "", [], and None are all
falsy but are NOT the same value as each other or as False.

Example:
result = None
if result is None:
    print("Not calculated yet")

def do_nothing():
    pass

print(do_nothing())   # None — no explicit return means None
""")

# ------------------------------------------------------- data_structures --
add("lists_and_methods", "Lists and List Methods", "data_structures", """
A list is an ordered, mutable collection created with square brackets.
Common methods are append() to add an item at the end, insert() to add at
a position, remove() to delete the first matching value, pop() to remove
and return an item by index, and sort() to order items in place.

Lists are mutable, which is powerful but also a common source of bugs:
assigning `list_b = list_a` doesn't copy the list, it makes list_b point
to the exact same list in memory, so changing one changes the other. Use
`list_b = list_a.copy()` or `list(list_a)` when you actually want an
independent copy.

Example:
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")
fruits.remove("banana")
fruits.sort()
print(fruits)                  # ['apple', 'cherry', 'orange']

original = [1, 2, 3]
alias = original               # NOT a copy — same list in memory
alias.append(4)
print(original)                # [1, 2, 3, 4] — original changed too!
""")

add("list_comprehension", "List Comprehensions", "data_structures", """
A list comprehension builds a new list from an existing iterable in one
line: [expression for item in iterable if condition]. It replaces creating
an empty list and calling append() inside a loop, and is usually both
shorter and measurably faster, since the looping happens at a lower level
inside Python's interpreter.

The main trade-off is readability: a comprehension with two nested loops
or several conditions can quickly become hard to read, and at that point a
regular for loop is often the better, more maintainable choice. A good
rule of thumb is to keep comprehensions to a single line that reads
naturally out loud.

Example:
numbers = [1, 2, 3, 4, 5, 6]
squares = [n ** 2 for n in numbers]
even_squares = [n ** 2 for n in numbers if n % 2 == 0]
print(squares)          # [1, 4, 9, 16, 25, 36]
print(even_squares)     # [4, 16, 36]

# equivalent, longer version without a comprehension:
even_squares_v2 = []
for n in numbers:
    if n % 2 == 0:
        even_squares_v2.append(n ** 2)
""")

add("tuples", "Tuples", "data_structures", """
A tuple is an ordered, immutable collection written with parentheses; once
created, its items cannot be changed, added to, or removed. Tuples are
used for fixed groups of values, like coordinates or a database row, and
can be safely used as dictionary keys since they're hashable, unlike lists.

Immutability is the whole point: it signals to anyone reading the code
that this collection of values isn't meant to change, and it lets Python
optimize and safely share tuples internally. A common point of confusion
is that a one-item tuple needs a trailing comma — `(5)` is just the number
5 in parentheses, but `(5,)` is a genuine one-item tuple.

Example:
point = (10, 20)
x, y = point
print(x, y)              # 10 20
print(point[0])          # 10

not_a_tuple = (5)
print(type(not_a_tuple))          # <class 'int'>
really_a_tuple = (5,)
print(type(really_a_tuple))       # <class 'tuple'>
""")

add("dictionaries", "Dictionaries", "data_structures", """
A dictionary stores key-value pairs, written with curly braces. Keys must
be unique and hashable (strings, numbers, tuples); values can be anything.
You access a value by key with square brackets, or with get() to avoid a
KeyError on a missing key — get() also accepts a default value to return
instead of raising an error. items(), keys(), and values() let you loop
over its contents.

Since Python 3.7, dictionaries remember the order items were inserted in,
which many people don't expect coming from older material. A very common
beginner mistake is using square-bracket access (`dict["key"]`) when a key
might not exist — that raises a KeyError and crashes the program, whereas
`.get("key")` fails gracefully.

Example:
student = {"name": "Sara", "age": 21}
print(student.get("gpa", "N/A"))   # N/A — key doesn't exist, no crash
for key, value in student.items():
    print(key, "->", value)

# student["gpa"] would raise: KeyError: 'gpa'
""")

add("dict_comprehension", "Dictionary Comprehensions", "data_structures", """
A dictionary comprehension builds a dict in one line: {key: value for item
in iterable if condition}. It's the dict equivalent of a list
comprehension and is especially useful for transforming an existing list
or dict into a fast lookup structure, avoiding repeated linear searches
through a list later in your code.

One subtlety worth knowing: if the comprehension produces duplicate keys,
only the LAST value for that key survives in the final dictionary — earlier
ones are silently overwritten, which can hide a bug if you're not
expecting duplicates in your source data.

Example:
names = ["Ali", "Mona", "Zaid"]
name_lengths = {name: len(name) for name in names}
print(name_lengths)     # {'Ali': 3, 'Mona': 4, 'Zaid': 4}

# duplicate-key example: later value wins
pairs = [("a", 1), ("a", 2)]
result = {k: v for k, v in pairs}
print(result)            # {'a': 2} — the first (a, 1) is gone
""")

add("sets", "Sets", "data_structures", """
A set is an unordered collection of unique, hashable items, written with
curly braces or set(). Sets automatically remove duplicates and support
fast membership tests (much faster than checking `item in a_list` for a
large list) plus math-style operations like union (|), intersection (&),
and difference (-).

Because sets are unordered, you can't index into one (`my_set[0]` doesn't
work), and printing a set won't reliably show items in the order you added
them. A very common practical use is de-duplicating a list quickly:
`list(set(my_list))` — though this also loses the original order, so it's
not a fit if order matters.

Example:
a = {1, 2, 3}
b = {2, 3, 4}
print(a | b)         # {1, 2, 3, 4}
print(a & b)         # {2, 3}
print(3 in a)        # True — fast membership check

numbers = [1, 2, 2, 3, 3, 3]
unique = list(set(numbers))
print(sorted(unique))   # [1, 2, 3]
""")

add("string_methods", "Common String Methods", "data_structures", """
Strings have many built-in methods for cleaning and transforming text:
strip() removes surrounding whitespace, split() breaks a string into a
list, join() combines a list into a string, replace() substitutes text,
and lower()/upper() change case. Strings are immutable, so every one of
these methods returns a brand-new string — the original string is never
modified in place.

Because strings are immutable, chaining several string methods is a
common and efficient pattern: `text.strip().lower().replace(" ", "_")` is
perfectly normal and reads top-to-bottom as a pipeline of transformations.
A frequent beginner mistake is calling a method like `text.strip()` and
expecting `text` itself to have changed — you have to assign the result
back to a variable to keep it.

Example:
text = "  Hello, World  "
cleaned = text.strip().lower()
print(cleaned)                    # "hello, world"
print(",".join(["a", "b", "c"]))  # "a,b,c"
print(text)                       # unchanged — still has the extra spaces
""")

add("slicing", "Sequence Slicing", "data_structures", """
Slicing extracts a sub-part of a list, tuple, or string using
sequence[start:stop:step]. start is inclusive, stop is exclusive, and step
lets you skip elements or reverse a sequence with a negative value. Any of
the three parts can be omitted, which is where most of slicing's real
power comes from in everyday code.

Slicing never raises an IndexError even if start or stop is out of range —
it just returns as much as exists, which is genuinely convenient but can
also silently hide a bug where you expected an error and didn't get one.

Example:
numbers = [0, 1, 2, 3, 4, 5]
print(numbers[1:4])     # [1, 2, 3]
print(numbers[:3])      # [0, 1, 2]
print(numbers[::-1])    # [5, 4, 3, 2, 1, 0] — reversed copy
print(numbers[2:100])   # [2, 3, 4, 5] — no error, just stops at the end
""")

add("sorting_data", "Sorting with sorted() and sort()", "data_structures", """
sorted() returns a new sorted list from any iterable without changing the
original, while list.sort() sorts a list in place and returns None. Both
accept a key function to control what is actually compared, and
reverse=True for descending order.

A common beginner mistake is writing `my_list = my_list.sort()`, which
sets my_list to None, because sort() modifies the list in place and
doesn't return the sorted list itself — that's the job of sorted(). Using
key=lambda is the standard way to sort complex data by something other
than its natural order, like sorting tuples by their second element.

Example:
students = [("Ali", 82), ("Mai", 91), ("Zaid", 76)]
by_score = sorted(students, key=lambda s: s[1], reverse=True)
print(by_score)   # [('Mai', 91), ('Ali', 82), ('Zaid', 76)]

numbers = [3, 1, 2]
numbers.sort()
print(numbers)     # [1, 2, 3] — sorted in place, sort() itself returns None
""")

add("unpacking", "Unpacking and the * Operator", "data_structures", """
Unpacking assigns the items of a list or tuple to multiple variables in
one line. The * operator collects extra items into a list during
unpacking, and can also spread a list's items out as individual arguments
when calling a function — two related but distinct uses of the same
symbol.

Unpacking has to match the number of variables exactly unless you use *
to soak up the extras — trying to unpack a 3-item list into 2 plain
variables raises a ValueError, which is a common early error message
beginners run into.

Example:
first, second, *rest = [1, 2, 3, 4, 5]
print(first, second, rest)   # 1 2 [3, 4, 5]

def add3(a, b, c):
    return a + b + c

values = [1, 2, 3]
print(add3(*values))   # 6 — * spreads the list as separate arguments

# a, b = [1, 2, 3]   # would raise: too many values to unpack
""")

# --------------------------------------------------- functions_functional --
add("functions_args", "Functions, Arguments, and Return Values", "functions_functional", """
A function is defined with def and can accept positional arguments,
keyword arguments, default values, *args for extra positional arguments,
and **kwargs for extra keyword arguments. return sends a value back to the
caller; without it, a function returns None, which surprises beginners
who assume "no return statement" means "no value at all."

Default argument values are evaluated only ONCE, when the function is
defined — not on every call. This causes a well-known gotcha with mutable
defaults like lists: using `def f(items=[])` means every call without an
explicit argument shares the SAME list, which can quietly accumulate data
across calls. The fix is to default to None and create the list inside
the function body.

Example:
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

def total(*numbers):
    return sum(numbers)

print(greet("Omar"))       # Hello, Omar!
print(total(1, 2, 3, 4))   # 10

def safe_append(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
""")

add("lambda_functions", "Lambda Functions", "functions_functional", """
A lambda is a small, anonymous, single-expression function created with
the lambda keyword instead of def. Lambdas are typically passed as a short
callback to functions like sorted(), map(), and filter(), and always
return the value of their one expression — they can't contain multiple
statements, loops, or assignments.

Lambdas are meant for genuinely small, throwaway logic. If you find
yourself writing a complicated or hard-to-read lambda, that's usually a
sign it should be a regular named function with def instead — readability
matters more than saving a few lines.

Example:
square = lambda x: x ** 2
print(square(5))    # 25
print(sorted([3, 1, 2], key=lambda x: -x))   # [3, 2, 1]

# same result written as a regular function — often clearer for anything
# more complex than a single small expression:
def negate(x):
    return -x
""")

add("map_filter_reduce", "map(), filter(), and reduce()", "functions_functional", """
map() applies a function to every item of an iterable and returns an
iterator of results. filter() keeps only the items for which a function
returns True. reduce(), from the functools module, combines all items into
a single value by repeatedly applying a function to a running result and
the next item.

map() and filter() return lazy iterators in Python 3, not lists — you
usually need to wrap them in list() to see or reuse the results more than
once, which trips up people expecting Python 2's behavior. In modern
Python, list/dict comprehensions are often considered more readable than
map()/filter() for simple cases, while reduce() still earns its place for
genuine running-accumulation logic.

Example:
from functools import reduce
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda n: n * 2, numbers))
evens = list(filter(lambda n: n % 2 == 0, numbers))
total = reduce(lambda a, b: a + b, numbers)
print(doubled, evens, total)   # [2, 4, 6, 8, 10] [2, 4] 15
""")

add("decorators", "Decorators", "functions_functional", """
A decorator is a function that wraps another function to add behavior
before or after it runs, without changing the original function's code.
Decorators are applied with @decorator_name placed above a function
definition, and are common for logging, timing, access control, and
caching.

A frequent decorator bug is forgetting to use *args and **kwargs in the
inner wrapper function, which then only works for functions that take
zero arguments. Another common issue is losing the original function's
name and docstring after decorating it — the standard fix is
`functools.wraps`, which copies that metadata onto the wrapper.

Example:
from functools import wraps

def log_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def add(a, b):
    return a + b

print(add(2, 3))          # Calling add, then 5
print(add.__name__)       # "add" — thanks to @wraps, not "wrapper"
""")

add("generators", "Generators and yield", "functions_functional", """
A generator produces a sequence of values lazily, one at a time, instead
of building the whole list in memory. It uses yield instead of return;
each yield pauses the function and remembers its exact state until the
next value is requested, which makes generators memory-efficient for
large or even infinite sequences.

A generator can only be iterated over once — once it's exhausted, looping
over it again produces nothing, which surprises people expecting
list-like reusability. If you need to loop over the same data multiple
times, convert it to a list first, at the cost of the memory savings.

Example:
def count_up_to(limit):
    n = 1
    while n <= limit:
        yield n
        n += 1

counter = count_up_to(4)
for number in counter:
    print(number)     # 1 2 3 4

for number in counter:   # nothing prints — the generator is exhausted
    print(number)
""")

add("closures", "Closures", "functions_functional", """
A closure is an inner function that remembers and can access variables
from its enclosing function's scope, even after the outer function has
finished running and would normally have "gone away." Closures are the
mechanism decorators are built on, and are useful for creating small,
configurable functions without resorting to a full class.

A well-known gotcha appears when creating closures inside a loop: if the
inner function references the loop variable directly, all the closures
end up sharing the SAME final value of that variable, not the value it
had at creation time. The fix is to pass the loop variable in as a default
argument, which captures its value immediately.

Example:
def make_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

double = make_multiplier(2)
print(double(5))   # 10

# the loop-variable gotcha and its fix:
funcs_wrong = [lambda: i for i in range(3)]
print([f() for f in funcs_wrong])          # [2, 2, 2] — surprising!
funcs_right = [lambda i=i: i for i in range(3)]
print([f() for f in funcs_right])          # [0, 1, 2] — fixed
""")

add("recursion", "Recursion", "functions_functional", """
A recursive function calls itself to solve a smaller version of the same
problem, until it reaches a base case that stops the recursion. Every
recursive function needs a clear base case, or it will keep calling
itself until Python raises a RecursionError, since Python's default
recursion limit is around 1000 calls deep.

Recursion is elegant for naturally recursive problems (tree traversal,
factorials, some search algorithms), but it isn't always the most
efficient choice in Python — each call adds overhead, and a loop-based
version of the same logic is often faster and uses less memory.

Example:
def factorial(n):
    if n <= 1:               # base case — stops the recursion
        return 1
    return n * factorial(n - 1)

print(factorial(5))    # 120

# without a base case, this would recurse forever until RecursionError:
# def broken(n):
#     return broken(n - 1)
""")

# ------------------------------------------------------------------ oop --
add("oop_classes", "Classes and Objects", "oop", """
A class is a blueprint for creating objects that bundle data and behavior
together. __init__ runs automatically when a new object is created and
sets up instance attributes. self refers to the specific instance a
method is called on and must be the first parameter of every regular
method — Python passes it automatically, you never supply it yourself
when calling the method.

Beginners often forget self when defining a method, which causes a
TypeError about the wrong number of arguments as soon as the method is
called, since Python is silently trying to pass the instance as the first
argument regardless.

Example:
class Student:
    def __init__(self, name, gpa):
        self.name = name
        self.gpa = gpa

    def describe(self):
        return f"{self.name} has a GPA of {self.gpa}"

s1 = Student("Laila", 3.8)
print(s1.describe())   # Laila has a GPA of 3.8
""")

add("oop_inheritance", "Inheritance", "oop", """
Inheritance lets a class reuse and extend the attributes and methods of
another class. The original class is the parent (base) class, and the new
class is the child (derived) class. Calling super().__init__() inside the
child's constructor runs the parent's setup logic before adding anything
new — skipping this call is a common bug that leaves the parent's
attributes never initialized.

Python supports multiple inheritance (a class inheriting from more than
one parent), but it should be used carefully, since it can make method
resolution order confusing; single inheritance covers the vast majority
of real-world cases cleanly.

Example:
class Person:
    def __init__(self, name):
        self.name = name

class Teacher(Person):
    def __init__(self, name, subject):
        super().__init__(name)   # sets up self.name via the parent
        self.subject = subject

t = Teacher("Mona", "Math")
print(t.name, t.subject)   # Mona Math
""")

add("polymorphism", "Polymorphism", "oop", """
Polymorphism means different classes can define a method with the same
name, and calling that method behaves according to each object's actual
class. This lets you write code that works with any object exposing the
expected method, without checking its exact type — often summarized as
"duck typing": if it walks like a duck and quacks like a duck, treat it
like a duck.

This is one of the most practical benefits of OOP in Python: functions
that loop over a mixed collection of objects and call the same method
name on each don't need if/elif chains checking each object's type first.

Example:
class Dog:
    def speak(self):
        return "Woof"

class Cat:
    def speak(self):
        return "Meow"

for animal in [Dog(), Cat()]:
    print(animal.speak())   # Woof, then Meow — same method call, different behavior
""")

add("encapsulation", "Encapsulation", "oop", """
Encapsulation means bundling data with the methods that operate on it, and
restricting direct access from outside the class. Python signals intent
with naming conventions rather than true enforcement: a single leading
underscore (_name) means "internal use, please don't touch," and a double
leading underscore (__name) triggers name mangling, which makes accidental
external access harder but not impossible.

Unlike some languages, Python doesn't have true "private" attributes —
it relies on convention and trust rather than a compiler-enforced wall.
Respecting the underscore convention, even though nothing stops you from
breaking it, is considered good Python style.

Example:
class Account:
    def __init__(self, balance):
        self.__balance = balance   # name-mangled, harder to access directly

    def deposit(self, amount):
        self.__balance += amount
        return self.__balance

acc = Account(100)
print(acc.deposit(50))       # 150
# print(acc.__balance)       # AttributeError — mangled to _Account__balance
""")

add("magic_methods", "Magic (Dunder) Methods", "oop", """
Magic methods, also called dunder methods because their names start and
end with double underscores, let a class customize how it behaves with
built-in operations. __str__ controls print() output, __len__ powers
len(), and __eq__ controls the == operator — without defining these,
Python falls back to a generic, not-very-useful default (like showing a
memory address).

Defining __repr__ in addition to __str__ is good practice: __str__ is for
a human-friendly display, while __repr__ is meant to be an unambiguous,
often code-like representation useful for debugging in a console.

Example:
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

print(Point(1, 2))                 # Point(1, 2)
print(Point(1, 2) == Point(1, 2))  # True — thanks to __eq__
""")

add("static_class_methods", "Static Methods and Class Methods", "oop", """
A regular method takes self and operates on one specific instance. A
static method, marked with @staticmethod, takes neither self nor cls and
behaves like a plain function that's just grouped inside the class for
organization — it can't touch instance or class data directly. A class
method, marked with @classmethod, takes cls instead of self and can
access or modify class-level state shared by all instances.

Class methods are commonly used as alternative constructors — a way to
create an instance from data in a different shape than __init__ expects,
without cluttering __init__ itself with special cases.

Example:
class MathHelper:
    @staticmethod
    def add(a, b):
        return a + b

class Pizza:
    def __init__(self, toppings):
        self.toppings = toppings

    @classmethod
    def margherita(cls):
        return cls(["mozzarella", "tomato"])   # alternative constructor

print(MathHelper.add(2, 3))   # 5
print(Pizza.margherita().toppings)   # ['mozzarella', 'tomato']
""")

add("properties", "Properties", "oop", """
The @property decorator turns a method into an attribute that computes its
value on access, letting you add validation or derived values without
changing how callers use the class — they access it like a plain
attribute (`c.area`), not a method call (`c.area()`). A matching
@name.setter lets you control assignment the same way, for example
rejecting an invalid value.

Properties are especially useful for keeping a public API stable while
changing the internal implementation: you can start with a plain attribute
and later convert it to a property with validation, without breaking any
code that uses the class.

Example:
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14159 * self.radius ** 2

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius can't be negative")
        self._radius = value

c = Circle(3)
print(c.area)   # 28.27...
""")

add("abstract_classes", "Abstract Classes", "oop", """
An abstract class defines a common interface that subclasses must
implement, but is never instantiated directly. Python provides this
through the abc module: inherit from ABC and mark required methods with
@abstractmethod, which forces every concrete subclass to override them —
trying to instantiate the abstract class itself, or a subclass missing a
required method, raises a TypeError.

Abstract classes are useful when you want to guarantee that every
subclass in a system implements a certain method (like area() for
different Shape types), catching a missing implementation at the moment
the object is created rather than much later when the method is actually
called.

Example:
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

# Shape()   # would raise: TypeError, can't instantiate abstract class
print(Square(4).area())   # 16
""")

add("dataclasses", "Dataclasses", "oop", """
The dataclasses module generates boilerplate code such as __init__,
__repr__, and __eq__ automatically for classes that mainly store data.
Decorating a class with @dataclass and listing typed attributes replaces
writing that boilerplate by hand, which reduces both the amount of code
and the number of places a small typo could introduce a bug.

Dataclasses are a great fit for simple data containers, but they aren't a
full replacement for regular classes when you need complex custom
behavior, private state, or inheritance-heavy designs — for those, a
hand-written class is still the clearer choice.

Example:
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1)              # Point(x=1, y=2) — free __repr__
print(p1 == p2)         # True — free __eq__, compares field values
""")

# ---------------------------------------------------------- errors_files --
add("error_handling", "Error Handling with try / except", "errors_files", """
Python uses exceptions to signal runtime errors. A try block holds code
that might fail, except catches a specific exception type and lets the
program keep running, else runs only if no exception occurred, and
finally always runs — whether or not an exception happened — which makes
it the natural place for cleanup like closing a file or a connection.

Catching a bare `except:` with no exception type is considered bad
practice: it silently swallows every possible error, including ones you
didn't anticipate (like a typo causing a NameError), making bugs much
harder to find. Catching a specific exception type is almost always the
better choice.

Example:
try:
    result = 10 / 0
except ZeroDivisionError:
    print("You cannot divide by zero.")
finally:
    print("Done trying the operation.")

# bad practice — avoid this:
# try:
#     risky()
# except:
#     pass
""")

add("custom_exceptions", "Custom Exceptions", "errors_files", """
You can define your own exception types by subclassing Exception (or a
more specific built-in exception). This lets calling code catch your
exact error type with except, and makes error messages specific to your
program's domain instead of generic — a caller can tell "insufficient
funds" apart from "invalid account number" just by the exception class.

A good custom exception hierarchy lets calling code catch broadly (the
common base class) or narrowly (one specific subclass), depending on how
it needs to react — this flexibility is one of the main reasons to define
your own exception types instead of always raising a generic ValueError.

Example:
class BankError(Exception):
    pass

class InsufficientFundsError(BankError):
    pass

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError("Not enough balance")
    return balance - amount

try:
    withdraw(50, 100)
except InsufficientFundsError as e:
    print(f"Withdrawal failed: {e}")
""")

add("context_managers", "Context Managers (with statement)", "errors_files", """
The with statement wraps a block of code with setup and cleanup logic that
always runs, even if an error occurs inside the block — most commonly
used for closing files or releasing resources like network connections
and locks. Any object that implements __enter__ and __exit__ can be used
after with, and open() already supports this pattern out of the box.

The main reason to prefer `with open(...) as f:` over manually calling
open() and close() is safety: if an exception happens between opening and
closing the file, a manual close() call would be skipped and the file
would stay open, silently leaking a resource — with guarantees cleanup
happens regardless.

Example:
with open("notes.txt", "w") as file:
    file.write("Learning Python RAG\\n")
# file is automatically closed here, even if writing had raised an error

class Timer:
    def __enter__(self):
        print("starting")
        return self
    def __exit__(self, *args):
        print("done")

with Timer():
    print("doing work")
""")

add("file_handling", "Reading and Writing Files", "errors_files", """
Python reads and writes files with open(), best used with a with statement
so the file always closes. The mode argument controls behavior: 'r' for
reading, 'w' for writing and overwriting (destroys existing content!),
and 'a' for appending without touching what's already there. read(),
readlines(), and write() move data in and out of a file.

A common and costly mistake is opening a file in 'w' mode when you meant
'a' — 'w' immediately truncates the file to zero bytes the moment it's
opened, even before you write anything, so any existing content is gone
for good.

Example:
with open("notes.txt", "w") as file:
    file.write("Learning Python RAG\\n")

with open("notes.txt", "a") as file:
    file.write("A second line, appended safely\\n")

with open("notes.txt", "r") as file:
    print(file.read())
""")

add("pathlib", "Working with Paths using pathlib", "errors_files", """
The pathlib module represents file system paths as objects instead of raw
strings, making path building, checking, and manipulation more readable
than manual string concatenation with os.path. Path objects support the /
operator for joining paths in a way that automatically handles
Windows-vs-Unix slash differences, plus methods like exists() and
is_file().

Using pathlib instead of manually building path strings with + or
os.path.join() avoids a whole category of cross-platform bugs, since
Windows uses backslashes and Unix-like systems use forward slashes —
pathlib handles that difference for you automatically.

Example:
from pathlib import Path

folder = Path("data")
file_path = folder / "notes.txt"
print(file_path.exists())
print(file_path.suffix)     # ".txt"
print(file_path.parent)     # "data"
print(file_path.name)       # "notes.txt"
""")

add("json_handling", "Working with JSON", "errors_files", """
The json module converts between Python objects and JSON text. json.dumps()
turns a dict or list into a JSON string, json.loads() parses a JSON string
back into Python objects, and json.dump()/json.load() do the same directly
with files, saving you from manually reading/writing text and converting
it yourself.

Not every Python object converts cleanly to JSON — types like sets,
datetime objects, or custom class instances raise a TypeError from
json.dumps() by default, since JSON only natively understands numbers,
strings, booleans, null, lists, and plain objects (dicts).

Example:
import json

data = {"name": "Sara", "age": 21}
text = json.dumps(data)
parsed = json.loads(text)
print(parsed["name"])   # Sara

with open("student.json", "w") as f:
    json.dump(data, f)
""")

add("csv_handling", "Working with CSV Files", "errors_files", """
The csv module reads and writes CSV (comma-separated values) files without
manually splitting strings on commas, which breaks as soon as a field
itself contains a comma inside quotes. csv.reader() iterates over rows as
plain lists, and csv.DictReader() reads each row as a dictionary keyed by
the header row, which is usually more convenient to work with.

Manually splitting a line with `line.split(",")` looks tempting but is a
real bug magnet: a field like `"Smith, John"` in a name column would get
incorrectly split into two pieces. The csv module correctly understands
quoting and handles this for you.

Example:
import csv

with open("data.csv", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["name"], row["score"])

with open("out.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["name", "score"])
    writer.writerow(["Sara", 91])
""")

add("os_module", "The os Module", "errors_files", """
The os module lets Python interact with the operating system: listing
directory contents, creating or removing folders, checking environment
variables, and building paths in a cross-platform way. os.getenv() is the
standard way to read configuration like API keys from the environment
instead of hardcoding secrets directly into source code.

Reading secrets via os.getenv() (often combined with a .env file and the
python-dotenv library) is the standard, safer pattern used throughout this
very project — hardcoding an API key directly in a .py file is a common
and risky beginner mistake, especially once that code is pushed to a
public GitHub repository.

Example:
import os

files = os.listdir(".")
api_key = os.getenv("OPENROUTER_API_KEY", "")
print(len(files), "files found")
print("key configured:", bool(api_key))
""")

# ------------------------------------------------------ modules_packages --
add("modules_imports", "Modules and Imports", "modules_packages", """
A module is a .py file, and Python lets you reuse code across files with
import. You can import an entire module, import a specific name with
'from module import name', or alias it with 'as' to shorten a long name.
The standard library ships with many ready-to-use modules such as math,
random, os, and datetime, so you rarely need to write common utilities
from scratch.

`from module import *` is generally discouraged in real code: it dumps
every public name from that module into your current namespace, making it
unclear where a given name actually came from and increasing the chance
of accidentally overwriting something.

Example:
import math
from random import randint

print(math.sqrt(16))     # 4.0
print(randint(1, 10))    # a random int between 1 and 10

# discouraged in real projects:
# from math import *
""")

add("packages_init", "Packages and __init__.py", "modules_packages", """
A package is a folder containing related modules, marked as a package by
an __init__.py file (which can be completely empty, or can control what
gets exposed when the package is imported). Packages let you organize a
larger project into a nested import structure, for example
project.utils.helpers, instead of one flat folder full of files.

__init__.py isn't strictly required in modern Python for a folder to be
treated as importable (this is called a "namespace package"), but
including it explicitly is still standard practice for clarity and for
controlling exactly what the package exposes to code that imports it.

Example:
# project/
#   __init__.py
#   utils/
#     __init__.py
#     helpers.py

from project.utils import helpers
from project.utils.helpers import some_function
""")

add("pip_packages", "Installing Packages with pip", "modules_packages", """
pip is Python's package installer, used to add third-party libraries that
are not part of the standard library. Packages are installed from PyPI,
the Python Package Index, and a project's exact dependencies are usually
recorded in a requirements.txt file, so anyone else can recreate the exact
same set of installed packages with one command.

Installing packages globally (without a virtual environment) is a common
source of version conflicts between different projects on the same
machine — this is exactly why requirements.txt plus a per-project virtual
environment (see the venv topic) is the standard, recommended workflow.

Example:
pip install requests
pip install -r requirements.txt
pip freeze > requirements.txt
pip install requests==2.31.0   # pin an exact version
""")

add("datetime_module", "The datetime Module", "modules_packages", """
The datetime module represents dates and times as objects instead of raw
strings, supporting arithmetic like adding days and formatting output in
whatever style you need. datetime.now() gives the current date and time,
and strftime() converts a datetime object into a custom formatted string
using format codes like %Y, %m, and %d.

Comparing or doing arithmetic on raw date strings (like "2026-07-25") is
fragile and error-prone; converting them into real datetime objects first
gives you correct, calendar-aware comparisons and arithmetic, including
handling month lengths and leap years automatically.

Example:
from datetime import datetime, timedelta

now = datetime.now()
tomorrow = now + timedelta(days=1)
print(now.strftime("%Y-%m-%d"))          # e.g. 2026-07-25
print(tomorrow.strftime("%Y-%m-%d"))     # the next calendar day, correctly
""")

add("math_random_modules", "The math and random Modules", "modules_packages", """
The math module provides mathematical functions like sqrt(), floor(), and
constants like pi, for calculations beyond the basic arithmetic operators.
The random module generates pseudo-random numbers, picks a random item
from a sequence with choice(), and shuffles a list in place with
shuffle().

random's numbers are "pseudo-random," not cryptographically secure — they
are predictable if you know the seed and algorithm, so random should never
be used for anything security-sensitive like generating passwords or
tokens; the secrets module exists specifically for that purpose instead.

Example:
import math, random

print(math.sqrt(25))            # 5.0
print(math.floor(4.7))          # 4
print(random.choice([1, 2, 3]))
random.seed(42)                 # makes "random" output reproducible
print(random.randint(1, 100))
""")

add("argparse_cli", "Command-Line Arguments with argparse", "modules_packages", """
The argparse module builds a command-line interface for a script: it
defines expected arguments, generates a --help message automatically from
those definitions, and converts and validates the values the user types.
This is the standard way to make a Python script configurable from the
terminal, instead of hardcoding values or editing the script every time.

argparse automatically produces a working `--help` flag and readable
error messages for missing or malformed arguments, for free — writing
that same validation logic by hand with sys.argv would be far more code
and far more error-prone.

Example:
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--name", required=True)
parser.add_argument("--times", type=int, default=1)
args = parser.parse_args()

for _ in range(args.times):
    print(f"Hello, {args.name}")
""")

# ------------------------------------------------------- current vs. outdated --
add("urllib_requests", "Making HTTP Requests (urllib.request)", "modules_packages", """
The modern way to make an HTTP request in Python's standard library is
urllib.request.urlopen(), or the third-party requests library for a
friendlier, more forgiving API. Both replace the old urllib2 module,
which only existed in Python 2 and was merged into urllib in Python 3.

For anything beyond the simplest one-off request, most developers reach
for the requests library instead of urllib.request directly — its API for
handling headers, JSON bodies, and errors is considerably more
beginner-friendly, even though urllib.request is always available with no
extra installation needed.

Example:
from urllib.request import urlopen

with urlopen("https://docs.python.org") as response:
    html = response.read().decode("utf-8")
print(len(html), "bytes read")

# with the third-party requests library instead:
# import requests
# response = requests.get("https://docs.python.org")
# print(response.status_code, len(response.text))
""")

add("python2_print_statement", "Python 2 print Statement", "basics", """
In Python 2, print was a statement, not a function: you wrote print
"hello" with no parentheses. This syntax was removed in Python 3, where
print is a regular function and requires parentheses: print("hello").
Code written with the old statement form raises a SyntaxError on Python 3
— it won't run at all, not even with a warning.

This is one of the most common signs that a code snippet, tutorial, or
Stack Overflow answer is written for Python 2 and needs to be updated
before running it on a modern Python installation, since Python 2 itself
reached its official end of life in January 2020.

Example:
print "hello"          # Python 2 only — SyntaxError on Python 3
print("hello")          # Correct on Python 3

# print "value:", x     # also Python 2 only
# print("value:", x)     # correct modern equivalent
""", is_current=False, replaces="print_function")

add("distutils_deprecated", "distutils Module (Deprecated)", "modules_packages", """
distutils was the original standard-library tool for packaging and
installing Python modules, used via a setup.py script and commands like
python setup.py install. It was deprecated in Python 3.10 and fully
removed from the standard library in Python 3.12. The modern replacement
is pip together with a pyproject.toml file, which is now the
community-standard way to define and install a package.

If you're following an older tutorial that instructs you to run `python
setup.py install`, that instruction is now outdated on current Python
versions and will likely fail with an import error, since distutils no
longer ships with the interpreter at all.

Example:
python setup.py install   # deprecated / removed — do not use on modern Python
pip install .              # modern equivalent, works from a project folder
pip install -e .           # "editable install," common during development
""", is_current=False, replaces="pip_packages")

add("urllib2_deprecated", "urllib2 Module (Python 2, Removed)", "modules_packages", """
urllib2 was the Python 2 standard-library module for opening URLs and
making HTTP requests, used as urllib2.urlopen(url). It does not exist in
Python 3 at all — trying to import it raises a ModuleNotFoundError, not a
gentler warning, because its functionality was merged into and
reorganized as urllib.request.

Seeing `import urllib2` in a code sample is a strong, immediate signal
that you're looking at Python 2 code that needs to be translated before it
will run on Python 3 — the fix is almost always a straightforward swap to
`from urllib.request import urlopen`.

Example:
import urllib2                       # Python 2 only — ModuleNotFoundError on Python 3
response = urllib2.urlopen(url)

# Python 3 equivalent:
# from urllib.request import urlopen
# response = urlopen(url)
""", is_current=False, replaces="urllib_requests")

# --------------------------------------------------------- concurrency --
add("threading_basics", "Threading Basics", "concurrency", """
The threading module runs multiple pieces of code concurrently within the
same process, which is useful for I/O-bound tasks like network requests
where a thread spends most of its time waiting rather than actively
computing. Each Thread is started with .start() and can be waited on with
.join(), which blocks the main program until that thread finishes.

Because of Python's Global Interpreter Lock (see the GIL topic),
threading does NOT speed up CPU-heavy work — it genuinely helps only when
threads spend time waiting on something external, like a network response
or disk I/O, during which other threads can run.

Example:
import threading

def worker(n):
    print(f"Task {n} running")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()   # wait for all threads to finish before continuing
""")

add("multiprocessing_basics", "Multiprocessing Basics", "concurrency", """
The multiprocessing module runs code in separate processes instead of
threads, each with its own Python interpreter and its own memory space.
This gives true parallelism on multiple CPU cores, making it the right
tool for CPU-bound work like heavy number crunching, unlike threading,
which is limited by the Global Interpreter Lock.

The trade-off is overhead: starting a new process is heavier than
starting a thread, and sharing data between processes requires explicit
mechanisms (like a Queue or shared memory) since processes don't
automatically share memory the way threads in the same process do.

Example:
from multiprocessing import Process

def worker(n):
    print(f"Process {n} running")

if __name__ == "__main__":
    p = Process(target=worker, args=(1,))
    p.start()
    p.join()
""")

add("async_await", "async and await", "concurrency", """
async def defines a coroutine, a function that can pause at await points
without blocking the whole program, which is efficient for handling many
concurrent I/O operations like network calls without the overhead of
threads or processes. asyncio.run() starts the event loop that drives
coroutines, and asyncio.gather() runs several of them concurrently.

async/await shines for I/O-bound workloads with many simultaneous
operations (like a web server handling thousands of connections), but it
doesn't help with CPU-bound work at all, and mixing blocking calls (like a
plain time.sleep() instead of asyncio.sleep()) inside an async function
accidentally blocks the entire event loop.

Example:
import asyncio

async def fetch(n):
    await asyncio.sleep(1)   # non-blocking wait
    return f"result {n}"

async def main():
    results = await asyncio.gather(fetch(1), fetch(2))
    print(results)

asyncio.run(main())
""")

add("gil_explained", "The Global Interpreter Lock (GIL)", "concurrency", """
The GIL is a lock in the standard CPython interpreter that allows only one
thread to execute Python bytecode at a time, even on a multi-core
machine. This means threading does not speed up CPU-bound Python code —
only one thread actually runs Python instructions at any given moment,
regardless of how many CPU cores are available.

The GIL is released automatically while waiting on I/O (network, file,
sleep), which is exactly why threading still helps for I/O-bound work even
though it can't help CPU-bound work. For true CPU parallelism, you need
multiprocessing instead, which sidesteps the GIL entirely by using
separate processes.

Example:
# CPU-bound work (heavy math, image processing): use multiprocessing
# I/O-bound work (network requests, file reads, sleep): threading or
# asyncio both work well, since the GIL is released during the wait
""")

add("queue_module", "The queue Module", "concurrency", """
The queue module provides a thread-safe FIFO queue used to pass data
safely between threads without manually managing locks yourself. Producer
threads call put() to add items, and consumer threads call get() to
retrieve them, blocking automatically until an item becomes available —
this coordination logic would be genuinely tricky and bug-prone to write
correctly by hand.

Using a plain list shared between threads without a Queue is a common
concurrency bug: list operations aren't guaranteed to be safe when
multiple threads modify the list at exactly the same moment, whereas
queue.Queue is specifically designed and tested to be thread-safe.

Example:
import queue, threading

q = queue.Queue()

def producer():
    q.put("data")

threading.Thread(target=producer).start()
print(q.get())   # blocks until an item is available, then returns it
""")

# ----------------------------------------------------- professional_tools --
add("unit_testing", "Unit Testing with unittest / pytest", "professional_tools", """
Unit tests check that individual pieces of code behave correctly and keep
working as the codebase changes. The built-in unittest module uses classes
with assert methods like assertEqual(), while pytest, a popular
third-party library, lets you write plain functions with a simple assert
statement, which most developers find noticeably less boilerplate-heavy.

The real value of tests shows up over time, not on day one: they catch
regressions when you (or a teammate) change code weeks later and
accidentally break something that used to work, long after you've
forgotten the original logic's fine details.

Example:
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0

# run with: pytest test_file.py
""")

add("logging_module", "The logging Module", "professional_tools", """
The logging module records what a program is doing, with severity levels
such as DEBUG, INFO, WARNING, and ERROR, and is the professional
replacement for scattering print() statements through code. Logs can be
routed to the console, a file, or both, with a configurable format
including timestamps — something plain print() doesn't give you for free.

Unlike print(), logging lets you filter by severity level without editing
the code — you can leave DEBUG-level statements in place throughout a
program and simply configure the logger to only show WARNING and above in
production, silencing the noisy detail when you don't need it.

Example:
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Server started")
logging.warning("Low disk space")
logging.error("Failed to connect to database")
""")

add("regex_basics", "Regular Expressions with re", "professional_tools", """
The re module matches and manipulates text using regular expression
patterns. re.search() finds the first match anywhere in a string,
re.findall() returns every match, and re.sub() replaces matches with new
text; patterns use symbols like a digit class and + for one or more
repetitions.

Regular expressions are powerful but easy to write incorrectly in subtle
ways — a pattern that seems to work on your test cases can still fail on
edge cases you didn't think of. For anything beyond simple, well-known
patterns, testing the regex against several real examples before relying
on it is a good habit.

Example:
import re

text = "Call me at 010-1234-5678"
match = re.search(r"\\d{3}-\\d{4}-\\d{4}", text)
print(match.group())   # 010-1234-5678

cleaned = re.sub(r"\\d", "#", text)
print(cleaned)          # "Call me at ###-####-####"
""")

add("type_hints", "Type Hints", "professional_tools", """
Type hints let you annotate variables, function parameters, and return
values with their expected type, using a colon for parameters and an
arrow for the return type. Python does not enforce them at runtime — a
type hint is purely documentation as far as the interpreter is concerned
— but tools like mypy and modern editors use them to catch bugs before
the code ever runs.

Because type hints aren't enforced, passing a value of the "wrong" type
won't cause an immediate error — the mismatch is only caught by a
separate type-checking tool like mypy, or by a human reading the code, not
by Python itself at runtime.

Example:
def greet(name: str, age: int) -> str:
    return f"{name} is {age} years old"

print(greet("Sara", 21))     # works fine
print(greet("Sara", "21"))   # also runs! Python doesn't check the hint
""")

add("f_strings", "String Formatting with f-strings", "professional_tools", """
f-strings, available since Python 3.6, are the modern, preferred way to
build strings containing variable values. Prefix the string with f and
place expressions inside curly braces; Python evaluates them at runtime,
including arbitrary expressions, not just plain variable names. f-strings
also support format specifiers, such as f'{price:.2f}' for exactly two
decimal places.

f-strings are generally faster and more readable than the older
%-formatting or str.format() styles, since the expression sits directly
inside the string rather than in a separate argument list you have to
mentally match up.

Example:
name = "Nour"
score = 87.456
print(f"Hello {name}, your score is {score:.1f}")
print(f"2 + 2 = {2 + 2}")            # expressions work directly inside {}
print(f"{name!r}")                    # !r calls repr() — shows 'Nour' with quotes
""")

add("enumerate_zip", "enumerate() and zip()", "professional_tools", """
enumerate() loops over an iterable while also giving you the index of each
item, avoiding the need for a manual counter variable that you'd otherwise
have to increment by hand. zip() pairs up items from two or more
iterables at the same position, stopping at the shortest one, which is
useful for looping over related lists together in lockstep.

Before enumerate() and zip() existed as idioms, beginners often reach for
`range(len(my_list))` and then index into the list manually — this works,
but enumerate() is both more readable and less error-prone, since there's
no separate counter variable to accidentally misuse.

Example:
names = ["Ali", "Mona"]
scores = [82, 91]
for index, name in enumerate(names):
    print(index, name)

for name, score in zip(names, scores):
    print(name, score)
""")

add("walrus_operator", "The Walrus Operator (:=)", "professional_tools", """
The walrus operator, introduced in Python 3.8, assigns a value to a
variable as part of a larger expression, letting you avoid computing the
same value twice — for example inside a while loop condition or a list
comprehension where you'd otherwise need to call the same function once
to check it and again to use it.

The walrus operator is entirely optional syntactic sugar — anything it
does can be written without it using an extra line of code — so it's best
used where it genuinely improves readability, not just to look clever.

Example:
data = [1, 2, 3, 4, 5]
if (n := len(data)) > 3:
    print(f"List has {n} items, that's a lot")

# without the walrus operator, the same logic needs an extra line:
n = len(data)
if n > 3:
    print(f"List has {n} items, that's a lot")
""")

add("itertools_collections", "The itertools and collections Modules", "professional_tools", """
itertools provides fast, memory-efficient building blocks for looping,
such as chain() to combine several iterables into one and product() for
generating all combinations. collections offers specialized data
structures beyond the built-ins, such as Counter for counting items and
defaultdict for dictionaries that supply an automatic default value
instead of raising a KeyError on a missing key.

defaultdict in particular eliminates a very common pattern of manually
checking `if key not in my_dict: my_dict[key] = []` before appending —
with defaultdict(list), that check becomes unnecessary, since a missing
key is created automatically with the given default.

Example:
from collections import Counter, defaultdict

words = ["a", "b", "a", "c", "b", "a"]
counts = Counter(words)
print(counts.most_common(2))   # [('a', 3), ('b', 2)]

groups = defaultdict(list)
groups["fruits"].append("apple")   # no KeyError, list created automatically
print(dict(groups))                 # {'fruits': ['apple']}
""")

# ---------------------------------------------------------------- basics (continued) --
add("conditionals", "Conditional Statements (if / elif / else)", "basics", """
Conditional statements let a program choose which block of code to run
based on a boolean expression. Python uses if, elif, and else, and relies
on indentation instead of curly braces to mark blocks — this makes
consistent indentation a functional requirement, not just a style choice,
since mixing tabs and spaces or indenting inconsistently causes real
errors. Comparison and logical operators are commonly used inside the
condition.

You can chain as many elif blocks as needed, and Python evaluates them in
order, stopping at the first one that's True — later elif/else branches
are simply skipped, which is worth remembering when conditions could
overlap.

Example:
score = 82
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
print(grade)   # B — the first true condition wins, later ones are skipped
""")

add("for_while_loops", "For and While Loops", "basics", """
A for loop iterates over the items of a sequence such as a list, string,
or range, running the loop body once per item. A while loop repeats as
long as a condition stays true, and is the right choice when you do not
know in advance how many iterations you need. break exits a loop early,
and continue skips straight to the next iteration without running the
rest of the current one.

A while loop that forgets to update the variable used in its condition
runs forever — this is one of the most common beginner bugs, and it's why
every while loop needs a clear path toward eventually making its
condition False.

Example:
for i in range(5):
    if i == 3:
        continue   # skip printing 3, move to the next iteration
    print(i)

count = 0
while count < 3:
    print("count is", count)
    count += 1   # forgetting this line would loop forever
""")

add("nested_conditionals", "Nested if Statements", "basics", """
A nested if statement is an if block placed inside another if (or elif or
else) block, used when a second decision only makes sense after the first
condition is already true. This differs from elif: an elif chain checks
alternatives at the same level and stops at the first true one, while
nesting checks a follow-up condition only inside a specific branch that's
already been entered.

Overusing nesting makes code progressively harder to read — three or four
levels deep, it becomes difficult to track which condition you're
actually inside. When conditions are mutually exclusive alternatives
rather than genuinely dependent follow-ups, elif is usually the clearer
choice.

Example:
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("Entry allowed")
    else:
        print("ID required")
else:
    print("Too young")
""")


# ------------------------------------------------------------- advanced --
add("iterator_protocol", "Iterators and the Iterator Protocol", "advanced", """
An iterable is any object you can loop over; an iterator is the object that
actually produces values one at a time via __next__(), raising
StopIteration when exhausted. iter(obj) gets an iterator from an iterable,
and next(it) pulls the next value — this is literally what a for loop does
under the hood.

Implementing __iter__ and __next__ on your own class lets it work
directly with for loops, list(), and every other place Python expects an
iterable — without this protocol, none of that works even if your object
otherwise "feels" like a sequence.

Example:
class Countdown:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1

for n in Countdown(3):
    print(n)   # 3 2 1
""")

add("generator_advanced", "Advanced Generators (yield from, send)", "advanced", """
yield from delegates part of a generator's work to another iterable,
flattening nested generators without an explicit inner loop. send(value)
resumes a paused generator and injects a value into it, which becomes the
result of the yield expression that paused it — turning a generator into
a two-way communication channel, not just a one-way value producer.

send() is genuinely rarely used in everyday code, but yield from is common
for cleanly combining several generators into one, and understanding it
also clarifies how Python's own async/await machinery is built underneath.

Example:
def inner():
    yield 1
    yield 2

def outer():
    yield 0
    yield from inner()   # delegates to inner(), no manual loop needed
    yield 3

print(list(outer()))   # [0, 1, 2, 3]
""")

add("contextlib_manager", "Custom Context Managers with contextlib", "advanced", """
Writing a full class with __enter__ and __exit__ for a simple context
manager is often more boilerplate than needed. contextlib.contextmanager
lets you write one as a regular generator function instead: code before
yield runs on entry, code after yield runs on exit (including on an
exception, if wrapped in try/finally).

This is the pragmatic middle ground between "just write two lines
manually" and "define a whole class" — most simple setup/teardown logic
fits comfortably in a single small generator function this way.

Example:
from contextlib import contextmanager

@contextmanager
def timer():
    print("starting")
    yield
    print("done")

with timer():
    print("doing work")
# starting / doing work / done
""")

add("functools_lru_cache", "Caching with functools.lru_cache", "advanced", """
@lru_cache automatically memoizes a function's results: calling it again
with the same arguments returns the cached answer instantly instead of
recomputing it. It's a decorator, so adding caching to an existing pure
function (same input always gives same output, no side effects) takes
one line, no manual dictionary needed.

lru_cache should only be used on functions without side effects and with
hashable arguments — calling it on a function that reads changing external
state (like the current time) will incorrectly return stale cached
results.

Example:
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(30))   # fast, even though naive recursion would be very slow here
""")

add("functools_partial", "functools.partial", "advanced", """
functools.partial creates a new function with some arguments already
"locked in," letting you reuse a general function as a more specific one
without writing a wrapper by hand. It's commonly used to adapt a function
to fit an API (like a callback) that expects fewer arguments than the
original function takes.

partial is a cleaner, more explicit alternative to writing a small lambda
just to pre-fill arguments, and it also preserves useful metadata about
the original function that a hand-written lambda wrapper would lose.

Example:
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))   # 25
print(cube(2))     # 8
""")

add("mro_super", "Method Resolution Order and super()", "advanced", """
When a class inherits from multiple parents, Python needs a defined order
to search for a method — this is the Method Resolution Order (MRO),
computed with the C3 linearization algorithm and viewable via
ClassName.__mro__. super() doesn't mean "my direct parent" — it means
"the next class in the MRO," which matters once multiple inheritance is
involved.

This distinction rarely matters for simple single-inheritance code, but
it's essential to understand correctly once a class hierarchy uses
multiple inheritance (like mixins), or method calls silently resolve to
an unexpected class.

Example:
class A:
    def greet(self):
        return "A"

class B(A):
    def greet(self):
        return "B -> " + super().greet()

class C(A):
    def greet(self):
        return "C -> " + super().greet()

class D(B, C):
    def greet(self):
        return "D -> " + super().greet()

print(D().greet())        # D -> B -> C -> A
print(D.__mro__)          # shows the exact resolution order
""")

add("enum_module", "The enum Module", "advanced", """
The enum module defines a fixed, named set of related constants, replacing
error-prone patterns like using plain strings or magic numbers for
statuses or categories. Enum members compare by identity and print with a
readable name, catching typos ("Statuss.ACTIV") at import time as an
AttributeError instead of silently creating a new, unintended string.

Using an Enum instead of raw strings for something like an order's status
means a typo becomes an immediate, loud error, rather than a status
comparison that silently always evaluates to False somewhere deep in the
code.

Example:
from enum import Enum

class Status(Enum):
    PENDING = 1
    SHIPPED = 2
    DELIVERED = 3

order_status = Status.SHIPPED
print(order_status)               # Status.SHIPPED
print(order_status == Status.SHIPPED)  # True
""")

add("namedtuple", "collections.namedtuple", "advanced", """
namedtuple creates a lightweight, immutable class with named fields,
combining a tuple's memory efficiency with attribute-style access
(point.x instead of point[0]) — readable field names without the full
overhead of defining a regular class by hand.

namedtuple predates dataclasses and is still common in existing codebases
and some standard-library return values; dataclasses (covered elsewhere in
this project) are the more modern choice when you also need mutability or
default values, but namedtuple remains simpler for pure, immutable data.

Example:
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p.x, p.y)     # 3 4
print(p)             # Point(x=3, y=4)
print(p[0])          # 3 — still works like a regular tuple too
""")

add("structural_pattern_matching", "Structural Pattern Matching (match/case)", "advanced", """
match/case, introduced in Python 3.10, is a more powerful alternative to
long if/elif chains, able to match not just values but also structure:
unpacking a list, checking a dict's shape, or matching a class's
attributes, all in the pattern itself rather than in separate manual
checks.

It's not simply a "switch statement" from other languages — the pattern
can bind variables and destructure data as part of matching, which a
traditional switch can't do, making it genuinely more expressive for many
real dispatch problems.

Example:
def describe(value):
    match value:
        case 0:
            return "zero"
        case [x, y]:
            return f"a pair: {x}, {y}"
        case {"name": name}:
            return f"a dict with name={name}"
        case _:
            return "something else"

print(describe([1, 2]))          # a pair: 1, 2
print(describe({"name": "Sara"}))  # a dict with name=Sara
""")

add("exception_chaining", "Exception Chaining (raise ... from)", "advanced", """
When you catch one exception and raise a different, more specific one in
its place, `raise NewError(...) from original_error` preserves the
original exception as the new one's __cause__, so the traceback shows
both: what ultimately went wrong, and what originally triggered it. Raising
without `from` inside an except block still chains automatically as
"context," but explicit `from` makes the relationship clearer.

This matters a lot for debugging real production issues — without
chaining, converting a low-level exception into a more meaningful one
silently discards the original root cause, making the real bug much
harder to trace later.

Example:
def load_config():
    try:
        return 1 / 0
    except ZeroDivisionError as e:
        raise RuntimeError("Config could not be loaded") from e

# raises RuntimeError, but the traceback also shows the original
# ZeroDivisionError as "The above exception was the direct cause of..."
""")

add("copy_deepcopy", "copy vs deepcopy", "advanced", """
Assigning a variable to another (b = a) never copies anything for mutable
objects — both names point to the same object in memory. copy.copy()
makes a shallow copy (a new outer object, but nested objects inside it are
still shared), while copy.deepcopy() recursively copies everything,
including nested lists, dicts, and objects, so nothing is shared at all.

Using a shallow copy() when you actually needed deepcopy() is a subtle,
common bug: the outer list looks independent, but mutating a nested list
inside it still affects the "copy" too, since that inner list was never
actually duplicated.

Example:
import copy

original = [[1, 2], [3, 4]]
shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow[0].append(99)
print(original)   # [[1, 2, 99], [3, 4]] — original changed too!
print(deep)        # [[1, 2], [3, 4]] — deep copy is fully independent
""")

add("bytes_vs_str", "Bytes, Strings, and Encoding", "advanced", """
str represents text (Unicode characters); bytes represents raw binary data.
encode() converts a str to bytes using a specified encoding (usually
UTF-8), and decode() converts bytes back to str. Files opened in text mode
('r') give you str, while files opened in binary mode ('rb') give you
bytes — mixing the two up is a very common source of TypeErrors.

Networking, file I/O at the OS level, and many APIs work in bytes, not
str, which is exactly why encode()/decode() come up constantly once a
program needs to talk to the outside world instead of just holding text
in memory.

Example:
text = "café"
encoded = text.encode("utf-8")
print(encoded)                # b'caf\\xc3\\xa9'
print(encoded.decode("utf-8"))  # café — back to the original string

# text + encoded   # would raise: TypeError, can't mix str and bytes
""")

add("type_hints_advanced", "Advanced Type Hints (Optional, Union, Generic)", "advanced", """
Beyond simple types like str and int, the typing module supports more
expressive hints: Optional[X] means "X or None," Union[X, Y] means
"either X or Y," and generics like List[int] or Dict[str, int] describe a
container's contents, not just its outer type. Since Python 3.10, X | Y
is accepted as a shorter equivalent to Union[X, Y].

Like basic type hints, these are still purely documentation as far as
Python itself is concerned at runtime — the real payoff is a type checker
like mypy catching a mismatch (like passing None where Optional wasn't
declared) before the code ever runs.

Example:
from typing import Optional, Union

def find_user(user_id: int) -> Optional[str]:
    users = {1: "Sara", 2: "Omar"}
    return users.get(user_id)   # returns str, or None if not found

def parse(value: Union[int, str]) -> int:
    return int(value)
""")

add("descriptors", "Descriptors", "advanced", """
A descriptor is a class that defines __get__, __set__, or __delete__ and
is used as a class attribute on another class, letting it intercept and
customize attribute access on every instance of that class. @property
(covered elsewhere in this project) is actually implemented internally
using the descriptor protocol — descriptors are the more general,
lower-level mechanism underneath it.

Descriptors are an advanced tool mostly relevant when building reusable
attribute behavior shared across many classes (validation, type
enforcement, lazy loading) — for a single one-off case, @property alone
is usually simpler and sufficient.

Example:
class PositiveNumber:
    def __set_name__(self, owner, name):
        self.name = "_" + name
    def __get__(self, obj, objtype=None):
        return getattr(obj, self.name, None)
    def __set__(self, obj, value):
        if value < 0:
            raise ValueError("Must be positive")
        setattr(obj, self.name, value)

class Product:
    price = PositiveNumber()   # descriptor used as a class attribute

p = Product()
p.price = 10
print(p.price)   # 10
# p.price = -5   # would raise: ValueError
""")

add("singleton_pattern", "The Singleton Design Pattern", "advanced", """
The Singleton pattern ensures a class has only ever one instance across
the whole program, and provides one global point of access to it —
useful for things like a shared configuration object or a single database
connection pool that genuinely should not be duplicated.

In Python specifically, a Singleton is often better replaced with a
module-level object (since modules are already only imported once and
naturally act like a singleton), or dependency injection — the classic
class-based Singleton pattern is more associated with languages that lack
Python's simple, naturally-singleton module system.

Example:
class Singleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

a = Singleton()
b = Singleton()
print(a is b)   # True — both names point to the exact same object
""")


def _build_fallback_documents():
    """Kept for 00_scrape_documents.py, which imports this to get the
    curated per-topic fallback text whenever scraping a specific topic
    fails (network issue, moved page, renamed anchor)."""
    return _fallback_documents


_CONFLICT_TEST_IDS = {
    "urllib_requests", "python2_print_statement", "distutils_deprecated", "urllib2_deprecated",
}


def _load_documents():
    conflict_test_docs = [d for d in _fallback_documents if d["id"] in _CONFLICT_TEST_IDS]

    if _SCRAPED_PATH.exists():
        try:
            scraped = json.loads(_SCRAPED_PATH.read_text(encoding="utf-8"))
            if scraped:
                print(f"[01_documents] Loaded {len(scraped)} scraped documents "
                      f"from {_SCRAPED_PATH.name}")
                return scraped + conflict_test_docs
        except (json.JSONDecodeError, OSError) as exc:
            print(f"[01_documents] Could not read {_SCRAPED_PATH.name} ({exc}), "
                  f"falling back to curated topics.")
    else:
        print(f"[01_documents] {_SCRAPED_PATH.name} not found - using curated topics. "
              f"Run python 00_scrape_documents.py to build it from docs.python.org.")
    return _fallback_documents


documents = _load_documents()
