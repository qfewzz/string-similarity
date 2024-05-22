class SequenceBasedStringSimilarity:
    @staticmethod
    def lcs(X, Y):
        """
        Computes the length of the longest common subsequence between two strings X and Y.
        
        Args:
            X (str): The first string.
            Y (str): The second string.
            
        Returns:
            int: The length of the longest common subsequence between X and Y.
        """
        # Determine the lengths of the input strings
        m, n = len(X), len(Y)
        
        # Create a 2D array (list of lists) to store the lengths of LCS of substrings
        # dp[i][j] will hold the length of LCS of X[0..i-1] and Y[0..j-1]
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Fill the dp table in a bottom-up manner
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # If the characters match, the LCS length at this point is 1 plus the LCS length
                # of the substrings without the last characters
                if X[i - 1] == Y[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                # If the characters do not match, take the maximum LCS length of the subproblems
                # without the current character of either string
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        # The value at dp[m][n] contains the length of LCS of X[0..m-1] and Y[0..n-1]
        return dp[m][n]

    
    @staticmethod
    def longest_common_substring(X, Y):
        """
        Find the longest common substring between two strings X and Y.

        Args:
            X (str): The first string.
            Y (str): The second string.

        Returns:
            str: The longest common substring between X and Y.
        """
        # Get the lengths of the input strings
        m, n = len(X), len(Y)
        
        # Initialize a 2D list (dp table) with dimensions (m+1) x (n+1) filled with zeros
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        # Variables to keep track of the maximum length of common substring found
        max_len = 0
        
        # Variables to keep track of the ending indices of the longest common substring in X and Y
        max_i, max_j = 0, 0

        # Fill the dp table in a bottom-up manner
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Check if characters at current position in both strings are the same
                if X[i - 1] == Y[j - 1]:
                    # If they are the same, update the dp table
                    dp[i][j] = dp[i - 1][j - 1] + 1
                    
                    # Check if this is the longest common substring found so far
                    if dp[i][j] > max_len:
                        # Update the maximum length and the ending indices
                        max_len = dp[i][j]
                        max_i, max_j = i, j

        # Initialize an empty string to store the longest common substring
        lcs = ''
        
        # Construct the longest common substring using the dp table
        while max_len > 0:
            # Append the current character to the result
            lcs = X[max_i - 1] + lcs
            
            # Move to the previous characters in both strings
            max_i, max_j, max_len = max_i - 1, max_j - 1, max_len - 1

        # Return the longest common substring
        return lcs
