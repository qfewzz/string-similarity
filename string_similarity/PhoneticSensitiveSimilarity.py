import re
from difflib import SequenceMatcher
import itertools

class PhoneticSensitiveSimilarity:
    
    @staticmethod
    def smith_waterman(
        seq1, seq2, match_score=3, mismatch_score=-3, gap_penalty=-2
    ):
        """
        Compute the Smith-Waterman local alignment score between two sequences.

        Args:
            seq1 (str): The first sequence.
            seq2 (str): The second sequence.
            match_score (int, optional): The score for a match. Defaults to 3.
            mismatch_score (int, optional): The score for a mismatch. Defaults to -3.
            gap_penalty (int, optional): The penalty for opening or extending a gap. Defaults to -2.

        Returns:
            int: The maximum local alignment score.
            str: The optimal local alignment for seq1.
            str: The optimal local alignment for seq2.
        """

        # Create a matrix to store alignment scores
        rows = len(seq1) + 1
        cols = len(seq2) + 1
        score_matrix = [[0 for j in range(cols)] for i in range(rows)]

        # Initialize the maximum score and the optimal alignments
        max_score = 0
        optimal_align1 = ""
        optimal_align2 = ""

        # Iterate over the sequences and fill the score matrix
        for i in range(1, rows):
            for j in range(1, cols):
                # Calculate the score for match/mismatch
                match = score_matrix[i - 1][j - 1] + (
                    match_score if seq1[i - 1] == seq2[j - 1] else mismatch_score
                )
                # Calculate the score for a gap in seq1
                delete = score_matrix[i - 1][j] + gap_penalty
                # Calculate the score for a gap in seq2
                insert = score_matrix[i][j - 1] + gap_penalty
                # Choose the maximum score
                score_matrix[i][j] = max(0, match, delete, insert)

                # Update the maximum score and optimal alignments if a better score is found
                if score_matrix[i][j] > max_score:
                    max_score = score_matrix[i][j]
                    optimal_align1 = seq1[:i]
                    optimal_align2 = seq2[:j]

        return max_score, optimal_align1, optimal_align2

    @staticmethod
    def editex(str1, str2):
        """
        Calculate the Editex distance/similarity between two strings.

        The Editex distance is a simple string similarity metric that measures
        the edit distance between two strings, while considering additional
        features specific to natural language processing tasks.

        Args:
            str1 (str): The first string to compare.
            str2 (str): The second string to compare.

        Returns:
            int: The Editex distance/similarity between the two input strings.
                A lower value indicates higher similarity between the strings.

        Notes:
            - The Editex distance is based on the Levenshtein distance, but with
                additional rules to handle specific cases in natural language
                processing.
            - These rules include:
                1. Removing consecutive duplicate characters (e.g., "aaaa" -> "a").
                2. Treating certain groups of characters as single units
                    (e.g., "ph" is treated as a single unit).
                3. Considering the difference between vowels and consonants.
            - The algorithm follows these steps:
                1. Remove consecutive duplicate characters from both strings.
                2. Convert both strings to their Editex-encoded forms.
                3. Calculate the Levenshtein distance between the encoded strings.
                4. Adjust the distance based on the difference between vowels
                    and consonants.

        Example:
            >>> editex("hello", "hallo")
            1
            >>> editex("night", "nacht")
            2
            >>> editex("language", "lenguaje")
            3
        """
        # Remove consecutive duplicate characters
        str1 = "".join(char for char, _ in itertools.groupby(str1))
        str2 = "".join(char for char, _ in itertools.groupby(str2))

        # Define vowels and consonants
        vowels = set("aeiouy")
        consonants = set("bcdfghjklmnpqrstvwxz")

        # Define Editex encoding rules
        encoding_rules = {
            "a": "0",
            "e": "0",
            "i": "0",
            "o": "0",
            "u": "0",
            "y": "0",
            "h": " ",
            "w": " ",
            "b": "1",
            "f": "1",
            "p": "1",
            "v": "1",
            "c": "2",
            "g": "2",
            "j": "2",
            "k": "2",
            "q": "2",
            "s": "2",
            "x": "2",
            "z": "2",
            "d": "3",
            "t": "3",
            "l": "4",
            "m": "5",
            "n": "5",
            "r": "6",
        }

    @staticmethod
    def encode_editex(string):
        """
        Encode a string according to the Editex rules.

        Args:
            string (str): The input string to encode.

        Returns:
            str: The Editex-encoded string.
        """
        encoded = []
        for char in string.lower():
            if char in encoding_rules:
                encoded.append(encoding_rules[char])
            else:
                encoded.append(char)
        return "".join(encoded)

        # Encode both strings using the Editex rules
        encoded_str1 = encode_editex(str1)
        encoded_str2 = encode_editex(str2)

        # Calculate the Levenshtein distance between the encoded strings
        distance = levenshtein_distance(encoded_str1, encoded_str2)

        # Adjust the distance based on the difference between vowels and consonants
        for i in range(min(len(encoded_str1), len(encoded_str2))):
        char1 = encoded_str1[i]
        char2 = encoded_str2[i]
        if char1 != char2:
            if (char1 in vowels and char2 in consonants) or (
                char1 in consonants and char2 in vowels
            ):
                distance += 1

        return distance

    @staticmethod
    def levenshtein_distance(str1, str2):
        """
        Calculate the Levenshtein distance between two strings.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.

        Returns:
            int: The Levenshtein distance between the two input strings.
        """
        m = len(str1)
        n = len(str2)

        # Create a distance matrix
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Initialize the first row and column
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j

        # Fill in the rest of the matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                deletion = dp[i - 1][j] + 1
                insertion = dp[i][j - 1] + 1
                substitution = dp[i - 1][j - 1]
                if str1[i - 1] != str2[j - 1]:
                    substitution += 1
                dp[i][j] = min(deletion, insertion, substitution)

        return dp[m][n]

    @staticmethod
    def count_syllables(word):
        """
        Count the number of syllables in a given word.

        This function uses a simple heuristic based on the number of vowel groups
        in the word to estimate the number of syllables.

        Args:
            word (str): The word to count syllables for.

        Returns:
            int: The estimated number of syllables in the word.
        """
        vowels = "aeiouy"
        count = 0
        prev_char_vowel = False
        
        for char in word.lower():
            is_vowel = char in vowels
            if is_vowel and not prev_char_vowel:
                count += 1
            prev_char_vowel = is_vowel
        
        # Add 1 if the word ends with 'e'
        if word.endswith('e'):
            count += 1
        
        # Ensure at least one syllable per word
        if count == 0:
            count = 1
        
        return count
   
    @staticmethod
    def syllable_alignment_distance(string1, string2):
        """
        Calculate the Syllable Alignment distance/similarity between two given strings.

        The Syllable Alignment distance is a measure of the similarity between two strings
        based on the number of syllables in each string and the alignment of those syllables.
        It is particularly useful for comparing names or words where the syllable structure
        is more important than the individual characters.

        Args:
            string1 (str): The first string to compare.
            string2 (str): The second string to compare.

        Returns:
            float: The Syllable Alignment distance/similarity between the two strings,
                    ranging from 0 (completely different) to 1 (identical).

        Example:
            >>> syllable_alignment_distance("Katherine", "Katarina")
            0.8
            >>> syllable_alignment_distance("John", "Jonathan")
            0.6
            >>> syllable_alignment_distance("Michael", "Michelle")
            0.4
        """
   

        # Tokenize the input strings into syllables
        syllables1 = [char for char in string1.lower() if char.isalpha()]
        syllables2 = [char for char in string2.lower() if char.isalpha()]

        # Calculate the number of syllables in each string
        num_syllables1 = PhoneticSensitiveSimilarity.count_syllables(string1)
        num_syllables2 = PhoneticSensitiveSimilarity.count_syllables(string2)

        # Initialize the distance matrix
        distance_matrix = [[0] * (num_syllables2 + 1) for _ in range(num_syllables1 + 1)]

        # Fill the distance matrix using dynamic programming
        for i in range(num_syllables1 + 1):
            distance_matrix[i][0] = i
        for j in range(num_syllables2 + 1):
            distance_matrix[0][j] = j

        for i in range(1, num_syllables1 + 1):
            for j in range(1, num_syllables2 + 1):
                if syllables1[i - 1] == syllables2[j - 1]:
                    distance_matrix[i][j] = distance_matrix[i - 1][j - 1]
                else:
                    distance_matrix[i][j] = min(distance_matrix[i - 1][j], distance_matrix[i][j - 1], distance_matrix[i - 1][j - 1]) + 1

        # Calculate the Syllable Alignment distance/similarity
        max_syllables = max(num_syllables1, num_syllables2)
        alignment_distance = distance_matrix[num_syllables1][num_syllables2]
        alignment_similarity = 1 - (alignment_distance / max_syllables)

        return alignment_distance