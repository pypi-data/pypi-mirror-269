# Closed/Open Address Hashing (Chaining) with hasharray

## Overview

The hasharray package provides an implementation of closed address hashing (chaining) using a hash array data structure. Closed address hashing is a way of efficiently store and retrieve key-value pairs in a hash table.

## Features

- Efficient storage and retrieval of key-value pairs using closed address hashing (chaining)
- Support for a wide range of data types as keys and values
- Toggling open addressing allowing automatic resizing of the hash array to maintain optimal performance
- Collision resolution through chaining, where multiple key-value pairs with the same hash value are stored in a linked list

## Installation

To use the hasharray package, you need to have Python installed. You can install the package using pip:

```
pip install hasharray
```