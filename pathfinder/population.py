"""
# population.py - CS481-GA-PATHFINDER
# Martin Miglio
#
# This file handles the genetic algorithm,
#   running a trial, calling for breeding,
#   and repeating.
"""

import random

from graphics import Point, Text

from pathfinder.finder import Finder


class Population:

    def __init__(self, size, lifespan, start_position, window):
        """Population constructor

        Args:
            size (int): number of finders in population
            lifespan (int): number of steps in each finder
            start_position (Vector): a vector describing the start position
            window (GraphWin): a window to add the population to
        """
        self.size = size
        self.finders = []
        # make the inital finders with random stats
        for _ in range(size):
            self.finders.append(
                Finder(lifespan=lifespan, start_position=start_position))
        # create a readout of fitness
        self.fitness_readout = Text(Point(250, 520), "")
        self.fitness_readout.draw(window)

    def run(self, window, environment):
        """A function to run the population

        Args:
            window (GraphWin): a window to run the population in
            environment (Environment): an Environment to run the population in
        """
        alive_count = 0
        for finder in self.finders:
            finder.update(window, environment)
            if not (finder.crashed or finder.completed):
                alive_count += 1
        if alive_count == 0:  # if no finders are alive, step the population
            self.step(environment)

    def step(self, environment):
        """A function to step from one population to the next

        Args:
            environment (Environment): the Environment the population
                was ran in
        """
        # sort finders on fitness
        sorted_finders = sorted(
            self.finders,
            key=lambda finder: finder.calculate_fitness(environment),
            reverse=True
        )
        average_fitness = sum(
            finder.fitness for finder in self.finders)/len(self.finders)
        self.fitness_readout.setText(
            f"Last round's average fitness: {average_fitness}")
        # where to split the population
        cutoff = self.size / 2 if self.size % 2 == 0 else (self.size + 1) / 2
        # the lucky finders who will continue on
        mating_pool = sorted_finders[0:int(cutoff) + 1]
        new_finders = []
        for _ in range(self.size):
            first_parent = random.choice(mating_pool)
            second_parent = random.choice(mating_pool)
            new_finders.append(first_parent.get_child(second_parent))
        # apply the new finders, ensuring there is the proper amount
        self.finders = new_finders[0:self.size]
