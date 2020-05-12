from random import randint

class Animatable:
    """ Defines a value which incrementally animates to a target value."""
    # Is it currently animating
    is_animating = False

    # Current value
    current = 0

    # The target value
    target = 0

    # The duration of the animation
    duration = 0

    # The increment, per millisecond
    inc = 0

    # A label used for debugging
    label = None

    def __init__(self, current, target, duration, label=None):
        self.current = current
        self.target = target
        self.duration = duration
        self.label = label
        self.define_inc()


    def change(self, target=None, duration=None):
        """ Change the animation to a new target and/or duration. """
        if target is not None:
            self.target = target
        if duration is not None:
            self.duration = duration
        self.define_inc()


    def define_inc(self):
        """Define the animation increment."""
        if self.duration >= 0:
            self.inc = (self.target - self.current) / self.duration
            self.is_animating = True
        else:
            self.duration = 0
            self.inc = 0
            self.is_animating = False


    def update(self, elapsed_ms):
        """Animate the current value towards the target.
        :param elasped_ms: The number of milliseconds since the last update.
        :return: If we're still animating
        """
        if not self.is_animating:
            return False
        if self.current == self.target or self.inc == 0:
            return False

        # Update current
        self.duration -= elapsed_ms
        self.current += self.inc * elapsed_ms

        # Animation complete
        if (
            self.duration <= 0
            or (self.inc > 0 and self.current >= self.target)
            or (self.inc < 0 and self.current <= self.target)
        ):
            self.inc = 0
            self.current = self.target
            self.is_animating = False

        return self.is_animating


    def __repr__(self):
        label = self.label if self.label else ''
        return f"Animatable:{label} (current={self.current}, target={self.target}, inc={self.inc}, duration={self.duration})"


class LivingAnimation(Animatable):
    """ An animation which chooses random values, within defined boundary ranges, to animate to.
    When the animation completes, new values are automatically chosen.
    """

    # The min/max milliseconds for the animation
    duration_range = None

    # The absolute min/max boundary for the value
    value_range = None

    # Move the value relatively min/max to the current value
    # Set to None to not animate relatively
    relative_range = None

    def __init__(self, initial_value, value_range, duration_range, relative_range=None, label=None):
        self.current = initial_value
        self.duration_range = duration_range
        self.value_range = value_range
        self.relative_range = relative_range
        self.create_target_values()
        super().__init__(self.current, self.target, self.duration, label=label)

    def rand_range(self, range_dict):
        """Pick a random number between the min/max value of a range dict."""
        min_val = round(range_dict['min'])
        max_val = round(range_dict['max'])
        return randint(min_val, max_val)

    def create_target_values(self):
        """ Create a new animation target values, randomly chosen from the boundary ranges. """
        self.duration = self.rand_range(self.duration_range)

        if self.relative_range is not None:
            relative = self.rand_range(self.relative_range)

            # Move away from the boundaries, if we're close.
            # Use 25% of the max value to determine the margin
            margin = self.relative_range['max'] / 4
            if self.current + margin >= self.value_range['max']:
                relative *= -1
            # If we're not close to a boundary, determine direction randomly
            elif self.current - margin >= self.value_range['min']:
                neg = randint(0, 1)
                if neg == 1:
                    relative *= -1

            # Set relative target within min/max values
            target = self.current + relative
            if target < self.value_range['min']:
                target = self.value_range['min']
            elif target > self.value_range['max']:
                target = self.value_range['max']
            self.target = target
        else:
            self.target = self.rand_range(self.value_range)

    def update(self, elapsed_ms):
        """Update the current value. When the animation is complete, automatically choose new target values."""
        super().update(elapsed_ms)

        if not self.is_animating:
            self.create_target_values()
            self.change(self.target, self.duration)
            # print(f"New: {self}")

        return True



