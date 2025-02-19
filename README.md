[![Python Tests](https://github.com/RishitLaddha/session23/actions/workflows/tests.yml/badge.svg)](https://github.com/RishitLaddha/session23/actions/workflows/tests.yml)

<img width="1225" alt="Screenshot 2025-02-19 at 07 18 16" src="https://github.com/user-attachments/assets/af25064f-c7d7-45fa-87b7-d766773dda14" />



# UserProfileManager System

The UserProfileManager System is designed to manage user profiles with a focus on robust data validation, memory-efficient caching, and clear property resolution behavior. The system handles three core attributes for each user profile: **username**, **email**, and **last_login**. Each attribute is subject to specific validation criteria, and the system leverages advanced Python techniques to ensure data integrity and efficient resource management.

---

## Project Expectations

The project required the implementation of a system capable of managing user profiles while enforcing strict validation rules for each profile attribute. The system was expected to perform the following:

1. **Data Validation Using Descriptors**  
   Each attribute of the user profile needed to be validated before being stored. For instance, the username must be a non-empty string, the email must contain certain characters to be considered valid, and the last_login attribute must either be a valid datetime object or be set to None. To achieve this, the solution employs a custom descriptor that encapsulates the logic for validating each value before assignment.

2. **Property Resolution and Overrides**  
   A critical aspect of the system was ensuring that when a property is not explicitly set, it returns a sensible default value. In this case, if the last_login property is not assigned a value, it should resolve to a default value, which is None. This behavior ensures consistency in how profile data is accessed and manipulated, providing a uniform interface for interacting with profile attributes.

3. **Efficient Memory Management via Weak References**  
   To prevent memory leaks in applications where many user profiles might be loaded and discarded, the system includes a caching mechanism based on weak references. The design ensures that user profile objects are automatically removed from the cache when there are no more strong references to them. This is essential in long-running applications to maintain a low memory footprint.

4. **Extensibility and Reusability**  
   The architecture of the system was designed with future extensibility in mind. The custom descriptor that handles validation is decoupled from specific attribute names by allowing the injection of validation logic through a function. This means that the descriptor can be reused for any attribute that requires validation, not just those defined in the current project. The design adheres to the principle of separation of concerns, isolating validation logic from the business logic of user profile management.

---

## What Is Being Done

### Data Validation

The system uses a custom descriptor, called the *ValidatedProperty*, to enforce validation rules on user profile attributes. Each instance of this descriptor is created with a specific validator function that checks whether the provided value meets the required conditions. For example, the validator for the username ensures that the value is a non-empty string by verifying its type and length. Similarly, the email validator checks for the presence of certain characters such as "@" and ".", ensuring the format is acceptable for an email address.

For the last_login attribute, the system expects either a valid datetime object or a None value. This validation is crucial because it allows the system to differentiate between profiles that have been logged in and those that have not. By encapsulating the validation logic within a descriptor, the system ensures that any attempt to assign an invalid value to these properties will immediately result in a clear and informative error. This minimizes the risk of data corruption and helps maintain a consistent state across user profiles.

### Property Resolution

A significant part of the system’s design involves property resolution. When a property has not been explicitly set on an instance, the system must decide what to return when that property is accessed. In the case of the last_login attribute, if no value has been assigned, the property defaults to returning None. This behavior is achieved by the descriptor’s getter method, which checks for the existence of a stored value and returns a default if necessary. This design pattern helps in maintaining predictable behavior, so developers using the system always know what to expect when accessing an attribute.

### Caching Mechanism with Weak References

Managing memory is a common challenge in systems that handle many objects. In the UserProfileManager System, a caching mechanism is implemented to store recently used profiles. However, storing strong references to all profiles can lead to memory leaks if those profiles are not needed anymore. To overcome this, the system uses weak references—a type of reference that does not increase the reference count of an object. When an object is no longer in use elsewhere in the application, the weak reference will return None, signaling that the object has been garbage-collected.

The caching mechanism is implemented as a class-level dictionary that maps a unique identifier (derived from the object’s id) to a weak reference of the profile. When retrieving a profile from the cache, the system checks if the weak reference still points to a valid object. If the object has been removed by the garbage collector, the corresponding entry is cleaned up. This approach ensures that the cache only contains active objects and helps maintain an efficient memory footprint even as profiles are created and discarded over time.

### Implementation Details

The solution is organized around a few key components:

- **Custom Descriptor for Validation**:  
  The descriptor is the backbone of the data validation mechanism. It is responsible for intercepting all attempts to get or set the properties on a user profile. Before any value is accepted and stored, the descriptor uses the provided validator function to verify its correctness. This pattern centralizes the validation logic and makes it easy to modify or extend in the future.

- **Class-Level Caching**:  
  The cache is implemented at the class level to ensure that all instances of the UserProfileManager can be managed consistently. The use of weak references in the cache is particularly important, as it means that the system does not inadvertently prevent the garbage collection of profiles that are no longer needed. This aspect of the design is crucial for applications where a large number of profiles might be processed during the lifetime of the application.

- **Default Value Handling**:  
  By defining default behaviors for properties (e.g., returning None when last_login has not been set), the system ensures that every profile maintains a consistent interface. This consistency is key when profiles are used across different parts of an application, reducing the need for additional checks or fallback code.

- **Error Handling**:  
  When a value fails to meet its validation criteria, the system raises a ValueError with a clear message indicating which property was affected. This immediate feedback is beneficial during development and debugging, as it allows developers to quickly identify and correct issues with profile data.

---
## How It Is Being Done

The UserProfileManager system masterfully combines two of Python’s most powerful features—descriptors and weak references—to enforce data integrity and efficient memory management.

**Descriptors as Data Gatekeepers**

At its core, the system uses a custom descriptor called **ValidatedProperty** to manage attribute access. Descriptors intercept attribute assignments and accesses by implementing the `__set_name__`, `__set__`, and `__get__` methods:

- **`__set_name__`** automatically binds the attribute name to a private storage name, ensuring that the actual value is tucked away safely.
- **`__set__`** acts as a vigilant gatekeeper, running a validator function before any value is accepted. If the value fails the check (e.g., an empty username or an improperly formatted email), a clear `ValueError` is raised.
- **`__get__`** retrieves the stored value or returns a default (`None`) if the attribute hasn’t been set.

This approach centralizes and encapsulates validation logic so that every profile attribute is consistently verified.

**Weak References for a Lean Cache**

Instead of maintaining strong references that can lead to memory bloat, the system implements a class-level cache using Python’s `weakref` module. This cache maps unique object identifiers to weak references, allowing the garbage collector to reclaim memory for profiles that are no longer in active use. When a profile is requested from the cache, the system checks whether the weak reference is still alive; if not, it cleans up the dead entry. This clever design keeps the cache lightweight and responsive.

**Modular and Extensible Design**

Each validator (for username, email, and last_login) is implemented as a standalone function, making it trivial to modify or extend the validation rules without altering the descriptor itself. By isolating validation, property resolution, and caching into discrete components, the system adheres to a clean, modular architecture that is both scalable and maintainable.

**Robust Error Handling**

Clear, descriptive error messages are raised whenever a value fails validation, enabling developers to quickly diagnose and address issues. This immediate feedback loop enhances both development speed and code reliability.

**In a Nutshell**

The UserProfileManager system ensures that every user profile is valid and memory-efficient. Descriptors guarantee that data is rigorously validated and stored with predictable defaults, while the use of weak references in caching prevents memory leaks. Together, these techniques create a robust, cleanly designed foundation for managing user profiles, paving the way for future expansion with minimal hassle.
