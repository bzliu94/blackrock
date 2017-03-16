/*

2017-03-16

problem #8 - perfect separating

inspired by sgtlaugh

complement - subsequence containing elements 
that weren't included in reference subsequence 
w.r.t. original sequence s

perfect - subsequence used to index into original sequence s 
s.t. complement subsequence used to index into s matches

find number of perfect sequences w.r.t. s

brute force - find all subsequences of sequence s, find complement for each, then index into s and tell if the two result subsequences match; note that for a sequence to be perfect w.r.t. s, the first subsequence must be length one-half that of s; that is, s must be of even length to have perfect sequences associated with it

for a subsequence to be perfect, post-indexing subsequence must e.g. have number of a's (or b's) that matches that for complement post-indexing subsequence and that is therefore even

(n / 2) C x is maximized by taking x to be n / 4

running time is O((n / 2) C (n / 4) * n)

*/

import java.util.ArrayList;
import java.lang.Exception;
import java.lang.Integer;
import java.lang.Math;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStream;
import java.lang.String;

public class Solution {
	
	/*
	i is position along s for eating up s
	"pattern" is post-indexing subsequence associated with a perfect x-y pair
	j is number of characters consumed for left (x)
	k is number of characters consumed for right (y)
	*/
	public static long count(ArrayList<String> s, long[][] dp, 
			int[] visited, char[] pattern, int n, int m, 
			int i, int j, int k) {
		// if we consumed s, j and k must be half length of s; return one
		if (i == n) {
			return (j == m && k == m) ? 1 : 0;
		}
		// save repeated work between different branches by memoizing on basis of j and k
		if (j < m && k < m && ((visited[j] & (1 << k)) != 0)) {
			return dp[j][k];
		}
		long result = 0;
		// this case is only valid if x is not totally consumed yet
		if (j < m && pattern[j] == s.get(i).charAt(0)) {
			result += Solution.count(s, dp, visited, pattern, n, m, i + 1, j + 1, k);
		}
		// this case is only valid if y is not totally consumed yet
		if (k < m && pattern[k] == s.get(i).charAt(0)) {
			result += Solution.count(s, dp, visited, pattern, n, m, i + 1, j, k + 1);
		}
		// have airlock; only after we finalize this cell do we set visited flag to be one
		if (j < m) {
			visited[j] |= 1 << k;
		}
		// memoize and return composite count
		if (j < m && k < m) {
			dp[j][k] = result;
		}
		return result;
	}
	
	public static int countStr(ArrayList<String> list, String str) {
		int count = 0;
		for (int i = 0; i < list.size(); i++) {
			if (list.get(i).equals(str) == true) {
				count += 1;
			}
		}
		return count;
	}
	
	public static long getNumPerfectSubsequences(String s, int n) {
		ArrayList<String> s_list = new ArrayList<String>(n);
		for (char c : s.toCharArray()) {
			String curr_str = Character.toString(c);
			s_list.add(curr_str);
		}
		// count a's and b's
		int a = Solution.countStr(s_list, "a");
		int b = Solution.countStr(s_list, "b");
		// "result" is number of perfect subsequences w.r.t. s
		long result = 0;
		// check that n, a, b are even
		if (((n % 2 == 0) && (a % 2 == 0) && (b % 2 == 0)) == false) {
			return result;
		}
		// m is half n, get largest binary value with m bits
		int m = n / 2;
		long largest_mask = (1 << m) - 1;
		long[][] dp = new long[m][m];
		for (int i = 0; i < m; i++) {
			for (int j = 0; j < m; j++) {
			dp[i][j] = 0;
			}
		}
		int[] visited = new int[m];
		for (int i = 0; i < m; i++) {
			visited[i] = 0;
		}
		char[] pattern = new char[n];
		for (int i = 0; i < n; i++) {
			pattern[i] = 'a';
		}
		for (int mask = 0; mask <= largest_mask; mask++) {
			// check that number of a's is half what it could be
			if (Integer.bitCount(mask) == (a >> 1)) {
				for (int i = 0; i < m; i++) {
					if ((mask & (1 << i)) != 0) {
						// if we see a one at a particular offset, we have an 'a'
						pattern[i] = 'a';
					} else {
						// if we don't, we have a 'b'
						pattern[i] = 'b';
					}
				}
				// reset "visited" binary flags
				for (int i = 0; i < m; i++) {
					visited[i] = 0;
				}
				result += Solution.count(s_list, dp, visited, pattern, n, m, 0, 0, 0);
			}
		}
		return result;
	}

	public static void main(String args[]) throws Exception {
		InputStream in = System.in;
		// InputStream in = new FileInputStream("/home/brianl/blackrock/8 - perfect separating/tests/official/input32.txt");
		InputStreamReader stream_reader = new InputStreamReader(in);
		BufferedReader br = new BufferedReader(stream_reader);
		String line = br.readLine();
		line = line.trim();
		String[] curr_args = line.split(" ");
		String s = curr_args[0];
		// System.out.println(s);
		int n = s.length();
		long result = Solution.getNumPerfectSubsequences(s, n);
		System.out.println(result);
	}

}


