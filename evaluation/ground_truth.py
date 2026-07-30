# =========================================================================
# Ground-truth queries for retrieval evaluation.
# Two queries per topic, phrased differently from each other (and from the
# topic title), so the evaluation genuinely tests whether retrieval
# understands *meaning* across different ways of asking the same thing —
# the same idea as Lab6/Lab7/Lab8's ground_truth dicts, just with more
# queries per topic for a more reliable average.
# =========================================================================

ground_truth = [
    {"query": "How do I show text on the screen in Python?", "relevant_document_id": "print_function"},
    {"query": "What function do I use to output something to the console?", "relevant_document_id": "print_function"},

    {"query": "What are the basic types of values a variable can hold?", "relevant_document_id": "variables_data_types"},
    {"query": "Do I need to declare a type before creating a variable in Python?", "relevant_document_id": "variables_data_types"},

    {"query": "How can my program read something the user types?", "relevant_document_id": "input_function"},
    {"query": "How do I pause the program and wait for keyboard input?", "relevant_document_id": "input_function"},

    {"query": "How do I convert a string into a number?", "relevant_document_id": "type_casting"},
    {"query": "How do I turn a number into text for printing?", "relevant_document_id": "type_casting"},

    {"query": "What is the difference between / and // in Python?", "relevant_document_id": "arithmetic_operators"},
    {"query": "How do I get the remainder after dividing two numbers?", "relevant_document_id": "arithmetic_operators"},

    {"query": "How do I combine two conditions with and/or?", "relevant_document_id": "comparison_logical_operators"},
    {"query": "What symbols do I use to check if two values are equal or not equal?", "relevant_document_id": "comparison_logical_operators"},

    {"query": "How do I write a note in my code that Python ignores?", "relevant_document_id": "comments_docstrings"},
    {"query": "What is the string right under a function definition used for?", "relevant_document_id": "comments_docstrings"},

    {"query": "What does None mean in Python?", "relevant_document_id": "booleans_none"},
    {"query": "Is True actually treated as the number 1?", "relevant_document_id": "booleans_none"},

    {"query": "How do I add an item to the end of a list?", "relevant_document_id": "lists_and_methods"},
    {"query": "How do I delete a specific value from a list?", "relevant_document_id": "lists_and_methods"},

    {"query": "Is there a shortcut to build a list from a loop in one line?", "relevant_document_id": "list_comprehension"},
    {"query": "How do I create a list of squared numbers without writing a for loop block?", "relevant_document_id": "list_comprehension"},

    {"query": "What is an immutable ordered collection in Python called?", "relevant_document_id": "tuples"},
    {"query": "Can I use a group of coordinates as a dictionary key?", "relevant_document_id": "tuples"},

    {"query": "How do I store data as key and value pairs?", "relevant_document_id": "dictionaries"},
    {"query": "How do I safely look up a key that might not exist without crashing?", "relevant_document_id": "dictionaries"},

    {"query": "Can I build a dictionary in a single line like a list comprehension?", "relevant_document_id": "dict_comprehension"},
    {"query": "How do I map each name in a list to its length using one expression?", "relevant_document_id": "dict_comprehension"},

    {"query": "How do I remove duplicate values from a collection?", "relevant_document_id": "sets"},
    {"query": "How do I find the common items between two groups of values?", "relevant_document_id": "sets"},

    {"query": "How do I remove extra spaces or change text to lowercase?", "relevant_document_id": "string_methods"},
    {"query": "How do I combine a list of words back into one sentence?", "relevant_document_id": "string_methods"},

    {"query": "How do I get part of a list using start and stop positions?", "relevant_document_id": "slicing"},
    {"query": "How do I reverse a list without writing a loop?", "relevant_document_id": "slicing"},

    {"query": "How do I order a list from smallest to largest?", "relevant_document_id": "sorting_data"},
    {"query": "How do I sort a list of names by score instead of alphabetically?", "relevant_document_id": "sorting_data"},

    {"query": "How do I split a list into separate variables at once?", "relevant_document_id": "unpacking"},
    {"query": "How do I collect the extra items into one variable while assigning?", "relevant_document_id": "unpacking"},

    {"query": "How do I pass a variable number of arguments into a function?", "relevant_document_id": "functions_args"},
    {"query": "How do I give a function a default value for a parameter?", "relevant_document_id": "functions_args"},

    {"query": "What is a quick one-line anonymous function called?", "relevant_document_id": "lambda_functions"},
    {"query": "How do I write a tiny function inline without using def?", "relevant_document_id": "lambda_functions"},

    {"query": "How do I apply a function to every item in a list without a loop?", "relevant_document_id": "map_filter_reduce"},
    {"query": "How do I keep only the even numbers from a list in one line?", "relevant_document_id": "map_filter_reduce"},

    {"query": "How can I add extra behavior to a function without editing it?", "relevant_document_id": "decorators"},
    {"query": "What is the @ symbol above a function definition for?", "relevant_document_id": "decorators"},

    {"query": "How do I create a sequence of values without storing them all in memory?", "relevant_document_id": "generators"},
    {"query": "What keyword pauses a function and remembers where it left off?", "relevant_document_id": "generators"},

    {"query": "What is a function that remembers variables from its outer scope?", "relevant_document_id": "closures"},
    {"query": "How does an inner function keep access to the outer function's variable after it returns?", "relevant_document_id": "closures"},

    {"query": "How does a function call itself to solve a problem?", "relevant_document_id": "recursion"},
    {"query": "What stops a self-calling function from running forever?", "relevant_document_id": "recursion"},

    {"query": "How do I define a blueprint for creating objects?", "relevant_document_id": "oop_classes"},
    {"query": "What does self mean inside a class method?", "relevant_document_id": "oop_classes"},

    {"query": "How can one class reuse the code of another class?", "relevant_document_id": "oop_inheritance"},
    {"query": "How do I call the parent class's constructor from a subclass?", "relevant_document_id": "oop_inheritance"},

    {"query": "How can different classes share the same method name but behave differently?", "relevant_document_id": "polymorphism"},
    {"query": "Can a Dog and a Cat class both have a speak method that returns different things?", "relevant_document_id": "polymorphism"},

    {"query": "How do I hide internal data of a class from outside access?", "relevant_document_id": "encapsulation"},
    {"query": "What does a double underscore before an attribute name do?", "relevant_document_id": "encapsulation"},

    {"query": "How do I customize what print() shows for my own object?", "relevant_document_id": "magic_methods"},
    {"query": "What method controls how the == operator compares two objects?", "relevant_document_id": "magic_methods"},

    {"query": "What is a method that does not need access to the object itself?", "relevant_document_id": "static_class_methods"},
    {"query": "What is the difference between a method that takes cls and one that takes self?", "relevant_document_id": "static_class_methods"},

    {"query": "How do I make a method act like a computed attribute?", "relevant_document_id": "properties"},
    {"query": "How can I add validation when someone assigns a new value to an attribute?", "relevant_document_id": "properties"},

    {"query": "How do I force subclasses to implement a certain method?", "relevant_document_id": "abstract_classes"},
    {"query": "Can I prevent a class from ever being instantiated directly?", "relevant_document_id": "abstract_classes"},

    {"query": "Is there a shortcut to avoid writing __init__ by hand for simple classes?", "relevant_document_id": "dataclasses"},
    {"query": "What decorator auto-generates a constructor and repr for a simple data class?", "relevant_document_id": "dataclasses"},

    {"query": "How do I stop my program from crashing when an error happens?", "relevant_document_id": "error_handling"},
    {"query": "What code always runs whether or not an exception happened?", "relevant_document_id": "error_handling"},

    {"query": "How do I create my own error type?", "relevant_document_id": "custom_exceptions"},
    {"query": "How do I raise a specific error for insufficient balance in my app?", "relevant_document_id": "custom_exceptions"},

    {"query": "What automatically closes a file even if something goes wrong?", "relevant_document_id": "context_managers"},
    {"query": "What do __enter__ and __exit__ do?", "relevant_document_id": "context_managers"},

    {"query": "How do I save text into a file on disk?", "relevant_document_id": "file_handling"},
    {"query": "What is the difference between opening a file in 'w' mode and 'a' mode?", "relevant_document_id": "file_handling"},

    {"query": "How do I check if a file exists in a modern, readable way?", "relevant_document_id": "pathlib"},
    {"query": "How do I join a folder name and file name into one path object?", "relevant_document_id": "pathlib"},

    {"query": "How do I convert a Python dictionary into JSON text?", "relevant_document_id": "json_handling"},
    {"query": "How do I parse a JSON string back into a Python object?", "relevant_document_id": "json_handling"},

    {"query": "How do I read data from a spreadsheet-style file?", "relevant_document_id": "csv_handling"},
    {"query": "How do I read each row of a CSV as a dictionary keyed by column name?", "relevant_document_id": "csv_handling"},

    {"query": "How do I read an environment variable in my script?", "relevant_document_id": "os_module"},
    {"query": "How do I list all the files inside a folder?", "relevant_document_id": "os_module"},

    {"query": "How do I reuse code from another .py file?", "relevant_document_id": "modules_imports"},
    {"query": "How do I give an imported module a shorter alias?", "relevant_document_id": "modules_imports"},

    {"query": "How do I organize multiple related modules into a folder?", "relevant_document_id": "packages_init"},
    {"query": "What is the __init__.py file used for?", "relevant_document_id": "packages_init"},

    {"query": "How do I install a third-party library?", "relevant_document_id": "pip_packages"},
    {"query": "How do I generate a requirements.txt from what's currently installed?", "relevant_document_id": "pip_packages"},

    {"query": "How do I get today's date in Python?", "relevant_document_id": "datetime_module"},
    {"query": "How do I add one day to a date object?", "relevant_document_id": "datetime_module"},

    {"query": "How do I generate a random number?", "relevant_document_id": "math_random_modules"},
    {"query": "How do I calculate a square root in Python?", "relevant_document_id": "math_random_modules"},

    {"query": "How do I make my script accept options from the terminal?", "relevant_document_id": "argparse_cli"},
    {"query": "How do I make a --name flag required when running my script?", "relevant_document_id": "argparse_cli"},

    {"query": "How do I run several tasks at the same time using threads?", "relevant_document_id": "threading_basics"},
    {"query": "How do I wait for a background thread to finish before continuing?", "relevant_document_id": "threading_basics"},

    {"query": "How do I use multiple CPU cores for heavy computation?", "relevant_document_id": "multiprocessing_basics"},
    {"query": "What is the difference between a thread and a separate process in Python?", "relevant_document_id": "multiprocessing_basics"},

    {"query": "How do I write non-blocking code that waits on network calls?", "relevant_document_id": "async_await"},
    {"query": "What does the await keyword actually do?", "relevant_document_id": "async_await"},

    {"query": "Why doesn't threading speed up CPU-heavy Python code?", "relevant_document_id": "gil_explained"},
    {"query": "What lock only allows one thread to run Python bytecode at a time?", "relevant_document_id": "gil_explained"},

    {"query": "How do I safely pass data between threads?", "relevant_document_id": "queue_module"},
    {"query": "What data structure blocks automatically until an item is available?", "relevant_document_id": "queue_module"},

    {"query": "How do I write automated tests for my functions?", "relevant_document_id": "unit_testing"},
    {"query": "What is the difference between unittest and pytest?", "relevant_document_id": "unit_testing"},

    {"query": "What is the professional way to record what my program is doing?", "relevant_document_id": "logging_module"},
    {"query": "Should I use print statements or something else for debugging a real project?", "relevant_document_id": "logging_module"},

    {"query": "How do I search text for a phone number pattern?", "relevant_document_id": "regex_basics"},
    {"query": "How do I replace every match of a pattern in a string?", "relevant_document_id": "regex_basics"},

    {"query": "How do I document the expected type of a function's parameters?", "relevant_document_id": "type_hints"},
    {"query": "Does Python enforce type annotations at runtime?", "relevant_document_id": "type_hints"},

    {"query": "What is the modern way to insert variables into a string?", "relevant_document_id": "f_strings"},
    {"query": "How do I show a floating point number with only two decimal places?", "relevant_document_id": "f_strings"},

    {"query": "How do I get both the index and the value while looping?", "relevant_document_id": "enumerate_zip"},
    {"query": "How do I loop over two lists together, pairing up matching positions?", "relevant_document_id": "enumerate_zip"},

    {"query": "What operator lets me assign and check a value in one condition?", "relevant_document_id": "walrus_operator"},
    {"query": "What symbol was introduced in Python 3.8 for assignment inside expressions?", "relevant_document_id": "walrus_operator"},

    {"query": "How do I count how many times each item appears in a list?", "relevant_document_id": "itertools_collections"},
    {"query": "What data structure gives a default value automatically for missing keys?", "relevant_document_id": "itertools_collections"},

    # --- added later: topics not covered by the original 61-topic ground truth ---
    {"query": "How do I make my program choose between two paths based on a condition?", "relevant_document_id": "conditionals"},
    {"query": "What keyword checks an additional condition after an if fails?", "relevant_document_id": "conditionals"},

    {"query": "How do I repeat an action a fixed number of times?", "relevant_document_id": "for_while_loops"},
    {"query": "What loop keeps running as long as a condition stays true?", "relevant_document_id": "for_while_loops"},

    {"query": "How do I put an if statement inside another if statement?", "relevant_document_id": "nested_conditionals"},
    {"query": "What's the difference between elif and nested if statements?", "relevant_document_id": "nested_conditionals"},

    {"query": "How do I fetch a web page's HTML in modern Python 3?", "relevant_document_id": "urllib_requests"},
    {"query": "What replaced urllib2 in Python 3?", "relevant_document_id": "urllib_requests"},

    {"query": "Why does print \"hello\" give a syntax error in Python 3?", "relevant_document_id": "python2_print_statement"},
    {"query": "How did print work without parentheses in old Python code?", "relevant_document_id": "python2_print_statement"},

    {"query": "Is python setup.py install still the recommended way to install a package?", "relevant_document_id": "distutils_deprecated"},
    {"query": "What packaging tool was removed from the standard library in Python 3.12?", "relevant_document_id": "distutils_deprecated"},

    {"query": "How do I open a URL with urllib2.urlopen?", "relevant_document_id": "urllib2_deprecated"},
    {"query": "Why do I get ModuleNotFoundError when importing urllib2 in Python 3?", "relevant_document_id": "urllib2_deprecated"},

    # --- added later: 15 new advanced topics ---
    {"query": "How does a for loop actually get values one at a time under the hood?", "relevant_document_id": "iterator_protocol"},
    {"query": "How do I make my own class work with Python's for loop?", "relevant_document_id": "iterator_protocol"},

    {"query": "How do I combine two generators into one without an extra loop?", "relevant_document_id": "generator_advanced"},
    {"query": "What does yield from actually do?", "relevant_document_id": "generator_advanced"},

    {"query": "Is there a shorter way to write a context manager than a full class?", "relevant_document_id": "contextlib_manager"},
    {"query": "How do I use the @contextmanager decorator?", "relevant_document_id": "contextlib_manager"},

    {"query": "How do I avoid recomputing the same expensive function call twice?", "relevant_document_id": "functools_lru_cache"},
    {"query": "What does the @lru_cache decorator do?", "relevant_document_id": "functools_lru_cache"},

    {"query": "How do I create a version of a function with some arguments already filled in?", "relevant_document_id": "functools_partial"},
    {"query": "What is functools.partial used for?", "relevant_document_id": "functools_partial"},

    {"query": "In multiple inheritance, which parent's method actually runs?", "relevant_document_id": "mro_super"},
    {"query": "Does super() always call my direct parent class?", "relevant_document_id": "mro_super"},

    {"query": "How do I define a fixed set of named constant options in Python?", "relevant_document_id": "enum_module"},
    {"query": "What is the enum module used for?", "relevant_document_id": "enum_module"},

    {"query": "How do I create a tuple where I can access fields by name instead of index?", "relevant_document_id": "namedtuple"},
    {"query": "What is collections.namedtuple?", "relevant_document_id": "namedtuple"},

    {"query": "Is there a modern alternative to long if/elif chains in Python?", "relevant_document_id": "structural_pattern_matching"},
    {"query": "How does match/case work in Python?", "relevant_document_id": "structural_pattern_matching"},

    {"query": "How do I raise a new exception while keeping track of the original one that caused it?", "relevant_document_id": "exception_chaining"},
    {"query": "What does raise ... from do?", "relevant_document_id": "exception_chaining"},

    {"query": "Why did changing my 'copied' list also change the original?", "relevant_document_id": "copy_deepcopy"},
    {"query": "What's the difference between copy.copy and copy.deepcopy?", "relevant_document_id": "copy_deepcopy"},

    {"query": "Why do I get an error mixing text and binary data in Python?", "relevant_document_id": "bytes_vs_str"},
    {"query": "How do I convert a string to bytes and back?", "relevant_document_id": "bytes_vs_str"},

    {"query": "How do I say a function argument is optional and might be None?", "relevant_document_id": "type_hints_advanced"},
    {"query": "What does Union or Optional mean in a type hint?", "relevant_document_id": "type_hints_advanced"},

    {"query": "How does @property actually work internally?", "relevant_document_id": "descriptors"},
    {"query": "What is a descriptor in Python?", "relevant_document_id": "descriptors"},

    {"query": "How do I make sure a class only ever has one instance?", "relevant_document_id": "singleton_pattern"},
    {"query": "What is the Singleton design pattern?", "relevant_document_id": "singleton_pattern"},
]
