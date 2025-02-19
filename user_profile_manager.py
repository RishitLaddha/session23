from datetime import datetime
import weakref

# A descriptor that validates a property value using a provided validator function.
class ValidatedProperty:
    def __init__(self, validator):
        # Store the validator function that checks if the value is valid.
        self.validator = validator

    def __set_name__(self, owner, name):
        """
        Called automatically when the owning class is created.
        Binds the attribute name to the descriptor so that we can store
        the value in an instance-specific private attribute.
        """
        self.name = name
        # We use a private name to avoid conflicts in the instance's __dict__.
        self.private_name = "_" + name

    def __get__(self, instance, owner):
        """
        When the attribute is accessed:
          - If accessed from the class (instance is None), return the descriptor itself.
          - If accessed from an instance, return the stored value or None if not set.
        """
        if instance is None:
            return self
        # Use getattr with a default of None if the attribute was never set.
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        """
        When a value is assigned to the property:
          - Validate the value using the provided validator function.
          - Raise a ValueError if validation fails.
          - Otherwise, store the value in the instance using a private attribute.
        """
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}")
        # Store the validated value in the instance's __dict__ using the private name.
        setattr(instance, self.private_name, value)

# Validator function to ensure a string is non-empty.
def non_empty_string(value):
    # Check if value is a string and is not empty (after stripping whitespace).
    return isinstance(value, str) and len(value.strip()) > 0

# Validator function to ensure a valid email.
def valid_email(value):
    # Check if value is a string and contains both "@" and "." characters.
    return isinstance(value, str) and ("@" in value) and ("." in value)

# Validator function for last_login.
def valid_last_login(value):
    # Allow the value to be None or a datetime instance.
    return value is None or isinstance(value, datetime)

# The UserProfileManager class represents a user profile with three attributes:
# - username, email, and last_login.
# Each attribute is managed by a ValidatedProperty descriptor that enforces the validation rules.
class UserProfileManager:
    username = ValidatedProperty(non_empty_string)
    email = ValidatedProperty(valid_email)
    last_login = ValidatedProperty(valid_last_login)  # Default value is None if not set

    # Class-level cache to hold weak references to profiles.
    _cache = {}

    @classmethod
    def add_to_cache(cls, profile):
        """
        Add a profile to the cache.
        We store a weak reference to avoid memory leaks—if no strong reference
        to the profile exists, it can be garbage-collected.
        """
        cls._cache[id(profile)] = weakref.ref(profile)

    @classmethod
    def get_from_cache(cls, uid):
        """
        Retrieve a profile from the cache by its unique id.
        If the profile is no longer strongly referenced, remove its weak reference.
        """
        ref = cls._cache.get(uid)
        if ref is None:
            return None
        obj = ref()  # Call the weak reference to get the actual object
        if obj is None:
            # If the object was garbage-collected, remove the dead weak reference.
            del cls._cache[uid]
        return obj
