# Kura API 🇰🇪

A secure online polling backend built with Django REST Framework.

## Tech Stack
- Django + DRF
- MySQL
-Simple JWT
-Openrouter API key
- GitHub Actions
s
## Git Flow
- main → production
- develop → staging
- feature/* → development 

## Apps Include
- accounts - for user registration and login
- polls - for admins creating polls
- Votes - For the voting process
- Analysis - Thinking of doing analysis with the help of ai or celery(work to be confirmed)

## Extras
-Ai summarry by gpt-40-mini from openAI. Chatgpt takes in the results and provides an insightful summarry from it.

## END POINTS
# Authentication and Authorization
*login - auth/login
*refresh - auth/refresh
*signup - auth/register
*update - auth/update - to update account
*delete - auth/delete - delete personal account

# Polling
*adding poll- polls/addpoll
*getting poll - polls/getpoll
*adding options - polls/addoptions
*getting options - polls/getoptions
*getting  results - polls/id/results

# Votes
*voting - votes/cast-vote

