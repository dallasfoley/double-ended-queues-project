# Project 5: Deque README
## Overview
Project 5 for CSE 331 FS23 is a detailed exploration and implementation of a Deque (Double-Ended Queue) using both array-based and linked-list-based structures. The project involves creating a Circular Deque and a Circular Doubly Linked List (CDLL) to understand the differences in performance and applications of these data structures.

## Features
CircularDeque: An array-based implementation of a deque with operations to add and remove elements from both ends.<br />
CDLLNode: A node class used for the linked list implementation, containing value, next, and previous pointers.<br />
CDLL (Circular Doubly Linked List): A linked-list-based implementation of a deque.<br />
CDLLCD (Circular Doubly Linked List Circular Deque): An interface that utilizes the CDLL for deque operations.<br />
Performance Comparison (Optional): Utilizes matplotlib to compare the performance of array-based and linked-list-based deques under various operations.<br />
## Usage
Creating Deques:<br />
CircularDeque: Use the CircularDeque class to create an array-based deque.<br />
CDLLCD: Use the CDLLCD class to create a linked-list-based deque.<br />
Basic Operations:<br />
enqueue: Adds an element to either the front or back of the deque.<br />
dequeue: Removes and returns an element from either the front or back of the deque.<br />
front_element / back_element: Retrieves the front/back element of the deque without removing it.<br />
Utility Functions:<br />
__len__: Returns the number of elements in the deque.<br />
is_empty: Checks whether the deque is empty.<br />
grow / shrink: Dynamically adjusts the size of the underlying array in CircularDeque.<br />

## Installation
Requires Python 3.7 or newer. If performance comparison is desired, install matplotlib:<br />

bash:<br /><br />

pip install matplotlib
## Dependencies
Python 3.7+<br />
Optional: matplotlib for performance comparison<br />
## Contributors
Starter code authored by Gabriel Sotelo

## Author
Dallas Foley
