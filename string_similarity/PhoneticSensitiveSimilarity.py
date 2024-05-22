import re
from difflib import SequenceMatcher


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
    def editex(s1, s2):
        """
        Calculate the Editex distance between two strings.

        The Editex distance is a string metric that measures the edit distance between two strings,
        with a special emphasis on preserving the consonant patterns. It is useful for identifying
        similar names or words, especially in situations where spelling errors or variations are common.

        Args:
            s1 (str): The first string.
            s2 (str): The second string.

        Returns:
            int: The Editex distance between the two strings.

        Example:
            >>> editex("hello", "hello")
            0
            >>> editex("hello", "hellp")
            1
            >>> editex("hello", "world")
            5
        """

        # Convert strings to uppercase and remove spaces
        s1 = ''.join(c for c in s1.upper() if c.isalnum())
        s2 = ''.join(c for c in s2.upper() if c.isalnum())

        # Initialize the edit distance
        edit_distance = 0

        # Iterate over the strings
        while s1 and s2:
            # Check if the first characters are the same
            if s1[0] == s2[0]:
                s1 = s1[1:]
                s2 = s2[1:]
            else:
                # If they are different, check if they are consonants
                is_s1_consonant = s1[0] not in 'AEIOU'
                is_s2_consonant = s2[0] not in 'AEIOU'

                if is_s1_consonant and is_s2_consonant:
                    # If both are consonants, replace the first character of s1 by the first character of s2
                    s1 = s2[0] + s1[1:]
                    edit_distance += 1
                else:
                    # If one is a consonant and the other is a vowel, remove the vowel
                    if is_s1_consonant:
                        s1 = s1[1:]
                    else:
                        s2 = s2[1:]
                    edit_distance += 1

        # Add the remaining characters from the longer string
        edit_distance += len(s1) + len(s2)

        return edit_distance

    @staticmethod
    def __syllable_count(word):
        """
        Count the number of syllables in a word.

        Parameters:
        word (str): The word to count syllables in.

        Returns:
        int: The number of syllables in the word.
        """
        # Define a regex pattern for vowels
        vowels = "aeiouy"
        word = word.lower().strip()
        count = 0
        prev_char_was_vowel = False

        # Iterate over characters in the word
        for char in word:
            if char in vowels:
                if not prev_char_was_vowel:
                    count += 1
                    prev_char_was_vowel = True
            else:
                prev_char_was_vowel = False

        # Handle silent 'e' at the end
        if word.endswith("e"):
            if count > 1 and not word[-2] in vowels:
                count -= 1

        return count

    @staticmethod
    def __get_syllables(word):
        """
        Break a word into its syllables.

        Parameters:
        word (str): The word to break into syllables.

        Returns:
        list: A list of syllables.
        """
        # A simple regex-based syllable splitting
        syllables = re.findall(
            r'[^aeiouy]*[aeiouy]+(?:[^aeiouy]*$|[^aeiouy](?=[^aeiouy]))?',
            word.lower(),
        )
        return syllables

    @staticmethod
    def syllable_alignment_distance(str1, str2):
        """
        Calculate the Syllable Alignment distance/similarity between two strings.

        Parameters:
        str1 (str): The first string.
        str2 (str): The second string.

        Returns:
        float: The similarity ratio between the two strings based on syllable alignment.
        """
        # Get syllables for both strings
        syllables1 = (
            PhoneticSensitiveSimilarity.__get_syllables(str1)
        )
        syllables2 = (
            PhoneticSensitiveSimilarity.__get_syllables(str2)
        )

        # Use SequenceMatcher to find the similarity ratio
        matcher = SequenceMatcher(None, syllables1, syllables2)
        similarity_ratio = matcher.ratio()

        return similarity_ratio

