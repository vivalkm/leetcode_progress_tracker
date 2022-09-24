
# leetcode_progress_tracker
This tool is used to track your daily efforts on LeetCode. It will show how many questions are solved by date and by difficulty.

## 0. Authors
[Lincoln Li](https://github.com/vivalkm)

## 1. Basic Use
1. Download the repo or clone it using: `git clone https://github.com/vivalkm/leetcode_progress_tracker.git`
2. Run: `python3 main.py` This will count your solved questions by difficulty in last 10 days by default.
3. For the first time running, the tracker will ask for your csrftoken & LEETCODE_SESSION cookie which can be found by following steps:
   
   a. Log into LeetCode using your browser as you would normally do.
   
   b. Get your csrftoken & LEETCODE_SESSION using the browser inspection tools
   ![image](https://user-images.githubusercontent.com/83200994/135570856-6b61d9dc-88a8-417b-8b28-1d67ece4205c.png)
4. Sample Output

   ![image](https://user-images.githubusercontent.com/83200994/192086326-5fb64574-06d8-477e-baa6-b6db10c17e27.png)

## 2. CLI
1. Count all solved questions by date for your session: `python3 tracker_cli.py -a`
2. Count solved questions in last n recent days: `python3 tracker_cli.py -n`
