import settings
import requests
import json
import pandas as pd
from datetime import datetime

settings.init_env()
url = settings.getURL()
my_cookies = settings.makeCookies()
session = requests.Session()
requests.utils.add_dict_to_cookiejar(session.cookies, my_cookies)

# Retrieve data


def getData(days=0):
    df_submissions = pd.DataFrame()
    has_next = True
    offset = 0
    date_set = set()
    break_flag = False
    try:
        while has_next and not break_flag:
            response = session.post(
                url+"/graphql", json=settings.SubmissionQuery(offset))
            submission_data = json.loads(response.content.decode('utf-8'))
            for submission in submission_data["data"]["submissionList"]["submissions"]:
                if submission["statusDisplay"] == "Accepted":
                    df_submissions = df_submissions.append(
                        submission, ignore_index=True)
                    date_set.add(datetime.fromtimestamp(
                        int(submission["timestamp"])).strftime("%Y-%m-%d"))
                    if days > 0 and len(date_set) > days:
                        break_flag = True
                        break
            offset += 20
            has_next = submission_data["data"]["submissionList"]["hasNext"]

        df_submissions = mapDifficulty(df_submissions)
    except:
        print("Server not responding. Please try later.")
    return df_submissions

# Join with difficulty


def mapDifficulty(df_submissions):
    if len(df_submissions) > 0:
        df_submissions["Date"] = (pd.to_datetime(df_submissions["timestamp"], unit='s', utc=True)
                                    .dt.tz_convert('US/Pacific')
                                    .dt.strftime("%Y-%m-%d"))
        df_submissions.drop(["timestamp", "statusDisplay"],
                            axis=1, inplace=True)
        df_submissions = df_submissions.drop_duplicates().reset_index(drop=True)
        # Add difficulty
        difficulty = []
        for i in range(len(df_submissions)):
            if i > 0 and df_submissions.loc[i, "titleSlug"] == df_submissions.loc[i-1, "titleSlug"]:
                difficulty.append(difficulty[-1])
            else:
                response = session.post(
                    url+"/graphql", json=settings.QuestionQuery(df_submissions.loc[i, "titleSlug"]))
                question_data = json.loads(response.content.decode('utf-8'))
                
                # get difficulty
                d = question_data["data"]["question"]["difficulty"]
                
                # rename difficulty for column ordering
                if d == 'Easy':
                    d = '1_Easy'
                elif d == 'Medium':
                    d = '2_Medium'
                else:
                    d = '3_Hard'
                difficulty.append(d)
        df_submissions['Difficulty'] = difficulty
    return df_submissions

# Organize and present data


def pivot(df_submissions):
    if len(df_submissions) > 0:
        df_summary = df_submissions.pivot_table(
            index="Date", columns="Difficulty", values="titleSlug", aggfunc='count', fill_value=0)
        df_summary.insert(0, "Total", df_summary.sum(axis=1))
        return df_summary
    else:
        return df_submissions

# Pull all accepted records by date


def allSubmission():
    df_submissions = getData()
    print(pivot(df_submissions))

# Pull recent n days of accepted records by date


def recentNDaySubmission(days):
    df_submissions = getData(days)
    print(pivot(df_submissions).tail(days))


if __name__ == '__main__':
    recentNDaySubmission(10)
