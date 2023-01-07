def get_levenstein_distance(a: str, b: str):
    ''' Get distance to transform text `a` to `b` '''
    n = len(a)
    m = len(b)
    # to optimize memory we only use 2 layer of dp instead of (n + 1)
    dp = [[0] * (m + 1) for i in range(0, 2)]
    
    for j in range(1, m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        dp[i % 2][0] = i
        for j in range(1, m + 1):
            dp[i % 2][j] = min(
                dp[i % 2][j - 1] + 1,
                dp[(i - 1) % 2][j] + 1,
                dp[(i - 1) % 2][j - 1] + (a[i - 1] != b[j - 1])
            )
    
    return dp[n % 2][m]

def get_levenstein_distance_normalized(a: str, b: str):
    ''' Get distance to transform text `a` to `b` divided by the length of text `a` '''
    if (len(a) == 0 and len(b) == 0):
        return 1.0

    return get_levenstein_distance(a, b) / max(len(a), len(b))
