
from __future__ import print_function
from random import choice, seed

import bundler

class AutFn():
    ''' This stores a collection of automorphisms of a free group F_n. When S is a punctured
    surface then \pi_1(S) is a free group and MCG(S) acts on \pi_1(S) by automorphisms.
    
    If S isn't punctured then \pi_1(S) isn't free and canonical may not produce a canonical
    representative, however:
        1) It 'rarely' fails to produce the canonical representative for a word.
        2) generate_FSM_info below doesn't actually require canonical representatives for every word.
            only that v & w have same canonical representative => v ~ w. Which this does.
        3) The performance gain is huge. '''
    
    def __init__(self, generators, twists=None):
        self.generators = generators
        self.trivial_relations = [generator + self.inverse(generator) for generator in generators]
        self.inverse_letters = dict(zip(generators, map(self.inverse, generators)))
        self.ordering = bundler.ShortLex(generators)
        self.actions = dict()
        
        if twists is not None:
            for curve in twists:
                self.add_action(curve, twists[curve])
    
    def canonical(self, w):
        w = self.cyclic_free_reduce(w)
        return self.ordering.cyclic_first_permutation(w, self.inverse(w))
    
    def add_action(self, Action_name, Action):
        ''' Adds an action on this group to the groups action database. '''
        # Create a dictionary with default values.
        d = dict(zip(self.generators, self.generators))
        
        for letter in Action:
            d[letter] = self.free_reduce(Action[letter])
            d[self.inverse(letter)] = self.free_reduce(self.inverse(Action[letter]))
        
        self.actions[Action_name] = d
    
    def cyclic_free_reduce(self, word):
        word = self.free_reduce(word)  # We assume that the word is already free reduced.
        len_word = len(word)
        for i in range(len_word):
            if word[i] != self.inverse_letters[word[len_word-i-1]]:
                return word[i:len_word-i]
        
        return ''
    
    def inverse(self, word):
        return word[::-1].swapcase()
    
    def free_reduce(self, word):
        loop = True
        while loop:
            loop = False
            for i in self.trivial_relations:
                if i in word:
                    word = word.replace(i, '')
                    loop = True
        
        return word
    
    def apply_to(self, action_name, w):
        ''' Applies an action to the loop w. '''
        action = self.actions[action_name]
        return self.free_reduce(''.join([action[letter] for letter in w]))

