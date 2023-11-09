import os
import git
import boto3

repo = git.Repo('.')

commits = list(repo.iter_commits(since='1.day.ago'))

if not commits:
    SUBJECT = 'No Progress Today'
    BODY = 'You should fuck yourself for not making any progress today!'
else:
    SUBJECT = f'Progress Summary: {len(commits)} Commits Today'
    BODY = 'Today Progress Summary:\n\n' + ''.join(f"- {commit.message}" for commit in commits)

# Send email
ses_client = boto3.client('ses', region_name=os.getenv("AWS_REGION"),
                          aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
                          )
response = ses_client.send_email(
    Source=os.getenv("SENDER_EMAIL"),
    Destination={
        'ToAddresses': [
          os.getenv("RECEIVER_EMAIL")
        ],
    },
    Message={
        'Subject': {
            'Data': SUBJECT
        },
        'Body': {
            'Text': {
                'Data': BODY
            },
        },
    }
)
