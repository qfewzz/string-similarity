class CharacterBasedStringSimilarity:
    @staticmethod
    def hamming_distance(str1, str2):
        """
        Calculate the Hamming distance between two strings of equal length.

        The Hamming distance is the number of positions at which the corresponding
        characters in the two strings are different.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.

        Returns:
            int: The Hamming distance between the two strings.

        Raises:
            ValueError: If the input strings have different lengths.
        """
        # Check if the strings have equal lengths
        if len(str1) != len(str2):
            raise ValueError(
                "Hamming distance is defined only for strings of equal length."
            )

        # Initialize the distance counter
        distance = 0

        # Iterate over the characters of the strings simultaneously
        for char1, char2 in zip(str1, str2):
            # If the characters are different, increment the distance
            if char1 != char2:
                distance += 1

        # Return the final Hamming distance
        return distance

    @staticmethod
    def levenshtein_distance(str1, str2):
        """
        Compute the Levenshtein distance between two strings.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.

        Returns:
            int: The Levenshtein distance between the two input strings.
        """
        m, n = len(str1), len(str2)

        # Initialize a matrix to store the costs of transforming a prefix of str1 to a prefix of str2
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Fill in the matrix with costs
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:  # If str1 is empty, cost is equal to the length of str2
                    dp[i][j] = j
                elif (
                    j == 0
                ):  # If str2 is empty, cost is equal to the length of str1
                    dp[i][j] = i
                else:
                    # Cost of transforming str1[:i] to str2[:j] is the minimum of:
                    # 1. Cost of transforming str1[:i-1] to str2[:j] + 1 (deletion)
                    # 2. Cost of transforming str1[:i] to str2[:j-1] + 1 (insertion)
                    # 3. Cost of transforming str1[:i-1] to str2[:j-1] + 1 (if str1[i-1] != str2[j-1]) or 0 (if str1[i-1] == str2[j-1])
                    dp[i][j] = min(
                        dp[i - 1][j] + 1,  # Deletion
                        dp[i][j - 1] + 1,  # Insertion
                        dp[i - 1][j - 1]
                        + (0 if str1[i - 1] == str2[j - 1] else 1),  # Substitution
                    )

        # Return the Levenshtein distance between the two input strings
        return dp[m][n]

    @staticmethod
    def damerau_levenshtein_distance(str1, str2):
        """
        Calculate the Damerau-Levenshtein distance between two strings.

        The Damerau-Levenshtein distance is a string metric that measures the edit distance between two strings.
        It is an extension of the Levenshtein distance which also accounts for transpositions of adjacent characters.

        Args:
            str1 (str): The first string.
            str2 (str): The second string.

        Returns:
            int: The Damerau-Levenshtein distance between the two strings.
        """
        m, n = len(str1), len(str2)

        # Initialize a matrix to store costs
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Fill in the matrix with costs
        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    dp[i][
                        j
                    ] = j  # If the first string is empty, the cost is the length of the second string
                elif j == 0:
                    dp[i][
                        j
                    ] = i  # If the second string is empty, the cost is the length of the first string
                else:
                    dp[i][j] = min(
                        dp[i - 1][j]
                        + 1,  # Deletion: Remove a character from the first string
                        dp[i][j - 1]
                        + 1,  # Insertion: Add a character to the first string
                        dp[i - 1][j - 1]
                        + (
                            0 if str1[i - 1] == str2[j - 1] else 1
                        ),  # Substitution: Replace a character in the first string
                    )

                    # Check for transposition (adjacent characters are swapped)
                    if (
                        i > 1
                        and j > 1
                        and str1[i - 1] == str2[j - 2]
                        and str1[i - 2] == str2[j - 1]
                    ):
                        dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)

        # Return the Damerau-Levenshtein distance
        return dp[m][n]

    @staticmethod
    def jaro_distance(str1, str2):
        """
        Calculate the Jaro distance between two strings.

        The Jaro distance is a measure of similarity between two strings.
        The higher the Jaro distance for two strings is, the more similar
        the strings are. The distance is a value between 0 and 1.

        Args:
            str1 (str): The first string to compare.
            str2 (str): The second string to compare.

        Returns:
            float: The Jaro distance between str1 and str2.
        """

        # Calculate the length of the strings
        len_str1, len_str2 = len(str1), len(str2)

        # Set the matching distance (up to which characters are considered matching)
        match_distance = max(len_str1, len_str2) // 2 - 1

        # Initialize arrays to store matching characters
        matches_str1 = [False] * len_str1
        matches_str2 = [False] * len_str2

        # Count the number of matching characters
        match_count = 0
        for i in range(len_str1):
            start = max(0, i - match_distance)
            end = min(i + match_distance + 1, len_str2)
            for j in range(start, end):
                if not matches_str2[j] and str1[i] == str2[j]:
                    matches_str1[i] = True
                    matches_str2[j] = True
                    match_count += 1
                    break

        # If no characters match, return 0.0 as similarity
        if match_count == 0:
            return 0.0

        # Count the number of transpositions
        transpositions = 0
        k = 0
        for i in range(len_str1):
            if matches_str1[i]:
                while not matches_str2[k]:
                    k += 1
                if str1[i] != str2[k]:
                    transpositions += 1
                k += 1

        # Each transposition is counted twice, so halve the count
        transpositions //= 2

        # Calculate the Jaro similarity
        jaro_similarity = (
            (match_count / len_str1)
            + (match_count / len_str2)
            + ((match_count - transpositions) / match_count)
        ) / 3

        return jaro_similarity

    @staticmethod
    def jaro_winkler_distance(str1, str2, p=0.1):
        """
        Calculate the Jaro-Winkler distance between two strings.

        Parameters:
        str1 (str): The first string to compare.
        str2 (str): The second string to compare.
        p (float): The scaling factor for the common prefix length (default is 0.1).

        Returns:
        float: The Jaro-Winkler distance between the two strings.
        """
        jaro_dist = (
            CharacterBasedStringSimilarity.jaro_distance(
                str1, str2
            )
        )  # Compute the Jaro distance between the strings

        # Calculate the length of the common prefix
        common_prefix_len = 0
        for char1, char2 in zip(str1, str2):
            if char1 == char2:
                common_prefix_len += 1
            else:
                break

        # Calculate the Jaro-Winkler distance
        jaro_winkler_dist = jaro_dist + p * common_prefix_len * (1 - jaro_dist)
        return jaro_winkler_dist
