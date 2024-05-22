class TokenBasedStringSimilarity:
    @staticmethod
    def qgram_similarity(str1, str2, q=2):
        """
        Calculate the q-gram similarity between two strings.

        Args:
            str1 (str): The first string to compare.
            str2 (str): The second string to compare.
            q (int): The length of each q-gram.

        Returns:
            float: The q-gram similarity as a ratio of the number of common q-grams
                to the maximum number of q-grams in either string.
        """
        # Generate the set of q-grams for the first string
        set1 = set([str1[i : i + q] for i in range(len(str1) - q + 1)])

        # Generate the set of q-grams for the second string
        set2 = set([str2[i : i + q] for i in range(len(str2) - q + 1)])

        # Find the intersection of the two sets of q-grams
        common_qgrams = set1.intersection(set2)

        # Calculate the q-gram similarity
        return len(common_qgrams) / float(max(len(set1), len(set2)))

    @staticmethod
    def overlap_coefficient(str1, str2):
        """
        Calculates the overlap coefficient between two strings.

        The overlap coefficient is a similarity measure that quantifies the degree of
        overlap between two sets of strings. It is calculated as the ratio of the
        length of the longest common substring to the length of the shorter string.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.

        Returns:
            float: The overlap coefficient between the two input strings.
        """
        # Find the length of the longest common substring
        m, n = len(str1), len(str2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        max_len = 0
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if str1[i - 1] == str2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    max_len = max(max_len, dp[i][j])

        # Calculate the overlap coefficient
        min_len = min(m, n)
        if min_len == 0:
            return 0.0
        else:
            return max_len / min_len

    @staticmethod
    def jaccard_similarity(str1, str2):
        """
        Calculate the Jaccard similarity between two strings.

        The Jaccard similarity is a measure of similarity between two sets.
        It is defined as the size of the intersection of the two sets
        divided by the size of the union of the two sets.

        In this implementation, the strings are first converted to sets
        of unique characters (case-insensitive), and then the Jaccard
        similarity is calculated using these sets.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.

        Returns:
            float: The Jaccard similarity between the two strings,
            ranging from 0 (completely different) to 1 (identical).

        Example:
            >>> jaccard_similarity('apple', 'appeal')
            0.6666666666666666
            >>> jaccard_similarity('hello', 'world')
            0.0
            >>> jaccard_similarity('python', 'python')
            1.0
        """
        # Convert strings to lowercase and convert to sets
        set1 = set(str1.lower())
        set2 = set(str2.lower())

        # Calculate the intersection and union of the sets
        intersection = set1.intersection(set2)
        union = set1.union(set2)

        # Calculate the Jaccard similarity
        if len(union) == 0:
            return 0.0
        else:
            return len(intersection) / len(union)

    @staticmethod
    def dice_coefficient(str1, str2):
        """
        Calculates the Dice Coefficient between two strings.

        The Dice Coefficient is a measure of similarity between two strings, and is
        calculated as twice the number of common bigrams divided by the total number
        of bigrams in both strings.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.

        Returns:
            float: The Dice Coefficient between the two strings, ranging from 0 to 1,
            where 1 indicates identical strings.

        """
        # Convert strings to lowercase and remove leading/trailing whitespace
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()

        # Create a set of bigrams for each string
        bigrams1 = set([str1[i : i + 2] for i in range(len(str1) - 1)])
        bigrams2 = set([str2[i : i + 2] for i in range(len(str2) - 1)])

        # Calculate the intersection and union of the bigram sets
        intersection = bigrams1.intersection(bigrams2)
        union = bigrams1.union(bigrams2)

        # If both strings are empty, return 1
        if len(union) == 0:
            return 1.0

        # Calculate the Dice Coefficient
        dice_coeff = 2 * len(intersection) / len(union)

        return dice_coeff

    @staticmethod
    def bag_distance(str1, str2):
        """
        Calculate the bag distance between two strings.

        The bag distance between two strings is defined as the sum of the
        absolute differences in the frequencies of each character in the strings.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.

        Returns:
            int: The bag distance between the two strings.

        Example:
            >>> bag_distance("hello", "world")
            9
            >>> bag_distance("python", "java")
            4
        """
        # Create dictionary to store character frequencies
        freq1 = {}
        freq2 = {}

        # Count character frequencies in each string
        for char in str1:
            freq1[char] = freq1.get(char, 0) + 1
        for char in str2:
            freq2[char] = freq2.get(char, 0) + 1

        # Calculate bag distance
        distance = 0
        for char in set(freq1.keys()).union(set(freq2.keys())):
            distance += abs(freq1.get(char, 0) - freq2.get(char, 0))

        return distance
