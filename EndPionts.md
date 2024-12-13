# end points :
## contests:
### 1. api/contests/int:contest_id/join/ :post this for join a contest:

### 2. api/contests/int:contest_id/participants/: get joining User to a contest
### 3. api/contests/upcontest/: get the first coming contest 

## problems:
### 1. api/problems/int:contest_id/problems/:get probelms from contest
### 2. api/problems/int:problem_id/ :get specific  problem
### 3. api/problems/int:problem_title/ :get specific  problem

### 4. api/problems/int:problem_id/test/: post a code and language and get  percentage of passed test cases 


## submissions: 
### 1. api/int:problem_id/submit/: post code and  


## User :
### 1. api/api/token: post name and possword get a access tkoen and refrech token of jwt 
```
reques post :
{
    "username": "username",  # Replace with your username
    "password": "password"   # Replace with your password
}

respond :
{
    "access": "Access Token",   // Your JWT Access Token
    "refresh": "Refresh Token"   // Your JWT Refresh Token
}
```
### 2. api/api/token/refrech :post a refrech token and get new access token when the access token is expired 

```
reques post :
{
    "refresh": "your_refresh_token"  // Replace with your refresh token
}

respond :
{
    "access": "access token"  // Your new access token
}
```
## board:
### 1.api/board/contest_id/:get dashboard with of contest with id

## condigspace:
### 2.api/codingspace/problem_id/language/:post a default code for problem based on language chosen  