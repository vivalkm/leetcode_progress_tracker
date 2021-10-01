import os
cookie_pair = {}

def init_env():
    # Initialize csrftoken and LEETCODE_SESSION if not exist
    if not os.path.isfile('cookie') or not checkLogin():
        csrf = input("Enter your csrftoken: ")
        session = input("Enter your LEETCODE_SESSION: ")
        f = open('cookie', 'w')
        add_string ="LEETCODE_CSRFTOKEN={}\nLEETCODE_SESSION={}".format(csrf, session)
        f.write(add_string)
        f.close()

# Check if csrftoken and LEETCODE_SESSION exist
def checkLogin():
    with open("cookie") as f:
        for line in f:
            (key, val) = line.split("=")
            cookie_pair[key] = val.strip()
    if (
        "LEETCODE_CSRFTOKEN" in cookie_pair.keys()
        and cookie_pair["LEETCODE_CSRFTOKEN"] != ""
        and "LEETCODE_SESSION" in cookie_pair.keys()
        and cookie_pair["LEETCODE_SESSION"] != ""
    ):
        return True
    return False

def makeCookies():
    if checkLogin():
        cookies = {
            "csrftoken": cookie_pair["LEETCODE_CSRFTOKEN"],
            "LEETCODE_SESSION": cookie_pair["LEETCODE_SESSION"],
        }
        return cookies

def getURL():
    return "https://leetcode.com"

# GraphQL query
def SubmissionQuery(offset = 0):
    data = {
        "operationName":"Submissions",
        "variables":{"limit": 30, "offset": offset},
        "query":"query Submissions($limit: Int!, $offset: Int!) {\n  submissionList(offset: $offset, limit: $limit) {\n  hasNext\n  submissions {\n      titleSlug\n      statusDisplay\n      timestamp\n}}}"
        }
    return data

def QuestionQuery(titleSlug):
    data = {
        "operationName":"questionData",
        "variables":{"titleSlug": titleSlug},
        "query":"query questionData($titleSlug: String) {\n  question(titleSlug: $titleSlug) {\n    difficulty\n    }\n}\n"
        }
    return data